from socket import *
import json
import pickle
from threading import Timer
import time
from random import *

WAITING = 0

def packet_dict(ack = None,data = None,msg = None):
    packet = {}
    packet['msg'] = msg
    packet['ack'] = ack
    packet['data'] = data

    return packet

def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    msg = input('Digite o hostname do server que voce quer se conectar: ')
    
    hostName = 'C ' + msg
    # dns info
    dnsAddress = '192.168.43.182'
    dnsPort = 5300

    registerDnsSocket.sendto(hostName.encode(),(dnsAddress,dnsPort))
    data, dnsInfo = registerDnsSocket.recvfrom(2048)

    return data,dnsInfo

def packetEncode(packet):
    packetEncoded = pickle.dumps(packet)

    return packetEncoded

def packetDecode(data):
    packetReceived = pickle.loads(data)
    
    return packetReceived



def send(socket,packetEncoded, serverInfo, isHandShake = False):
    if isHandShake:
        while True:
            #socket.settimeout(0.05)
            socket.sendto(packetEncoded, serverInfo)

            try:
                data, infoServer = socket.recvfrom(8096)
                socket.settimeout(None)
                return data, infoServer
            except timeout:
                print('Estouro do temporizador')
    else:
        pacote = packetDecode(packetEncoded)
        #print('Cliente mandou ack = ', pacote['ack'])
        socket.sendto(packetEncoded, serverInfo)
        data, infoServer = socket.recvfrom(8096)
        p = packetDecode(data)
        #print('Cliente recebeu ack = ', p['ack'])

        return data, infoServer



def hand_shake_client(clientSocket,serverIp):
    global WAITING
    packet = packet_dict()
    
    packetEncoded = packetEncode(packet)

    data, infoServer = send(clientSocket,packetEncoded, (serverIp,13000), True)
   
   
    packetReceived = packetDecode(data)
    print(packetReceived['ack'])
    isConnected = packetReceived['ack'] == WAITING
    if isConnected:
        WAITING = (WAITING + 1) % 2
        print('Espera mudou para ', WAITING)

    return isConnected, infoServer, packetReceived['ack']
       
   
def send_and_wait(clientSocket,serverInfo,ack,msg = None,data = None):
    global WAITING
    packet = packet_dict(ack,data,msg)
    packetEncoded = packetEncode(packet)

    data, infoServer = send(clientSocket,packetEncoded, serverInfo)
   
    packetReceived = packetDecode(data)

    if packetReceived['msg'] == 'FIN': 
        print('FIN')
        WAITING = 0
        return False, packetReceived,serverInfo,ack, True
    
    isConnected = packetReceived['ack'] == WAITING

    if isConnected:
        WAITING = (WAITING + 1) % 2
        print('Espera mudou para ', WAITING)
  
    return isConnected, packetReceived,serverInfo,packetReceived['ack'], False

def fin(clientSocket,infoServer,ack):
    msg = '3'
    isConnected, packetReceived, serverInfo, ack, FIN = send_and_wait(clientSocket,infoServer,ack,msg)
    
    if FIN: 
        clientSocket.close()
    


def make_socket_tcp(serverIp):
   
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    isConnected, infoServer, ack = hand_shake_client(clientSocket, serverIp)

    while isConnected is False:
        isConnected, infoServer, ack = hand_shake_client(clientSocket, serverIp)


    return clientSocket, infoServer, ack

def send_socket_tcp(serverIp):
    while True:
        print('Escolha uma opcao\n 1 - Solicitar um arquivo\n 2 - Solicitar uma lista de arquivos disponıveis no repositorio\n 3 - Encerrar conexao\n')

        op = input()

        if op == '1':
            clientSocket, infoServer, ack = make_socket_tcp(serverIp)
            request_file(clientSocket,infoServer,ack)
            
        elif op == '2':
            clientSocket, infoServer,ack = make_socket_tcp(serverIp)
            request_list_file(clientSocket,infoServer,ack)
        elif op == '3':
            clientSocket, infoServer,ack = make_socket_tcp(serverIp)
            fin(clientSocket,infoServer,ack)
            break
        else:
            print('Operacao invalida!!!\n')

# mudar para recvfrom
def receive_file(clientSocket,fileName,packet,serverInfo):
    l = packet['data']
    msg = packet['msg']
    ack = packet['ack']

    if msg == 'File not found!!!':
        print(msg)
    else:
        file = open('download_' + fileName,'wb')
        file.write(l)

        isConnected, l, serverInfo, ack, FIN = send_and_wait(clientSocket,serverInfo,ack)
        l = l['data']
        
        while l:            
            if isConnected:
                file.write(l)

            isConnected, l, serverInfo, ack, FIN = send_and_wait(clientSocket,serverInfo,ack)
            if FIN:
                clientSocket.close()
                break   

            l = l['data']
        
        file.close()
        
        print('fechou o arquivo')
        clientSocket.close()


def request_file(clientSocket,infoServer,ack):
    op = '1 '
    fileName = input('Digite o nome do arquivo no formato nome.extensao: ')
    msg = op + fileName

    isConnected, packetReceived, serverInfo, ack, FIN = send_and_wait(clientSocket,infoServer,ack,msg)
    
    receive_file(clientSocket,fileName,packetReceived,serverInfo)

def receive_list_file(clientSocket,packet,serverInfo):
    l = packet['data']
    msg = packet['msg']
    ack = packet['ack']

    if msg == 'Empty List!!!':
        print(msg)
    else:
        num = randrange(100)
        file = open('list_file' + str(num) + '.txt','wb')
        file.write(l)

        isConnected, l, serverInfo, ack, FIN = send_and_wait(clientSocket,serverInfo,ack)
        l = l['data']
        
        while l:            
            if isConnected:
                file.write(l)

            isConnected, l, serverInfo, ack, FIN = send_and_wait(clientSocket,serverInfo,ack)
            if FIN :
                clientSocket.close()
                break   

            l = l['data']
        
        file.close()
        
        print('fechou o arquivo')
        clientSocket.close()




def request_list_file(clientSocket,infoServer,ack):
    op = '2'

    isConnected, packetReceived, serverInfo, ack, FIN = send_and_wait(clientSocket,infoServer,ack,op)

    receive_list_file(clientSocket,packetReceived,infoServer)

    clientSocket.close()

def main():
    registerDnsSocket = make_socket_dns_connection()
    data, dnsInfo = udp_dns_connection(registerDnsSocket)

    
    if data.decode() == 'Not Found':
        print(data.decode())

    else:
        print('Dns server returned: ' + data.decode())
        send_socket_tcp(data.decode())


if __name__ == "__main__":
    main()    