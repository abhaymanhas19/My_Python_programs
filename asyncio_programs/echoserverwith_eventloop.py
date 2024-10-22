import asyncio
import socket
from asyncio import AbstractEventLoop
from context_maanger  import CustomContextManager

async def echo(connection:socket, loop:AbstractEventLoop)->None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')
            if data == b'boom\r\n':
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        print("error is ",ex)
    finally:
        connection.close()


async def listen_connection(server_socket:socket, loop:AbstractEventLoop) -> None:
    while True:
        connection ,address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connectio from address {address}")
        asyncio.create_task(echo(connection, loop))
        
async def main():
    loop = asyncio.get_event_loop()
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    server_address =("127.0.0.1",8000)
    server_socket.bind(server_address)
    server_socket.setblocking(False)
    server_socket.listen()
    
    await listen_connection(server_socket,asyncio.get_event_loop())
    
    # async with CustomContextManager(server_socket) as connection:
    #     data = await loop.sock_recv(connection, 1024)
    #     print(data)
    
asyncio.run(main())