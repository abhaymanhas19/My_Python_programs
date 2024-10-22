import selectors
import socket
from selectors import SelectorKey
from typing import List,Tuple


selector = selectors.DefaultSelector()
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


socket_address =  ("127.0.0.1",8000)
socket_server.setblocking(False)
socket_server.bind(socket_address)
socket_server.listen()

selector.register(socket_server,selectors.EVENT_READ)

while True:
    events : List[Tuple[SelectorKey,int]] =selector.select(timeout=2)
    if len(events)==0:
        print("No event")
        
    for event,_ in events:
        event_socket = event.fileobj
        
        if event_socket == socket_server:
            connection , address =socket_server.accept()
            connection.setblocking(False)
            selector.register(connection , selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            event_socket.send(data)