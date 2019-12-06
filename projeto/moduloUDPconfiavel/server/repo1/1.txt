from socket import *

dnsServers = {}

def make_dnsServer():
    # server info
    dnsIp = '192.168.43.182'
    dnsPort = 5300 

    print('Ip do dns: ' + dnsIp)
    # create a udp server socket 
    dnsSocket = socket(AF_INET,SOCK_DGRAM)
    dnsSocket.bind((dnsIp,dnsPort))

    return dnsSocket, (dnsIp,dnsPort)

def register_to_dns(data):
    try:
        dnsServers[data[1]] = data[2]
        print(dnsServers)
        return 'Success'

    except:
        return 'Failed'


def translate_hostname_to_ip(hostname):
    return dnsServers[hostname]

def run_dns_server(dnsSocket, infoSocket ):
    while True:
        data, infoClient = dnsSocket.recvfrom(2048)
        dnsType = data.decode().split(' ')[0]

        if dnsType == 'R':
            msg = register_to_dns(data.decode().split(' '))
            dnsSocket.sendto(msg.encode(), infoClient )

        elif dnsType == 'C':
            hostname = data.decode().split(' ')[1]
            result = None

            if hostname in dnsServers:
                result = translate_hostname_to_ip(hostname)
            
            else:
                result = 'Not Found'
            
            dnsSocket.sendto(result.encode(), infoClient )


def main():
    dnsSocket, (dnsIp,dnsPort) = make_dnsServer()
    run_dns_server(dnsSocket,(dnsIp,dnsPort))
    
# use to start main function
if __name__ == '__main__':
    main()