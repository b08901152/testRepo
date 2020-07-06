import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.20.10.4"
        self.port = 11111
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()

    def send(self, data):
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        

n= Network()
while True:
    string = input("please input: ")
    print(n.send(string))
    print(n.connect())
