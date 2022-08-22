from pydoc import cli
from socket import *
import os
import time

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

while True:
    print("* Waiting for client...")
    data, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)

    clientRequest = data.decode('utf8')
    print("Request was (%s)" % clientRequest)
    command = clientRequest.split()[0]


    if command == 'exit':
        serverSocket.close
        exit()
    elif command == 'list':
        createFileList()
        #sentFlag = serverSocket.sendto()
    elif command == 'get':
        sentFlag = serverSocket.sendto()
    elif command == 'put':
        sentFlag = serverSocket.sendto()