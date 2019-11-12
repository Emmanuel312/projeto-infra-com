from socket import *


def make_socket_dns_connection():
    registerDnsSocket = socket(AF_INET,SOCK_DGRAM)

    return registerDnsSocket

def udp_dns_connection(registerDnsSocket):
    info = 'R sises.ufpe.br 127.0.0.1'
    # dns info
    dnsAddress = '127.0.0.1'
    dnsPort = 5300

    registerDnsSocket.sendto(info.encode(), (dnsAddress,dnsPort))
    data, serverInfo = registerDnsSocket.recvfrom(2048)

    return data,serverInfo

def send_file(connectionSocket,info):
    file = open(info[1] +'.pdf','rb') 

    l = file.read(2048)

    while l:
        connectionSocket.send(l)
        l = file.read(2048)
    
    file.close()
    connectionSocket.close()

def run_server():
    serverAddress = '127.0.0.1'
    serverPort = 13000

    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind((serverAddress,serverPort))

    serverSocket.listen(1)

    print('Server on port 13000...')

    while True:
        connectionSocket, clientInfo = serverSocket.accept()
        data = connectionSocket.recv(2048)


        print(data.decode())
        info = data.decode().split(' ')
        op = info[0]

        if op == '1':
            send_file(connectionSocket,info)

        elif op == '2':
            pass
        else:
            print('Operacao invalida')


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
        



