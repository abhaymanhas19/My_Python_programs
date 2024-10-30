# app.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import httpx
import json
import logging
import requests

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /stream endpoint first
@app.get('/stream')
async def stream(request: Request):
    return StreamingResponse(data_generator(request), media_type='text/event-stream')

# Serve index.html at the root path
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# Mount static files at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

async def data_generator(request):
    external_url = "https://jsonplaceholder.typicode.com/posts"
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", external_url) as response:
            async for chunk in response.aiter_text():
                if await request.is_disconnected():
                    logger.info("Client disconnected")
                    break
                # Optionally, process the chunk before sending
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                await asyncio.sleep(0.1) 
                

# async def data_generator(request):
#     external_url = "https://jsonplaceholder.typicode.com/posts"
#     with requests.get(external_url,stream=True) as response:
#        response.raise_for_status()
#        for line in response.iter_lines(decode_unicode=True):
#             try:
#                 data = json.loads(line)
#             except json.JSONDecodeError:
#                 data = {'content': line}
#             yield f"data: {json.dumps(data)}\n\n"
        