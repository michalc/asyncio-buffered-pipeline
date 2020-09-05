import asyncio

def buffered_pipeline():
    tasks = []

    async def _buffer_iterable(iterable, buffer_size=1):
        queue = asyncio.Queue(maxsize=buffer_size)

        async def _iterate():
            try:
                async for value in iterable:
                    await queue.put((None, value))
            except asyncio.CancelledError:
                raise
            except Exception as exception:
                await queue.put((exception, None))

        task = asyncio.create_task(_iterate())
        tasks.append(task)

        try:
            while not queue.empty() or not task.done():
                exception, value = await queue.get()
                queue.task_done()
                if exception is not None:
                    raise exception from None
                yield value
        except BaseException as exception:
            for task in tasks:
                task.cancel()
            tasks.clear()
            raise

    return _buffer_iterable
