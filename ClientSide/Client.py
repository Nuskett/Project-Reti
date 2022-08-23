from socket import *
import time
import os

BUFFERED_PACKET_SIZE = 2048
FILE_LIST = 'fileList.txt'

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)

#bisogna fare il controllo di hashing e gestione errori
#aggiungi display status per update del client
def receiveData():
    flag, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    if (flag.decode('utf8') == 'abort'):
        print("* File not found\n* Tranfer failed")
        return
    filenameToDecode, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    filename = filenameToDecode.decode('utf8')
    receivedFile = open(filename,'wb')
    packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    while (packet):
        receivedFile.write(packet)
        packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)


while True:
    clientMessage = input("* Type the message to send to the server\n>>")
    command = clientMessage.split()[0]
    print("* Waiting for server...")

    print(command)

    if command == 'exit':
        sentFlag = clientSocket.sendto(command.encode('utf8'),serverSocketAddress)
        print("Closing the client")
        clientSocket.close()
        exit()
    elif command == 'list':
        sentFlag = clientSocket.sendto(command.encode('utf8'),serverSocketAddress)
        receiveData()
    elif command == 'get':
        sentFlag = clientSocket.sendto()
    elif command == 'put':
        sentFlag = clientSocket.sendto()
    else :
        print("* This request is not recognized, please rety")