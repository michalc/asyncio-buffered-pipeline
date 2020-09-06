# asyncio-buffered-pipeline [![CircleCI](https://circleci.com/gh/michalc/asyncio-buffered-pipeline.svg?style=shield)](https://circleci.com/gh/michalc/asyncio-buffered-pipeline) [![Test Coverage](https://api.codeclimate.com/v1/badges/84661ec860980bc4b5ab/test_coverage)](https://codeclimate.com/github/michalc/asyncio-buffered-pipeline/test_coverage)

Parallelise pipelines of Python async iterables/generators.

## Installation

```bash
pip install asyncio-buffered-pipeline
```

## Usage / What problem does this solve?

If you have a chain of async generators, even though each is async, only one runs at any given time. For example, the below runs in (just over) 30 seconds.

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
from asyncio_buffered_pipeline import buffered_pipeline

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

The `buffered_pipeline` ensures internal tasks are cancelled on any exception.

### Buffer size

The default buffer size is 1. This is suitable if each iteration takes approximately the same amount of time. If this is not the case, you may wish to change it using the `buffer_size` parameter of `buffer_iterable`.

```python
it = buffer_iterable(gen(), buffer_size=2)
```

## Features

- Only one task is created for each `buffer_iterable`, in which the iterable is iterated over, with its values stored in an internal buffer.

- All the tasks of the pipeline are cancelled if any of the generators raise an exception.

- If a generator raises an exception, the exception is propagated to calling code.

- The buffer size of each step in the pipeline is configurable.

- The "chaining" is not abstracted away. You still have full control over the arguments passed to each step, and you don't need to buffer each iterable in the pipeline if you don't want to: just don't pass those through `buffer_iterable`.
