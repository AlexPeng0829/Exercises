from socket import *
import threading

SERVER_PORT = 8080
BUFFER_SIZE = 2048
MAX_CONNECTION = 1

def Serve_Single_Client(Conn_Socket=None):
    message = Conn_Socket.recv(BUFFER_SIZE).decode()
    print(message)
    # if len(message) == 0:
    #     print("Empty message from client, skip!")
    # Conn_Socket.close()
    # return
    
    request_type = message.split()[0]
    filename = message.split()[1]
    try:
        if request_type != 'GET':
            print("Not implemented!")
            Conn_Socket.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            Conn_Socket.send("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n".encode())
            Conn_Socket.close()
            return

        with open(filename[1:]) as fd:
            output_data = fd.read()

        #Send the HTTP Header
        header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (len(output_data))
        Conn_Socket.send(header.encode())
        #Send the HTTP Content
        Conn_Socket.send(output_data.encode())
    except IOError:
        Conn_Socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        Conn_Socket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    Conn_Socket.close()
    return

def main():
    Server_Socket = socket(AF_INET, SOCK_STREAM)
    Server_Socket.bind(('', SERVER_PORT))
    Server_Socket.listen(MAX_CONNECTION)
    print("Server is ready, waiting for client...")
    while True:
        Conn_Socket, addr = Server_Socket.accept()  
        kThread = threading.Thread(target=Serve_Single_Client, kwargs={'Conn_Socket':Conn_Socket})
        kThread.start()
    Server_Socket.close()
    sys.exit()

if __name__ == "__main__":
    main()


