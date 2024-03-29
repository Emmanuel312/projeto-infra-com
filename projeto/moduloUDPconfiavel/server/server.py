from socket import *
from os import listdir
import pickle
import json
import time

WAITING = 0

def packet_dict(ack = None,data = None,msg = None):
    packet = {}
    packet['msg'] = msg
    packet['ack'] = ack
    packet['data'] = data

    return packet


# nome do repositorio que contem os arquivos do servidor
repo = 'repo1'
serverIp = '192.168.43.182'

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
    dnsAddress = '192.168.43.182'
    dnsPort = 5300

    registerDnsSocket.sendto(info.encode(), (dnsAddress,dnsPort))
    data, serverInfo = registerDnsSocket.recvfrom(2048)

    return data,serverInfo

def file_exists(requestedFile):
    return requestedFile in listdir('./' + repo) 


def send_and_await(serverSocket,packet,infoClient,ack):                             #ta certo
    packetEncoded = packetEncode(packet)
    while True:
        serverSocket.settimeout(0.1)
        
        
        print('Servidor mandou ack = ', packet['ack'])
        serverSocket.sendto(packetEncoded,infoClient)

        try:
            serverSocket,dataDecoded,ack,infoClient, isAck = recv(serverSocket,ack)
            serverSocket.settimeout(None)
            if isAck :
                break

            
        except timeout:
            print('Estouro do temporizador!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    
    return ack

def fin(serverSocket,ack,infoClient):
    msg = 'FIN'
    packetEncoded = packetEncode(packet_dict(ack,None,msg))
        
    serverSocket.sendto(packetEncoded,infoClient)
    
    serverSocket.close()
    

# mudar metodos para recvfrom e sendto
def send_file(connectionSocket,info,ack,infoClient):
    global WAITING
    if file_exists(info[1]):
        
        file = open('./' + repo + '/' + info[1],'rb') 
        msg = 'Sending file...'

        l = file.read(2048)

        packet = packet_dict(ack,l,msg)
        ack = send_and_await(connectionSocket,packet,infoClient,ack)

        while l:
            l = file.read(2048)
            if l:
                packet = packet_dict(ack,l,msg)
                ack = send_and_await(connectionSocket,packet,infoClient,ack)
        
        # implementa Fin
        packet = packetEncode(packet_dict(ack,l,'FIN'))
        WAITING = 0
        connectionSocket.sendto(packet,infoClient)

        
        file.close()
        connectionSocket.close()
        print('fechou o arquivo')
    else:
        msg = 'File not found!!!'
        
    connectionSocket.close()

def send_list_file(serverSocket,ack,infoClient):
    
    separator = '\n'

    listFileArray = listdir('./' + repo)

    if len(listFileArray) > 0:
        listFileString = separator.join(listFileArray)
        
        file = open('list_file.txt','w')

        file.write(listFileString)
        file = open('list_file.txt','rb')
        msg = 'Sending file...'

        l = file.read(1)

        packet = packet_dict(ack,l,msg)
        ack = send_and_await(serverSocket,packet,infoClient,ack)

        while l:
            l = file.read(1)
            if l:
                packet = packet_dict(ack,l,msg)
                ack = send_and_await(serverSocket,packet,infoClient,ack)
        
        # implementa Fin
        packet = packetEncode(packet_dict(ack,l,'FIN'))
        WAITING = 0
        serverSocket.sendto(packet,infoClient)

        
        file.close()
        serverSocket.close()
        print('fechou o arquivo')
    else:
        msg = 'Empty List!!!'

def hand_shake_server(serverSocket):
    ack = 0
    while True:
        data , infoClient = serverSocket.recvfrom(2048)
        if packetDecode(data)['ack'] is None: break

    print('sai do while')
   
    packetReceived = packetDecode(data)
    print(packetReceived)
    packet = packet_dict(ack)

    packetEncoded = packetEncode(packet)

    print(packet)
    
    
    serverSocket.sendto(packetEncoded, infoClient)

    return serverSocket, ack

def recv(serverSocket, ack):
    global WAITING
    while True:
        data , infoClient = serverSocket.recvfrom(2048)
        if packetDecode(data)['ack'] is not None: break
   

    dataDecoded = packetDecode(data)
    print('Servidor recebeu ack = ', dataDecoded['ack'])

    isAck = dataDecoded['ack'] == WAITING

    if isAck:
        WAITING = (ack + 1) % 2
        ack = (ack + 1) % 2

    return serverSocket,dataDecoded,ack,infoClient, isAck


def run_server():
    serverPort = 13000


    
    while True:

        print('Server on port 13000...')

        serverSocket = socket(AF_INET,SOCK_DGRAM)
        serverSocket.bind((serverIp,serverPort))
    
        serverSocket, ack = hand_shake_server(serverSocket)

        serverSocket, dataDecoded, ack, infoClient, isAck = recv(serverSocket, ack)
        

        data = dataDecoded['msg']
        
        info = data.split(' ')
        op = info[0]

        if op == '1':
            send_file(serverSocket,info,ack,infoClient)

        elif op == '2':
            send_list_file(serverSocket,ack,infoClient)

        elif op == '3':
            print('chegou aqui')
            fin(serverSocket,ack,infoClient)


        else:
            print('Operacao invalida')


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
        



