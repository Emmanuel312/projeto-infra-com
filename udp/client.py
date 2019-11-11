from socket import *

# server info
serverAddress = '127.0.0.1'
serverPort = 13000

clientSocket = socket(AF_INET,SOCK_DGRAM)

message = input('Type message to server: ')

clientSocket.sendto(message.encode(),(serverAddress,serverPort))
data, serverAddress = clientSocket.recvfrom(2048)

print(data.decode())

clientSocket.close()



