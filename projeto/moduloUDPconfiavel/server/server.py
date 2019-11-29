from socket import *
from os import listdir
import pickle
import json

def packet_dict(ack = None,data = None,msg = None):
    packet = {}
    packet['msg'] = msg
    packet['ack'] = ack
    packet['data'] = data

    return packet


# nome do repositorio que contem os arquivos do servidor
repo = 'repo1'
serverIp = gethostbyname(gethostname())

def packetEncode(packet):
    packetEncoded = pickle.dumps(packet)

    return packetEncoded

def packetDecode(data):
    packetReceived = pickle.loads(data)
    
    return packetReceived


def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    info = 'R a ' + serverIp
    # dns info
    dnsAddress = '127.0.1.1'
    dnsPort = 5300

    registerDnsSocket.sendto(info.encode(), (dnsAddress,dnsPort))
    data, serverInfo = registerDnsSocket.recvfrom(2048)

    return data,serverInfo

def file_exists(requestedFile):
    return requestedFile in listdir('./' + repo) 


def send_and_await(serverSocket,packet,infoClient,ack):                             #ta certo
    packetEncoded = packetEncode(packet)
    while True:
        serverSocket.settimeout(0.05)
        serverSocket.sendto(packetEncoded,infoClient)

        try:
            serverSocket,dataDecoded,ack,infoClient = recv(serverSocket,ack)
            
            return ack
        except timeout:
            print('Estouro do temporizador')
    
    
    


# mudar metodos para recvfrom e sendto
def send_file(connectionSocket,info,ack,infoClient):
    if file_exists(info[1]):
        
        file = open('./' + repo + '/' + info[1],'rb') 
        msg = 'Sending file...'


        l = file.read(100)
        packet = packet_dict(ack,l,msg)
        ack = send_and_await(connectionSocket,packet,infoClient,ack)

        while l:
            l = file.read(100)
            if l:
                packet = packet_dict(ack,l,msg)
                ack = send_and_await(connectionSocket,packet,infoClient,ack)
        
        # implementa Fin
        packet = packetEncode(packet_dict(ack,l,'FIN'))
        connectionSocket.sendto(packet,infoClient)

        
        file.close()
        connectionSocket.close()
        print('fechou o arquivo')
    else:
        msg = 'File not found!!!'
        
    connectionSocket.close()

def send_list_file(connectionSocket):
    
    separator = '\n'

    listFileArray = listdir('./' + repo)
    listFileString = separator.join(listFileArray)
    
    connectionSocket.send(listFileString.encode())                                  #ta certo

    connectionSocket.close()

def hand_shake_server(serverSocket):
    ack = 0
    data , infoClient = serverSocket.recvfrom(2048)
    packetReceived = packetDecode(data)
    packet = packet_dict(ack)

    packetEncoded = packetEncode(packet)

    serverSocket.sendto(packetEncoded, infoClient )

    return serverSocket, ack

def recv(serverSocket, ack):
    data, infoClient = serverSocket.recvfrom(2048)
    
    dataDecoded = packetDecode(data)
    
    print('ack mandado = ', dataDecoded['ack'])


    if dataDecoded['ack'] == ack:
        ack = (ack + 1) % 2
        return serverSocket,dataDecoded,ack,infoClient
    else:
        #recv(serverSocket,ack)
        return serverSocket,dataDecoded,ack,infoClient


def run_server():
    serverPort = 13000


    
    while True:

        print('Server on port 13000...')


        serverSocket = socket(AF_INET,SOCK_DGRAM)
        serverSocket.bind((serverIp,serverPort))
    
        serverSocket, ack = hand_shake_server(serverSocket)

        serverSocket, dataDecoded, ack, infoClient = recv(serverSocket, ack)
        
        data = dataDecoded['msg']
        
        
        info = data.split(' ')
        op = info[0]

        if op == '1':
            send_file(serverSocket,info,ack,infoClient)

        # elif op == '2':
        #     send_list_file(connectionSocket)
            
        # else:
        #     print('Operacao invalida')


def main():
    registerDnsSocket = make_socket_dns_connection()
    data, serverInfo = udp_dns_connection(registerDnsSocket)


    if data.decode() == 'Success':
        run_server()

    else:
        print(data.decode())


# use to start main function
if __name__ == '__main__':
    main()
        



