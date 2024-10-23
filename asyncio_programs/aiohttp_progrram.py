import aiohttp
import asyncio


async def fetch_status(session, url):
    async with session.get(url) as response:
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.google.com/' for _ in range(1000)]
        # urls = ['https://example.com', 'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        
        #asyncio.gather takes list of courtine and gives the result when all the countine complete his job.
        status_codes = await asyncio.gather(*requests,return_exceptions=True)
        
        
        # AS_COMPLETED  is a function that give the result of the courtine as they finished it without waiting to complete all courtine.but there is no deterministic ordering of results
        # for finished_task in asyncio.as_completed(requests,timeout=2):
        #     print(await finished_task)
        
        # done_task, pending_task = await asyncio.wait(requests)
        # done_task,pending_task= await asyncio.wait(requests,return_when=asyncio.FIRST_COMPLETED)
        # done_task, pending_task= await asyncio.wait(requests,return_when=asyncio.FIRST_EXCEPTION)
        
        
        # by this process we know which task is completed and which task is pending that overcome the Drawback of as_completed function because as_completed function res.ult order is nondeterministic 
        # while pending:
        #     done, pending = await asyncio.wait(pending,
        #     return_when=asyncio.FIRST_COMPLETED)
        #     print(f'Done task count: {len(done)}')
        #     print(f'Pending task count: {len(pending)}')
        #     for done_task in done:
        #          print(await done_task)
        print(status_codes)       
        
asyncio.run(main())