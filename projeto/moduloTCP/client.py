from socket import *

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


def make_socket_tcp(serverIp):
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverIp,13000))

    return clientSocket

def close(clientSocket):
    msg = '3'
    clientSocket.send(msg.encode())

    clientSocket.close()

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
            clientSocket = make_socket_tcp(serverIp)
            close(clientSocket)
        else:
            print('Operacao invalida!!!\n')

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