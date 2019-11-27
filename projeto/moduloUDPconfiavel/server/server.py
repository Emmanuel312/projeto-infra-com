from socket import *
from os import listdir
import pickle
import json


class Packet:
    def __init__(self,seq,ack = None,data = None,):
        self.seq = seq
        self.ack = ack
        self.data = data


# nome do repositorio que contem os arquivos do servidor
repo = 'repo1'
serverIp = socket.gethostbyname(socket.gethostname())

def packetEncode(packet):
    packetJson = json.dumps(packet.__dict__)
    packetEncoded = pickle.dumps(packetJson)

    return packetEncoded

def packetDecode(packet):
    packetReceived = pickle.loads(data)
    packetReceived = json.loads(packetReceived) # json to dict
    
    return packetReceived


def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    info = 'R a ' + serverIp
    # dns info
    dnsAddress = '127.0.0.1'
    dnsPort = 5300

    registerDnsSocket.sendto(info.encode(), (dnsAddress,dnsPort))
    data, serverInfo = registerDnsSocket.recvfrom(2048)

    return data,serverInfo

def file_exists(requestedFile):
    return requestedFile in listdir('./' + repo) 


    

# mudar metodos para recvfrom e sendto
def send_file(connectionSocket,info):
    print(file_exists(info[1]))
    if file_exists(info[1]):
        file = open('./' + repo + '/' + info[1],'rb') 
        msg = 'Sending file...'
        connectionSocket.send(msg.encode())

        l = file.read(2048)

        while l:
            connectionSocket.send(l)
            l = file.read(2048)
        
        file.close()
    else:
        msg = 'File not found!!!'
        connectionSocket.send(msg.encode())
   
    connectionSocket.close()

def send_list_file(connectionSocket):
    
    separator = '\n'

    listFileArray = listdir('./' + repo)
    listFileString = separator.join(listFileArray)
    
    print(listFileString)
    connectionSocket.send(listFileString.encode())

    connectionSocket.close()

def hand_shake_server(serverSocket):
    data , infoClient = serverSocket.recvfrom(2048)

    packetReceived = packetDecode(data)
    
    packet = Packet(0, packetReceived['seq'] + 1)

    packetEncoded = packetEncode(packet)

    serverSocket.sendto(packetEncoded, infoClient )
       


# aqui tem que fazer com udp agora
def run_server():
    serverPort = 13000

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    serverSocket.bind((serverIp,serverPort))

    #serverSocket.listen(1)

    print('Server on port 13000...')

    while True:
        hand_shake_server(serverSocket)

       
        # info = data.decode().split(' ')
        # op = info[0]

        # if op == '1':
        #     send_file(connectionSocket,info)

        # elif op == '2':
        #     send_list_file(connectionSocket)
            
        # else:
        #     print('Operacao invalida')


def main():
    registerDnsSocket = make_socket_dns_connection()
    data, serverInfo = udp_dns_connection(registerDnsSocket)
    print(data.decode(), serverInfo)

    if data.decode() == 'Success':
        run_server()

    else:
        print(data.decode())


# use to start main function
if __name__ == '__main__':
    main()
        



