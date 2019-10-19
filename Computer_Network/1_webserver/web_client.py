from socket import *
from web_server import SERVER_PORT

SERVER_NAME = '192.168.0.107'
BUFFER_SIZE = 2048

Client_Socket = socket(AF_INET, SOCK_STREAM)
Client_Socket.connect((SERVER_NAME, SERVER_PORT))
print("Client is connneting to server...")
Client_Socket.send("GET /HelloWorld.html HTTP/1.1\r\n\r\n")
reply_content = Client_Socket.recv(BUFFER_SIZE)
print(reply_content)

Client_Socket.close()

