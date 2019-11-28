from socket import *
import sys

SERVER_PORT = 8005

# Only support HTTP GET

def main():
    if len(sys.argv) <= 1:
        print("len: {}".format(len(sys.argv)))
        print("Usage: python proxy_server.py [SEVER_IP]")
        sys.exit(2)

    tcp_connection_socket = socket(AF_INET, SOCK_STREAM)
    tcp_connection_socket.bind((sys.argv[1], SERVER_PORT))
    tcp_connection_socket.listen(1)

    while(True):
        print("Proxy ready to serve")
        tcp_client_server, addr= tcp_connection_socket.accept()
        print("Received a connection from: {}".format(addr))
        message = tcp_client_server.recv(1024).decode()
        print("message:",message)
        request_url = message.split()[1].partition("/")[2]
        print("request_url:", request_url)
        file_stored_dir = '/' + request_url
        file_exist = False
        try:
            with open(file_stored_dir[1:], "r") as f:
                file_exist = True
                output_data = f.readlines()
                tcp_client_server.send("HTTP/1.0 200 OK\r\n")
                tcp_client_server.send("Content-Type:text/html\r\n")
                tcp_client_server.sendall(output_data)
                print("Read from the cache")
        except IOError:
            if file_exist == False:
                host_name = request_url.replace("www.", "", 1)
                print("host_name: {}".format(host_name))
                tcp_proxy_socket = socket(AF_INET, SOCK_STREAM)
                tcp_proxy_socket.connect((host_name, 80))
                tcp_proxy_socket.sendall(message.encode())
                proxy_buffer = tcp_proxy_socket.recv(4096)

                with open("./" + host_name,"wb") as tmp_file:
                    for each_line in proxy_buffer:
                        tmp_file.write(each_line)
                tcp_connection_socket.sendall(proxy_buffer.encode())
                tcp_proxy_socket.close()
            else:
                tcp_client_server.send("HTTP/1.0 404 sendErrorErrorError\r\n")
                tcp_client_server.send("Content-Type:text/html\r\n")
                tcp_client_server.send("\r\n")
        tcp_client_server.close()

    tcp_connection_socket.close()

if __name__ == "__main__":
    main()