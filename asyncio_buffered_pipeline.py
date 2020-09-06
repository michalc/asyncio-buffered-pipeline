import asyncio
import collections

def buffered_pipeline():
    tasks = []

    def queue(size):
        # The regular asyncio.queue doesn't have a function to wait for space
        # in the queue, which we need so we don't iterate upstream until there
        # is space. We also can guarantee there will be at most one getter
        # and putter at any one time, and that _put won't be called until
        # there is space in the queue, so we can have much simpler code than
        # asyncio.Queue

        _queue = collections.deque()
        at_least_one_in_queue = asyncio.Event()
        until_space = asyncio.Event()
        until_space.set()

        async def _space():
            await until_space.wait()

        def _has_items():
            return bool(_queue)

        async def _get():
            nonlocal at_least_one_in_queue
            await at_least_one_in_queue.wait()
            value = _queue.popleft()
            until_space.set()
            if not _queue:
                at_least_one_in_queue = asyncio.Event()
            return value

        def _put(item):
            nonlocal until_space
            _queue.append(item)
            at_least_one_in_queue.set()
            if len(_queue) >= size:
                until_space = asyncio.Event()

        return _space, _has_items, _get, _put

    async def _buffer_iterable(iterable, buffer_size=1):
        nonlocal tasks
        queue_space, queue_has_items, queue_get, queue_put = queue(buffer_size)
        iterator = iterable.__aiter__()

        async def _iterate():
            try:
                while True:
                    await queue_space()
                    value = await iterator.__anext__()
                    queue_put((None, value))
                    value = None  # So value can be garbage collected
            except BaseException as exception:
                queue_put((exception, None))

        task = asyncio.create_task(_iterate())
        tasks.append(task)

        try:
            while queue_has_items() or task:
                exception, value = await queue_get()
                if exception is not None:
                    raise exception from None
                yield value
                value = None  # So value can be garbage collected
        except StopAsyncIteration:
            pass
        except BaseException as exception:
            for task in tasks:
                task.cancel()
            all_tasks = tasks
            tasks = []
            for task in all_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            raise

    return _buffer_iterable
