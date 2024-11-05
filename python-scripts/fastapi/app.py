# app.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import httpx
import json
import logging
import requests
from time import sleep

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @app.get('/stream')
# async def stream(request: Request):
#     return StreamingResponse(data_generator(request), media_type='text/event-stream')

@app.get('/stream')
def stream(request: Request):
    return data_generator(request)


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


# async def data_generator(request):
#     external_url = "https://jsonplaceholder.typicode.com/posts"
#     async with httpx.AsyncClient() as client:
#         async with client.stream("GET", external_url) as response:
#             async for chunk in response.aiter_text():
#                 if await request.is_disconnected():
#                     logger.info("Client disconnected")
#                     break
#                 # Optionally, process the chunk before sending
#                 yield f"data: {json.dumps({'content': chunk})}\n\n"
#                 await asyncio.sleep(0.1) 
                

# def data_generator(request):
#     external_url = "https://jsonplaceholder.typicode.com/posts"
#     with requests.get(external_url,stream=True) as response:
#        response.raise_for_status()
#        for line in response.iter_lines(decode_unicode=True):
#             try:
#                 data = json.loads(line)
#             except json.JSONDecodeError:
#                 data = {'content': line}
#             yield f"data: {json.dumps(data)}\n\n"
        
        
def data_generator(request):
    total=0
    for i in range(100):
        sleep(1)
        print(i)
        total+=i
    return total
        