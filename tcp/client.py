from socket import *

serverAddress = '127.0.0.1'
serverPort = 13000

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverAddress,serverPort))

message = input('Type a message to server: ')

clientSocket.send(message.encode())
data = clientSocket.recv(2048)

print(data.decode())

clientSocket.close()





