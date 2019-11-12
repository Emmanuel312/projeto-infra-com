from socket import *

def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    hostName = 'C sises.ufpe.br'
    # dns info
    dnsAddress = '127.0.0.1'
    dnsPort = 5300

    registerDnsSocket.sendto(hostName.encode(),(dnsAddress,dnsPort))
    data, dnsInfo = registerDnsSocket.recvfrom(2048)

    return data,dnsInfo

def make_and_send_socket_tcp(serverIp):
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverIp,13000))

    while True:
        print('Escolha uma opcao\n 1 - Solicitar um arquivo\n 2 - Solicitar uma lista de arquivos disponıveis no repositorio\n 3 - Encerrar conexao\n')

        op = int(input())

        if op == 1:
            request_file(clientSocket)
            break
        elif op == 2:
            
            break
        elif op == 3:
            clientSocket.close()
            break
        else:
            print('Operacao invalida!!!\n')

def receive_file(clientSocket,fileName):
    file = open(fileName + '_receive.pdf','wb')

    l = clientSocket.recv(2048)

    while l:
        file.write(l)
        l = clientSocket.recv(2048)
        
    file.close()
    clientSocket.close()

def request_file(clientSocket):
    op = '1 '
    fileName = input('Digite o nome do arquivo: ')
    msg = op + fileName

    clientSocket.send(msg.encode())

    receive_file(clientSocket,fileName)
   
def main():
    registerDnsSocket = make_socket_dns_connection()
    data, dnsInfo = udp_dns_connection(registerDnsSocket)

    
    if data.decode() == 'Not Found':
        print(data.decode())

    else:
        make_and_send_socket_tcp(data.decode())


if __name__ == "__main__":
    main()    