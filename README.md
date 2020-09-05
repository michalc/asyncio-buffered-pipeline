# asyncio-buffered-pipeline [![CircleCI](https://circleci.com/gh/michalc/asyncio-buffered-pipeline.svg?style=shield)](https://circleci.com/gh/michalc/asyncio-buffered-pipeline) [![Test Coverage](https://api.codeclimate.com/v1/badges/84661ec860980bc4b5ab/test_coverage)](https://codeclimate.com/github/michalc/asyncio-buffered-pipeline/test_coverage)

Parallelise pipelines of Python async iterables/generators.

## Installation

```bash
pip install asyncio-buffered-pipeline
```

## Usage / What problem does this solve?

If you have a pipeline of async generators, even though each is async, only one runs at any given time. For example, the below runs in (just over) 30 seconds.

```python
import asyncio

async def gen_1():
    for value in range(0, 10):
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value

async def gen_2(it):
    async for value in it:
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value * 2

async def gen_3(it):
    async for value in it:
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value + 3

async def main():
    it_1 = gen_1()
    it_2 = gen_2(it_1)
    it_3 = gen_3(it_2)

    async for val in it_3:
        print(val)

asyncio.run(main())
```

The `buffered_pipeline` function allows you to make to a small change, passing each generator through its return value, to parallelise the generators to reduce this to (just over) 12 seconds.

```python
import asyncio
from asyncio_buffer_iterable import buffered_pipeline

async def gen_1():
    for value in range(0, 10):
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value

async def gen_2(it):
    async for value in it:
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value * 2

async def gen_3(it):
    async for value in it:
        await asyncio.sleep(1)  # Could be a slow HTTP request
        yield value + 3

async def main():
    buffer_iterable = buffered_pipeline()
    it_1 = buffer_iterable(gen_1())
    it_2 = buffer_iterable(gen_2(it_1))
    it_3 = buffer_iterable(gen_3(it_2))

    async for val in it_3:
        print(val)

asyncio.run(main())
```

The `buffered_pipeline` ensures internal tasks are cleaned up on any exception.
