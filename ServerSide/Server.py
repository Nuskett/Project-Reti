from socket import *
import hashlib
import time
import os

BUFFERED_PACKET_SIZE = 2048
FILE_LIST = 'fileList.txt'

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocketAddress = ('localhost',8080)
serverSocket.bind(serverSocketAddress)
print("* Server online")

def createFileList():
    fileList = open(FILE_LIST,'w')
    for file in os.listdir(os.getcwd()):
        if ((file != FILE_LIST) and (file != os.path.basename(__file__))):
            fileList.write(file+'\n')
    fileList.close()

def checkFileExistence(filename):
    if os.path.exists(filename):
        return True
    return False

def calculateSha256(filename):
    file = open(filename,'rb')
    fileBytes = file.read()
    hashResult = hashlib.sha256(fileBytes)
    return hashResult.hexdigest()

def receiveDatafromClient():
    flag, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)
    if (flag.decode('utf8') == 'abort'):
        print("* File not found\n* Tranfer failed")
        return
    hash, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)
    filenameToDecode, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)
    print("* File found, now downloading...")
    filename = filenameToDecode.decode('utf8')
    receivedFile = open(filename,'wb')
    packet, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)
    try:
        while (packet):
            receivedFile.write(packet)
            serverSocket.settimeout(1)
            packet, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)
    except timeout:
        receivedFile.close()
    serverSocket.settimeout(None)
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

def sendFileToClient(filename,address):
    print("* Confirming file existance")
    if checkFileExistence(filename):
        serverSocket.sendto('continue'.encode('utf8'),address)
        print("* File found")
    else:
        serverSocket.sendto('abort'.encode('utf8'),address)
        print("* File not found")
        print("* Transfer aborted")
        return
    serverSocket.sendto(str(calculateSha256(filename)).encode('utf8') ,address)
    print("* Sent the hashing of the file")
    serverSocket.sendto(filename.encode('utf8'),address)
    print("* Sent filename")
    fileToSend = open(filename,'rb')
    packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    print("* Sending the file...")
    while (packet):
        serverSocket.sendto(packet,address)
        packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    fileToSend.close()
    print("* File sent")

while True:
    print("* Waiting for client...")
    data, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)

    clientRequest = data.decode('utf8')
    print("* Request was (%s)" % clientRequest)
    command = clientRequest.split()[0]

    if command == 'exit':
        print("* Closing the server")
        serverSocket.close
        exit()
    elif command == 'list':
        createFileList()
        sendFileToClient(FILE_LIST,address)
        os.remove(FILE_LIST)
    elif command == 'get':
        sendFileToClient(clientRequest.split()[1],address)
    elif command == 'put':
        receiveDatafromClient()