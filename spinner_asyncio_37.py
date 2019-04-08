# requires python 3.7
import asyncio
import itertools
import sys


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    # pretent wiating a long time for I/O
    await asyncio.sleep(3)
    return 123


async def supervisor():
    spinner = asyncio.create_task(spin('working...'))
    print('spinner object', spinner)
    result = await slow_function()
    spinner.cancel()
    return result


def main():
    result = asyncio.run(supervisor())
    print('Answer: ', result)


if __name__ == "__main__":
    main()
