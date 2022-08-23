from socket import *
import hashlib
import time
import os

BUFFERED_PACKET_SIZE = 2048
FILE_LIST = 'fileList.txt'

clientSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)

def checkFileExistence(filename):
    if os.path.exists(filename):
        return True
    return False

def calculateSha256(filename):
    file = open(filename,'rb')
    fileBytes = file.read()
    hashResult = hashlib.sha256(fileBytes)
    return hashResult.hexdigest()

def sendData(filename):
    print("* Confirming file existance")
    if checkFileExistence(filename):
        clientSocket.sendto('continue'.encode('utf8'),serverSocketAddress)
        print("* File found")
    else:
        clientSocket.sendto('abort'.encode('utf8'),serverSocketAddress)
        print("* File not found")
        print("* Transfer aborted")
        return
    clientSocket.sendto(str(calculateSha256(filename)).encode('utf8') ,serverSocketAddress)
    print("* Sent the hashing of the file")
    clientSocket.sendto(filename.encode('utf8'),serverSocketAddress)
    print("* Sent filename")
    fileToSend = open(filename,'rb')
    packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    print("* Sending the file...")
    while (packet):
        clientSocket.sendto(packet,serverSocketAddress)
        packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    fileToSend.close()
    print("* File sent")

def receiveData():
    flag, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    if (flag.decode('utf8') == 'abort'):
        print("* File not found\n* Tranfer failed")
        return
    hash, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    filenameToDecode, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    print("* File found, now downloading...")
    filename = filenameToDecode.decode('utf8')
    receivedFile = open(filename,'wb')
    packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    try:
        while (packet):
            receivedFile.write(packet)
            clientSocket.settimeout(1)
            packet, address = clientSocket.recvfrom(BUFFERED_PACKET_SIZE)
    except timeout:
        receivedFile.close()
    if (checkFileExistence(filename)):
        print("* File downloaded, now checking integrity...")
    else:
        print("* Download failed, please retry")
        return
    if (calculateSha256(filename) == str(hash.decode('utf8'))):
        print("* File successfully downloaded")
    else:
        print("* File corrupted, deleting corrupted file. Please try again")
        os.remove(filename)

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
        print("* Here's all files avaiable for download")
        for line in list:
            print('#) '+line, end='')
        list.close()
        os.remove(FILE_LIST)
    elif command == 'get':
        sentFlag = clientSocket.sendto(clientMessage.encode('utf8'),serverSocketAddress)
        receiveData()
    elif command == 'put':
        sentFlag = clientSocket.sendto(clientMessage.encode('utf8'),serverSocketAddress)
        sendData(clientMessage.split()[1])
    else :
        print("* This request is not recognized, please rety")