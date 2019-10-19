from socket import *
import threading

SERVER_PORT = 2828
BUFFER_SIZE = 2048

Server_Socket = socket(AF_INET, SOCK_STREAM)
Server_Socket.bind(('', SERVER_PORT))
Server_Socket.listen(1)
print("Server is ready, waiting for client...")

while True:
    Conn_Socket, addr = Server_Socket.accept()
    try:
        message = Conn_Socket.recv(BUFFER_SIZE).decode()
        print(message)
        request_type = message.split()[0]
        filename = message.split()[1]

        if request_type != 'GET':
            print("Not implemented!")
            Conn_Socket.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            Conn_Socket.send("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n".encode())
            break

        with open(filename[1:]) as fd:
            output_data = fd.read()

        #Send the HTTP Header
        header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (len(output_data))
        Conn_Socket.send(header.encode())
        #Send the HTTP Content
        for i in range(0, len(output_data)):
            Conn_Socket.send(output_data[i].encode())
        Conn_Socket.close()

    except IOError:
        Conn_Socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        Conn_Socket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # error_msg = ' HTTP/1.1 404 Not Found'
        # Conn_Socket.send(error_msg.encode())

Server_Socket.close()


