from socket import *
import hashlib
import time
import os

BUFFERED_PACKET_SIZE = 2048
FILE_LIST = 'fileList.txt'

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)

def receiveData():
    flag, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    if (flag.decode('utf8') == 'abort'):
        print("* File not found\n* Tranfer failed")
        return
    filenameToDecode, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    print("* File found, now downloading...")
    filename = filenameToDecode.decode('utf8')
    receivedFile = open(filename,'wb')
    packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    try:
        while (packet):
            receivedFile.write(packet)
            clientSocket.settimeout(5)
            packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    except timeout:
        receivedFile.close()
        print("* File downloaded, now checking integrity...")
        #to-do add hashing check

while True:
    clientMessage = input("* Type the message to send to the server\n>>")
    command = clientMessage.split()[0]
    print("* Waiting for server...")

    if command == 'exit':
        sentFlag = clientSocket.sendto(command.encode('utf8'),serverSocketAddress)
        print("* Closing the client")
        clientSocket.close()
        exit()
    elif command == 'list':
        sentFlag = clientSocket.sendto(command.encode('utf8'),serverSocketAddress)
        receiveData()
        list = open(FILE_LIST,'r')
        print("* Here's all files avaiable for download\n")
        for line in list:
            print('#) '+line)
        list.close()
        os.remove(FILE_LIST)
    elif command == 'get':
        sentFlag = clientSocket.sendto()
    elif command == 'put':
        sentFlag = clientSocket.sendto()
    else :
        print("* This request is not recognized, please rety")