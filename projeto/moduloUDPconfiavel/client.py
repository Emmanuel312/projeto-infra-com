from socket import *
import json
import pickle
from threading import Timer
import time


class Packet:
    def __init__(self,ack = None,data = None, msg = None):
        self.ack = ack
        self.data = data
        self.msg = msg

def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    msg = input('Digite o hostname do server que voce quer se conectar: ')
    print(msg)
    hostName = 'C ' + msg
    # dns info
    dnsAddress = '127.0.1.1'
    dnsPort = 5300

    registerDnsSocket.sendto(hostName.encode(),(dnsAddress,dnsPort))
    data, dnsInfo = registerDnsSocket.recvfrom(2048)

    return data,dnsInfo

def packetEncode(packet):
    print(type(packet))
    packetJson = json.dumps(packet.__dict__)
    print(packetJson)
    packetEncoded = pickle.dumps(packetJson)

    return packetEncoded

def packetDecode(data):
    packetReceived = pickle.loads(data)
    packetReceived = json.loads(packetReceived) # json to dict
    
    return packetReceived



def send(socket,packetEncoded, serverInfo):

    while True:
        socket.settimeout(2)
        socket.sendto(packetEncoded, serverInfo)

        try:
            data, infoServer = socket.recvfrom(2048)
            return data, infoServer
        except timeout:
            print('Estouro do temporizador')


def hand_shake_client(clientSocket,serverIp):
    packet = Packet()
    
    packetEncoded = packetEncode(packet)

    data, infoServer = send(clientSocket,packetEncoded, (serverIp,13000))
   
   
    packetReceived = packetDecode(data)

    isConnected = packetReceived['ack'] == 0

    return isConnected, infoServer, packetReceived['ack']
       
   
def send_and_wait(clientSocket,serverInfo,ack,msg = None,data = None):
    packet = Packet(ack,data,msg)
    packetEncoded = packetEncode(packet)

    data, infoServer = send(clientSocket,packetEncoded, serverInfo)
   
   
    packetReceived = packetDecode(data)

    isConnected = packetReceived['ack'] == ack

    while isConnected is False:
        isConnected, data, serverInfo = send_and_wait(clientSocket, serverInfo, ack)

    print('saiu do loop send and wait')

    return isConnected, data,serverInfo
       
    
    



# mudar para socket udp
def make_socket_tcp(serverIp):
   
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    isConnected, infoServer, ack = hand_shake_client(clientSocket, serverIp)

    while isConnected is False:
        isConnected, infoServer, ack = hand_shake_client(clientSocket, serverIp)

    print('saiu do loop')

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
def receive_file(clientSocket,fileName,data,serverInfo):
    l = data['data']
    msg = data['msg']
    ack = data['ack']


    if msg.decode() == 'File not found!!!':
        print(msg.decode())
    else:
        print(msg.decode())

        file = open('download_' + fileName,'wb')

        isConnected, l, ack = send_and_wait(clientSocket,serverInfo,ack)
        l = l['data']

        while l:
            file.write(l)
            isConnected, l, ack = send_and_wait(clientSocket,serverInfo,ack)
            l = l['data']
        
        file.close()
    
    clientSocket.close()

#mudar para sendto
def request_file(clientSocket,infoServer,ack):
    op = '1 '
    fileName = input('Digite o nome do arquivo no formato nome.extensao: ')
    msg = op + fileName



    data = send_and_wait(clientSocket,infoServer,ack,msg)

    receive_file(clientSocket,fileName,data,infoServer)

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