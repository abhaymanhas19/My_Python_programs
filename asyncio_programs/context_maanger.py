import asyncio

#A context manager in Python is an object that is used to manage resources.
class CustomContextManager:
    def __init__(self, server_socket):
        self._server_socket = server_socket
        self._connection = None
    
    async def __aenter__(self):
        loop = asyncio.get_event_loop()
        connection , address = await loop.sock_recv(self._server_socket)
        self._connection=connection
        return self._connection
        
        
    async def __aexit__(self,exc_type,exc_val,exc_tb):
        self._connection.close()
     
# async def main():   
#     async with CustomContextManager() as manager:
#         print("Asf")
        

# asyncio.run(main())