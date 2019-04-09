import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import time


def blocking(n):
    print(f'im blocking things !!! {n} pid={os.getpid()}')
    time.sleep(1)
    print(f'ok done {n} pid={os.getpid()}')
    return (n, n**2)


async def run_blocking(executor):
    print('here')
    loop = asyncio.get_event_loop()
    procs = [loop.run_in_executor(executor, blocking, n) for n in range(100)]

    # results are stored as they complete
    # completed, _ = await asyncio.wait(procs)
    #results = [p.result() for p in completed]

    # results are stored in the same order they were called
    results = await asyncio.gather(*procs)

    print(f'results {results}')
    return results


def main():
    # for cpu intensive tasks
    #executor = ProcessPoolExecutor(max_workers=None)

    # for i/o intensive tasks
    executor = ThreadPoolExecutor(max_workers=100)

    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(run_blocking(executor))
    finally:
        loop.close()
    print(f'{result}')


if __name__ == '__main__':
    main()
