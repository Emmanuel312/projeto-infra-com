from socket import *

# dns info
dnsAddress = '127.0.0.1'
dnsPort = 5300

hostName = 'C virtus.ufpe.br'

clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.sendto(hostName.encode(),(dnsAddress,dnsPort))

data, dnsInfo = clientSocket.recvfrom(2048)

print(data.decode())