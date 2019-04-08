# requires python 3.7
import asyncio
import requests
import time


async def req_coro():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(
        None, requests.get, 'http://www.google.com.mx')
    future2 = loop.run_in_executor(
        None, requests.get, 'http://www.google.co.uk')
    # response1 = await future1
    # response2 = await future2
    # print(time.monotonic(), 'waiting 5')
    await asyncio.sleep(0.01)
    res = await asyncio.gather(future1, future2)
    print(res[0].text[:60])
    print(res[1].text[:60])
    # print(response1.text[:60])
    # print(response2.text[:60])

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


def main():
    asyncio.run(req_coro())


if __name__ == "__main__":
    main()
