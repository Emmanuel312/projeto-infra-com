from socket import *
import json
import pickle

class Packet:
    def __init__(self,seq,ack = None,data = None):
        self.seq = seq
        self.ack = ack
        self.data = data


def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    msg = input('Digite o hostname do server que voce quer se conectar: ')
    print(msg)
    hostName = 'C ' + msg
    # dns info
    dnsAddress = '127.0.0.1'
    dnsPort = 5300

    registerDnsSocket.sendto(hostName.encode(),(dnsAddress,dnsPort))
    data, dnsInfo = registerDnsSocket.recvfrom(2048)

    return data,dnsInfo

def hand_shake_client(clientSocket,serverIp):
    packet = Packet(0)
    
    packetJson = json.dumps(packet.__dict__)


    packetEncoded = pickle.dumps(packetJson)

    clientSocket.sendto(packetEncoded, (serverIp,13000))

    data, infoServer = clientSocket.recvfrom(2048)

    packetReceived = pickle.loads(data)
    packetReceived = json.loads(packetReceived) # json to dict

    return packetReceived['ack'] == packet.seq + 1
       
    

    



# mudar para socket udp
def make_socket_tcp(serverIp):
   
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    if hand_shake_client(clientSocket, serverIp):
        print('Success')
    else:
        print('Failed')
   



    return clientSocket

def send_socket_tcp(serverIp):
    while True:
        print('Escolha uma opcao\n 1 - Solicitar um arquivo\n 2 - Solicitar uma lista de arquivos disponıveis no repositorio\n 3 - Encerrar conexao\n')

        op = input()

        if op == '1':
            clientSocket = make_socket_tcp(serverIp)
            request_file(clientSocket)
            
        elif op == '2':
            clientSocket = make_socket_tcp(serverIp)
            request_list_file(clientSocket)
        elif op == '3':
            clientSocket.close()
            break
        else:
            print('Operacao invalida!!!\n')

# mudar para recvfrom
def receive_file(clientSocket,fileName):
    l = clientSocket.recv(2048)


    if l.decode() == 'File not found!!!':
        print(l.decode())
    else:
        print(l.decode())

        file = open('download_' + fileName,'wb')

        l = clientSocket.recv(2048)
        
        while l:
            file.write(l)
            l = clientSocket.recv(2048)
        
        file.close()
    
    clientSocket.close()

#mudar para sendto
def request_file(clientSocket):
    op = '1 '
    fileName = input('Digite o nome do arquivo no formato nome.extensao: ')
    msg = op + fileName

    clientSocket.send(msg.encode())

    receive_file(clientSocket,fileName)

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