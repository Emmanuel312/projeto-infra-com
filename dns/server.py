from socket import *

# dns info
dnsAddress = '127.0.0.1'
dnsPort = 5300

# server info
serverAddress = '127.0.0.1'
serverPort = 13000


serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((serverAddress,serverPort))

info = 'R virtus.ufpe.br 127.0.0.1'
serverSocket.sendto(info.encode(), (dnsAddress,dnsPort))

while True:
    data, serverInfo = serverSocket.recvfrom(2048)
    print(data.decode(), serverInfo)





