from socket import *
import json
import pickle
from threading import Timer

class Packet:
    def __init__(self,seq,ack = None,data = None):
        self.seq = seq
        self.ack = ack
        self.data = data

clientSocket = socket(AF_INET,SOCK_DGRAM)

def packetEncode(packet):
    packetJson = json.dumps(packet.__dict__)
    packetEncoded = pickle.dumps(packetJson)

    return packetEncoded


packet = Packet(0, 2)

packetEncoded = packetEncode(packet)

clientSocket.sendto(packetEncoded,('127.0.1.1',4000))