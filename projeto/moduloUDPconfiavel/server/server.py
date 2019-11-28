from socket import *
from os import listdir
import pickle
import json


class Packet:
    def __init__(self,ack = None,data = None, msg = None):
        self.ack = ack
        self.data = data
        self.msg = msg

# nome do repositorio que contem os arquivos do servidor
repo = 'repo1'
serverIp = gethostbyname(gethostname())

def packetEncode(packet):
    #print(packet)
    packet = Packet(0,None,"gay")
    packetJson = json.dumps(packet.__dict__)
    print(packetJson)
    packetEncoded = pickle.dumps(packetJson)

    return packetEncoded

def packetDecode(data):
    packetReceived = pickle.loads(data)
    packetReceived = json.loads(packetReceived) # json to dict
    
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
    serverSocket.sendto(packetEncoded,infoClient)
    
    serverSocket,dataDecoded,ack,infoClient = recv(serverSocket,ack)

    return ack

# mudar metodos para recvfrom e sendto
def send_file(connectionSocket,info,ack,infoClient):
    if file_exists(info[1]):
        print(info)
        file = open('./' + repo + '/' + info[1],'rb') 
        msg = 'Sending file...'


        l = file.read(2048)
        
        packet = Packet(ack,l,msg)
        ack = send_and_await(connectionSocket,packet,infoClient,ack)                #aqui ta certo
       

        while l:
            packet = Packet(ack,l,msg)
            ack = send_and_await(connectionSocket,packet,infoClient,ack)            #aqui ta certi
            l = file.read(2048)
        
        file.close()
    else:
        msg = 'File not found!!!'
        connectionSocket.send(msg)
   
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
    
    packet = Packet(ack)

    packetEncoded = packetEncode(packet)

    serverSocket.sendto(packetEncoded, infoClient )

    return serverSocket, ack

def recv(serverSocket, ack):
    data, infoClient = serverSocket.recvfrom(2048)
    
    dataDecoded = packetDecode(data)
    
    if dataDecoded['ack'] == ack:
        ack = (ack + 1) % 2
        return serverSocket,dataDecoded,ack,infoClient
    else:
        recv(serverSocket,ack)
    
        





def run_server():
    serverPort = 13000

    serverSocket = socket(AF_INET,SOCK_DGRAM)
    serverSocket.bind((serverIp,serverPort))

    #serverSocket.listen(1)

    print('Server on port 13000...')

    while True:
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
        



