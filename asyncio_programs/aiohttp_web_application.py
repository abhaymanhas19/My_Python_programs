import asyncio
from aiohttp import web
import json

async def hello_handler(request):
    # Simple text response
    return web.Response(text="Hello, world!")

async def json_handler(request):
    # Return a JSON response
    data = {"message": "Hello, this is a JSON response!", "status": "ok"}
    return web.json_response(data)

async def add_handler(request):
    # Extract query parameters: /add?x=10&y=20
    x = int(request.query.get('x', 0))
    y = int(request.query.get('y', 0))
    result = x + y
    return web.Response(text=f"The sum of {x} and {y} is {result}")

async def delay_handler(request):
    # Simulate a short async delay
    delay = float(request.query.get('sec', 1.0))
    await asyncio.sleep(delay)
    return web.Response(text=f"Waited for {delay} seconds!")

async def echo_handler(request):
    # Read text data from the request and echo it back
    # For example, send a POST request with text in the body.
    text = await request.text()
    return web.Response(text=f"You sent: {text}")

async def main():
    app = web.Application()
    # Add multiple routes with different tasks
    app.router.add_get('/', hello_handler)
    app.router.add_get('/json', json_handler)
    app.router.add_get('/add', add_handler)
    app.router.add_get('/delay', delay_handler)
    app.router.add_post('/echo', echo_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    
    http_site = web.TCPSite(runner, '0.0.0.0', 8080)
    https_site = web.TCPSite(runner, '0.0.0.0', 8443, ssl_context=ssl_context)

    await http_site.start()
    await https_site.start()
    

    print("Server started at http://127.0.0.1:8080")
    # Keep running until stopped
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
