from socket import *
import time

BUFFERED_PACKET_SIZE = 2048

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)

while True:
    clientMessage = input("* Type the message to send to the server\n>>")
    sentFlag = clientSocket.sendto(clientMessage.encode(),serverSocketAddress)
    print("* Waiting to receive...")


    data, server = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    serverAnswer = data.decode('utf8')

    if serverAnswer == 'exit':
        clientSocket.close
        exit()
    else :
        print(data.decode('utf8'))