from socket import *
import time
from UDPPingerServer import SERVER_PORT

SERVER_NAME = '127.0.0.1'
TIME_OUT = 1

def main():
    
    RTTs = list()
    Client_Socket = socket(AF_INET, SOCK_DGRAM)
    Client_Socket.settimeout(TIME_OUT)
    
    for trial_count in range(1,11):
        send_asctime = time.asctime() 
        send_time_in_second = time.time()
        ping_msg = 'ping ' + str(trial_count) + ' ' + send_asctime
        Client_Socket.sendto(ping_msg.encode(), (SERVER_NAME, SERVER_PORT))
      
        try:
            Modified_Msg = Client_Socket.recv(2048)
            receive_time_in_second = time.time()
            RTT = receive_time_in_second - send_time_in_second
            print("RTT: {} (s)".format(RTT))
            print(Modified_Msg.decode())
            RTTs.append(RTT)
        except:
            print('Request time out!')
            continue
    
    Client_Socket.close()
    print('Avg RTT: {}'.format(sum(RTTs)/len(RTTs)))

if __name__ == '__main__':
    main()