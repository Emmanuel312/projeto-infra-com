from socket import *

def upperEncode(data):
    return data.decode().upper()

serverAddress = '127.0.0.1'
serverPort = 13000

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((serverAddress,serverPort))

print('Server on localhost port 13000...')

while True:
    data, clientAddress = serverSocket.recvfrom(2048)
    upper = upperEncode(data)
    serverSocket.sendto(upper.encode(), clientAddress)


