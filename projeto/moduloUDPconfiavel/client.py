from socket import *
import json
import pickle
from threading import Timer
import time

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
    dnsAddress = '127.0.1.1'
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



def send(socket,packetEncoded, serverInfo):

    while True:
        socket.settimeout(0.05)
        socket.sendto(packetEncoded, serverInfo)

        try:
            data, infoServer = socket.recvfrom(8096)
            
            return data, infoServer
        except timeout:
            print('Estouro do temporizador')


def hand_shake_client(clientSocket,serverIp):
    packet = packet_dict()
    
    packetEncoded = packetEncode(packet)

    data, infoServer = send(clientSocket,packetEncoded, (serverIp,13000))
   
   
    packetReceived = packetDecode(data)
    print(packetReceived['ack'])
    isConnected = packetReceived['ack'] == 0

    return isConnected, infoServer, packetReceived['ack']
       
   
def send_and_wait(clientSocket,serverInfo,ack,msg = None,data = None):
    packet = packet_dict(ack,data,msg)
    packetEncoded = packetEncode(packet)

    print('ack mandado = ', ack)

    data, infoServer = send(clientSocket,packetEncoded, serverInfo)
   
    
    packetReceived = packetDecode(data)

    if packetReceived['msg'] == 'FIN': return False, packetReceived,serverInfo,ack
    
    ack = (ack + 1) % 2

    isConnected = packetReceived['ack'] == ack

    while isConnected is False:
        isConnected, packetReceived, serverInfo,ack = send_and_wait(clientSocket, serverInfo, ack)
    

    return isConnected, packetReceived,serverInfo,ack
       


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
            clientSocket, infoServer = make_socket_tcp(serverIp)
            request_list_file(clientSocket)
        elif op == '3':
            clientSocket.close()
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

        isConnected, l, serverInfo,ack = send_and_wait(clientSocket,serverInfo,ack)
        l = l['data']
        
        while l:
            file.write(l)
            
            lAnt = l

            isConnected, l,serverInfo, ack = send_and_wait(clientSocket,serverInfo,ack)
            l = l['data']
        
        print(l)
        
        file.close()
        
        print('fechou o arquivo')
        clientSocket.close()


def request_file(clientSocket,infoServer,ack):
    op = '1 '
    fileName = input('Digite o nome do arquivo no formato nome.extensao: ')
    msg = op + fileName

    isConnected, packetReceived, serverInfo, ack = send_and_wait(clientSocket,infoServer,ack,msg)
    
    receive_file(clientSocket,fileName,packetReceived,infoServer)

def request_list_file(clientSocket):
    op = '2'

    clientSocket.send(op.encode())
    listFile = clientSocket.recv(2048)

    print('The server returned the following list:\n' + listFile.decode() + '\n')

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