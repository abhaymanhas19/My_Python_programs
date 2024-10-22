import aiohttp
import asyncio


async def fetch_status(session, url):
    async with session.get(url) as response:
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        # urls = ['https://www.google.com/' for _ in range(1000)]
        urls = ['https://example.com', 'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests,return_exceptions=True)
        print(status_codes)       
        
asyncio.run(main())