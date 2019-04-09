import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import time

import requests


def blocking(n):
    print(f'im blocking things !!! {n} pid={os.getpid()}')
    resp = requests.get('https://postman-echo.com/delay/3')
    print(f'ok done {n} pid={os.getpid()}')
    return resp


async def run_blocking(executor):
    print('here')
    loop = asyncio.get_event_loop()
    procs = [loop.run_in_executor(executor, blocking, n) for n in range(200)]

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

    executor = ThreadPoolExecutor(max_workers=50)

    loop = asyncio.get_event_loop()
    s = time.perf_counter()
    try:
        result = loop.run_until_complete(run_blocking(executor))
    finally:
        loop.close()
    print(f'{result}')
    print(f'done in {time.perf_counter()-s} seconds')


if __name__ == '__main__':
    main()
