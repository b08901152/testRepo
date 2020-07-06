import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.5"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(2048*1024))
       

    def send(self, data):
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(2048*1024))
       
