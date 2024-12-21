import asyncio
import aiohttp
import random
from fp.fp import FreeProxy
import FreeProxy


async def make_request(session, url, method='GET', headers=None, data=None):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
      
    }
    connector = None 
    try:
        if method == 'GET':
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
        elif method == 'POST':
            async with session.post(url, headers=headers, data=data) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error making request: {e}")
        return None
    
    
    
async def main():
    URL="https://www.g4k.go.kr:9043/robots.txt"
    method = 'GET'  # Change to 'POST' if needed
    data = None  # Data to send in POST request
    
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(make_request(session,URL,method,data)) for _ in range(2)]
        responses = await asyncio.gather(*tasks)
         
    with open('responses.txt', 'w') as f:
        for response in responses:
            if response:
                f.write(response + '\n')



if __name__=="__main__":              
    asyncio.run(main())