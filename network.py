import socket
import pickle
import traceback

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.100.102.42"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def receive(self):
        try:
            data = pickle.loads(self.client.recv(2048 * 2))
            return data
        except Exception as e:
            print(e)
            print("dude")
            print(traceback.print_exc())

    def connect(self):
        try:
            self.client.connect(self.addr)
            #return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print("n.send ",e)


    def __del__(self):
       # self.client.shutdown()
        self.client.close()

    def __str__(self):
        return f"port is {self.port}"


""" def send_raw(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv
        except Exception as e:
            print(e)"""
