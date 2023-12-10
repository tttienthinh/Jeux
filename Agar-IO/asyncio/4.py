import asyncio
import aiohttp
import time

async def fetch_url(url):
    start = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
            print(f"{time.time()-start} for {url}")
            return result

async def main():
    start = time.time()
    url_1 = "https://www.wikipedia.org/"
    url_2 = "https://www.google.com" 

    task1 = asyncio.create_task(fetch_url(url_1))
    task2 = asyncio.create_task(fetch_url(url_2))    
    data1 = await task1
    data2 = await task2    
    print("Data from ",url_1, len(data1), "bytes")
    print("Data from ",url_2, len(data2), "bytes")
    print(time.time()-start)

# Run the event loop
asyncio.run(main())