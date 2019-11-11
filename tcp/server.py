from socket import *

serverAddress = '127.0.0.1'
serverPort = 13000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddress,serverPort))

serverSocket.listen(1)

print('Server on port 13000...')

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    data = connectionSocket.recv(2048)

    upper = data.decode().upper()

    connectionSocket.send(upper.encode())
    connectionSocket.close()