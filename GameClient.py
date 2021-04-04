import socket
from threading import *
import threading
import time
import pickle
import traceback
from twisted.internet.protocol import DatagramProtocol
from Cryptodome.Cipher import AES

from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
key = b'mysecretpassword'




import base64
import hashlib

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

    def Encrypt1(self, msg, key):
        iv = ""
        with open('iv.txt', 'rb') as c_file:
            iv = c_file.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        chiphertext = cipher.encrypt(pad(msg, AES.block_size))
        print(cipher.iv)
        print(chiphertext)
        return chiphertext

    def Decrypt1(self,ciphertext, key):
        iv = ""
        with open("iv.txt", 'rb') as c_file:
            iv = c_file.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = unpad(cipher.decrypt(ciphertext), AES.block_size)
        #print(msg)
        return msg

    def Encrypt(self, msg, key):
        crypt = bytearray()
        for ch in msg:
            chnum = ch  # - ord('a')
            chnum += key
            # chnum %= 26
            chnum %= 256
            crypt += (chnum).to_bytes(1, byteorder="big")  # + #ord('a'))
        return crypt

    def Decrypt(self, crypt, key):
        msg = bytearray()
        for ch in crypt:
            chnum = ch
            chnum -= key
            chnum %= 256
            msg += (chnum).to_bytes(1, byteorder="big")
        return msg

    def connect(self):
        self.client.connect(self.add)
        return self.Decrypt1(self.client.recv(4096 * 10),key)

    def disconnect(self):
        self.client.close()

    def send(self, send_data, should_pickle=False):
            cTime = time.time()
            info = None
            while time.time() - cTime < 5: # change back to <5
                if type(self.client) is not socket.socket:
                    continue
                print("send_data is ", send_data)

                if should_pickle:
                    send_data = pickle.dumps(send_data)
                elif type(send_data) is str:
                    send_data = send_data.encode()



                #send_data = pickle.dumps(send_data) if should_pickle else str(send_data).encode()
                try:
                    send_data = self.Encrypt1(send_data,key)
                    self.client.send(send_data)
                except Exception as e:

                    print(e)
                    print(traceback.print_exc())

                info = self.client.recv(4096 * 10)
                info = self.Decrypt1(info, key)
                try:
                    info = pickle.loads(info)
                    break
                except Exception as e:
                    return info.decode()
                    print(e)
                    print(traceback.print_exc())

            return info

    """def recv(self, data):
        try:
            data = self.client.recv(2048 * 2)
        except Exception as e:
            print("Error in game client ", e)
            exit()

        print(type(data))
        if type(data) is bytes or type(data) is bytearray:
            return data.decode()
        else:
            return pickle.loads(data)"""
