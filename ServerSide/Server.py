from pydoc import cli
from socket import *
import os
from struct import pack
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
    fileList.close()

def checkFileExistence(filename):
    if os.path.exists(filename):
        return True
    return False


#bisogna fare il controllo di hashing
#aggiungi display status per update del server
def sendFileToClient(filename,address):
    #prima controllo se esiste e mando il risultato come messaggio
    if checkFileExistence(filename):
        serverSocket.sendto('continue'.encode('utf8'),address)
    else:
        serverSocket.sendto('abort'.encode('utf8'),address)
        return
    #mando il nome del file per crearlo
    serverSocket.sendto(filename.encode('utf8'),address)
    fileToSend = open(filename,'rb')
    packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    while (packet):
        serverSocket.sendto(packet,address)
        packet = fileToSend.read(BUFFERED_PACKET_SIZE)
    fileToSend.close()



while True:
    print("* Waiting for client...")
    data, address = serverSocket.recvfrom(BUFFERED_PACKET_SIZE)

    clientRequest = data.decode('utf8')
    print("Request was (%s)" % clientRequest)
    command = clientRequest.split()[0]


    if command == 'exit':
        print("Closing the server")
        serverSocket.close
        exit()
    elif command == 'list':
        createFileList()
        sendFileToClient(FILE_LIST,address)
    elif command == 'get':
        sentFlag = serverSocket.sendto()
    elif command == 'put':
        sentFlag = serverSocket.sendto()