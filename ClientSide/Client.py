from socket import *
import time
import os

BUFFERED_PACKET_SIZE = 2048
FILE_LIST = 'fileList.txt'

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)

while True:
    clientMessage = input("* Type the message to send to the server\n>>")
    command = clientMessage.split()[0]
    print("* Waiting for server...")

    print(command)

    if command == 'exit':
        sentFlag = clientSocket.sendto(command.encode(),serverSocketAddress)
        clientSocket.close()
        exit()
    elif command == 'list':
        sentFlag = clientSocket.sendto(command.encode(),serverSocketAddress)
    elif command == 'get':
        sentFlag = clientSocket.sendto()
    elif command == 'put':
        sentFlag = clientSocket.sendto()
    else :
        print("* This request is not recognized, please rety")