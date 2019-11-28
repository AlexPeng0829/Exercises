from socket import *
from web_server import SERVER_PORT

LOCAL_HOST = '127.0.0.1'
# SERVER_NAME = '192.168.0.107'
SERVER_NAME = LOCAL_HOST
BUFFER_SIZE = 2048

FILE_PATH = '/HelloWorld.html'

Client_Socket = socket(AF_INET, SOCK_STREAM)
# Client_Socket.connect((SERVER_NAME, SERVER_PORT))
Client_Socket.connect((LOCAL_HOST, SERVER_PORT))
print("Client is connneting to server...")
request_head_1 = 'GET {}'.format(FILE_PATH)
request_head_2=' HTTP/1.1\nHost: {}:{}\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\n\
Purpose: prefetch\n\
Accept-Encoding: gzip, deflate, br\n\
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8'.format(SERVER_NAME, str(SERVER_PORT))
request_msg = request_head_1 + FILE_PATH + request_head_2 + SERVER_NAME
Client_Socket.send((request_head_1 + request_head_2).encode())
reply_content = Client_Socket.recv(BUFFER_SIZE)
print(reply_content.decode())

Client_Socket.close()


