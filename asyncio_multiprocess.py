
import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from random import randint


async def sub_main(seq):
    # do something that takes a random time
    await asyncio.sleep(randint(0, 5)*.1)
    print(seq, 'subprocess done.', os.getpid())
    return (seq, os.getpid())  # return your result


def sub_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    tasks = map(loop.create_task, map(sub_main, range(5)))
    return loop.run_until_complete(asyncio.gather(*tasks))


async def start(executor):
    # await asyncio.get_event_loop().run_in_executor(executor, sub_loop)
    procs = []
    for i in range(10):
        procs.append(asyncio.get_event_loop(
        ).run_in_executor(executor, sub_loop))
    result = await asyncio.gather(*procs)
    for r in result:
        print(r)
if __name__ == '__main__':
    executor = ProcessPoolExecutor()
    asyncio.get_event_loop().run_until_complete(start(executor))
    print(os.cpu_count(), " cpu\'s")
