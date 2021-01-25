import socket
from threading import *
import threading
import time
import pickle
import traceback
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio

class Network(DatagramProtocol):
    def __init__(self):
        self.port = 8080
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.host = "localhost"
        self.add = (self.host, self.port)
        self.board = self.connect()
        self.board = pickle.loads(self.board)
        """
        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass
                """

    def connect(self):
        self.client.connect(self.add)
        return self.client.recv(4096 * 10)

    def disconnect(self):
        self.client.close()

    def send(self, send_data, should_pickle=False):
            cTime = time.time()
            info = None
            while time.time() - cTime < 5:
                if type(self.client) is not socket.socket:
                    continue
                print("send_data is ", send_data)

                if should_pickle:
                    send_data = pickle.dumps(send_data)
                elif type(send_data) is str:
                    send_data = send_data.encode()



                #send_data = pickle.dumps(send_data) if should_pickle else str(send_data).encode()
                try:
                    self.client.send(send_data)
                except Exception as e:

                    print(e)
                    print(traceback.print_exc())

                info = self.client.recv(4096 * 10)

                try:
                    info = pickle.loads(info)
                    break
                except Exception as e:
                    return info.decode()
                    print(e)
                    print(traceback.print_exc())

            return info

    def recv(self, data):
        try:
            data = self.client.recv(2048 * 2)
        except Exception as e:
            print("Error in game client ", e)
            exit()

        print(type(data))
        if type(data) is bytes or type(data) is bytearray:
            return data.decode()
        else:
            return pickle.loads(data)
