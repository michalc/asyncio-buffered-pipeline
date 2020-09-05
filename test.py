import asyncio
from unittest import (
    TestCase,
)

from asyncio_buffer_iterable import buffer_iterable


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestBufferIterable(TestCase):

    @async_test
    async def test_chain_all_buffered(self):
        async def gen_1():
            for value in range(0, 10):
                yield value

        async def gen_2(it):
            async for value in it:
                yield value * 2

        async def gen_3(it):
            async for value in it:
                yield value + 3

        it_1 = buffer_iterable(gen_1())
        it_2 = buffer_iterable(gen_2(it_1))
        it_3 = buffer_iterable(gen_3(it_2))

        values = [value async for value in it_3]
        self.assertEqual(values, [3, 5, 7, 9, 11, 13, 15, 17, 19, 21])

    @async_test
    async def test_chain_some_buffered(self):
        async def gen_1():
            for value in range(0, 10):
                yield value

        async def gen_2(it):
            async for value in it:
                yield value * 2

        async def gen_3(it):
            async for value in it:
                yield value + 3

        it_1 = buffer_iterable(gen_1())
        it_2 = gen_2(it_1)
        it_3 = buffer_iterable(gen_3(it_2))

        values = [value async for value in it_3]
        self.assertEqual(values, [3, 5, 7, 9, 11, 13, 15, 17, 19, 21])

    @async_test
    async def test_chain_parallel(self):
        num_gen_1 = 0
        num_gen_2 = 0
        num_gen_3 = 0

        async def gen_1():
            nonlocal num_gen_1
            for value in range(0, 10):
                yield
                num_gen_1 += 1

        async def gen_2(it):
            nonlocal num_gen_2
            async for value in it:
                yield
                num_gen_2 += 1

        async def gen_3(it):
            nonlocal num_gen_3
            async for value in it:
                yield
                num_gen_3 += 1

        it_1 = buffer_iterable(gen_1())
        it_2 = buffer_iterable(gen_2(it_1))
        it_3 = buffer_iterable(gen_3(it_2))

        num_done = []
        async for _ in it_3:
            # Slight hack to wait for buffers to be full
            await asyncio.sleep(0.02)
            num_done.append((num_gen_1, num_gen_2, num_gen_3))

        self.assertEqual(num_done, [
            (6, 4, 2), (7, 5, 3), (8, 6, 4), (9, 7, 5), (10, 8, 6),
            (10, 9, 7), (10, 10, 8), (10, 10, 9), (10, 10, 10), (10, 10, 10),
        ])
