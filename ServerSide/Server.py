from socket import *
import time

BUFFERED_PACKET_SIZE = 2048

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)
serverSocket.bind(serverSocketAddress)
print("* Server online")

while True:
    print("* Waiting for client...")
    data, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)

    print("* Received %s bytes from %s" % (len(data),address))
    clientRequest = data.decode('utf8')
    print("Request was (%s)" % clientRequest)
    
    if clientRequest == 'exit':
        sentFlag = serverSocket.sendto(data,address)
        serverSocket.close
        exit()
    else :
        sentFlag = serverSocket.sendto("* This request is not recognized, please rety".encode(),address)