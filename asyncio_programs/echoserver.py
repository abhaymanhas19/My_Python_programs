import socket

# socker AF_INET tells us which type of address our socket will interact  and SOCK_STREAM means that we are using TCP protocol for communication
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# To set the SO_REUSEADDR to one  is allow us to reuse the port number after we stop and restart the application
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# we need to addresss to bind with socker so client can talks to 
address = ('127.0.0.1', 8000)
socket_server.bind(address)

# to listen socker for incoming connection
socket_server.listen()

#Running socket in not blocking mode
socket_server.setblocking(False)


connections = []
try:
    while True:
        try :
            connection, client_address = socket_server.accept()
            connection.setblocking(False)
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
        except BlockingIOError:
            pass
        
        for connection in connections:
            try:
                buffer = b""
                
                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f'I got data: {data}!')
                        buffer+=data
                print(f"All the data is: {buffer}")
                connection.send(buffer)
            except BlockingIOError:
                pass
finally:
    socket_server.close()