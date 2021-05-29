import socket
from _thread import *
import time
import pickle
from ChessBoard import Board
from network import *
import traceback
import mysql.connector
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome import Random
from Cryptodome.Util.Padding import unpad
key = b'mysecretpassword'

import threading
server = "0.0.0.0"
port = 8080
MAX_ROOMS = 6
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (server, port)
serverip = socket.gethostbyname(server)
try:
    s.bind(server_address)
except Exception as e:
    print(e)
    print(traceback.format_exc())

s.listen()
print("Server in now online, and waiting for a client connection")
col1 = 0
row1 = 0
prev_piece = None

room_dict = {0:Board(8, 8)}

spec_ctr = 0
specs= []
conn_ctr = 0
vcslist=[]




def Encrypt1(msg, key):
    """

    :param msg: the message to encrypt, string
    :param key: the encryption key, bytes object
    :return: the function returns the encrypted msg asa a bytes object
    """
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    ciphertext = cipher.encrypt(pad(msg,AES.block_size))
    return iv + ciphertext

def Decrypt1(ciphertext, key):
    """

    :param ciphertext:encrypted msg, bytes
    :param key: thhe encryption key, bytes
    :return:  the function returns the decrypted msg , string
    """
    iv = ciphertext[:16]
    ciphertext= ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return msg



def Encrypt(msg, key):
    crypt = bytearray()
    for ch in msg:
        chnum = ch  # - ord('a')
        chnum += key
        chnum %= 256
        crypt += chnum.to_bytes(1, byteorder="big")  # + #ord('a'))
    return crypt


def Decrypt(crypt, key):
    msg = bytearray()
    for ch in crypt:
        chnum = ch
        chnum -= key
        chnum %= 256
        msg += chnum.to_bytes(1, byteorder="big")
    return msg

def add_winner(winner):
    """

    :param winner: the name of the winner of the chess game
    :return: the function adds a win to wins counter of the winner in the database
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="io.pngxxwp7673G",
        database="voicechessusersdb")
    mycursor = mydb.cursor()
    sql = "Update Users Set Wins = Wins + 1 WHERE Username = %s"
    val = (winner,)
    mycursor.execute(sql, val)
    mydb.commit()



    #UPDATE Users SET Wins = Wins + 1 WHERE

def game_count(player1, player2):
    """
    :param player1: the name of one of the players
    :param player2: the name of the other player
    the function adds 1 to the Games column in data base for each  one of the two players
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="io.pngxxwp7673G",
        database="voicechessusersdb")
    mycursor = mydb.cursor()
    sql = "Update Users Set Games = Games + 1 WHERE Username = %s"
    val = (player1,)
    mycursor.execute(sql, val)
    mydb.commit()
    val =(player2,)
    mycursor.execute(sql,val)
    mydb.commit()


def SendData(con, msg):
    """

    :param con: socket
    :param msg: message to send, string
    the function encrypts msg and sends it to the socket
    """
    con.sendall(Encrypt1(msg,key))

def RecvData(con, size):
    """

    :param con: socket
    :param size: size of message to receive from the client
    :return: the decrypted message received from the client as a string
    """
    data = con.recv(size)
    try:
        data = Decrypt1(data,key)
    except:
        print("this is the data", data)
    return data


def times_in_dictlist(l, room):
    """

    :param l: dictionary of players
    :param room: room number, int
    :return: returns true if the dictionary has 0 or 2 instances of player with room number l
    """
    c=0
    for d in l:
        if d["room"] == room:
            c+=1
    return c == 2 or c == 0
def make_connection(con, game_num, isSpec = False):
    """

    :param con: client socket
    :param game_num: int, game number
    :param isSpec: boolean, whether the client is a player or a spectator
    this function is in charge of the communication with the client, answers the clients' requests , and calls other functions to make necessary changes to the board
    """
    voicechat_port = "8081"
    vcrequest_flag = False
    name = ""
    global conn_ctr, room_dict, spec_ctr, pos, currentId, color, col1, row1, prev_piece
    if isSpec == False:
        name = None
        try:
            cBoard = room_dict[game_num]
        except:
            print("game num not in c_games")

        if conn_ctr % 2 == 0:
            color = "w"
        else:
            color = "b"
        cBoard.start_user = color
        serilNum = pickle.dumps(cBoard)

        if color == "b":
            cBoard.is_full = True
            cBoard.startTime = time.time() #time since Jan 1st 1970


        SendData(con,serilNum)

        room = -1
        for c in conn_list:
            if c["con"] == con:
                room = c["room"]
                if room != -1:
                    voicechat_port = FIRST_VC_PORT + room
                    if voicechat_port != 8081:
                        voicechat_port-=1
                    print("new voice room")
        SendData(con,str(voicechat_port).encode())
        voice_chat_ack = RecvData(con, 1024).decode()

        if voice_chat_ack != "ok":

            pass

        conn_ctr += 1
        isRunning = True
        while isRunning:
            if game_num not in room_dict:
                break
            try:

                info = RecvData(con, 8192 * 4)
                check = info
                info = info.decode("utf-8")

                if not check:
                    break
                else:
                    if info.count("move_piece") > 0:
                        data = info.split(" ")
                        print(data)
                        color = data[1]
                        current_row = int(data[2])
                        current_col = int(data[3])

                        new_row = int(data[4])
                        new_col = int(data[5])

                        if color != cBoard.turn:
                            continue

                        start = (current_row, current_col)
                        end = (new_row, new_col)
                        print("current row and col:", cBoard.board[current_row][current_col])
                        if not cBoard.move(start, end, color):
                            continue

                        opp_color = "b" if color == "w" else "w"

                        if cBoard.checkmate3(opp_color):
                            cBoard.winner = color
                            winner = cBoard.winner
                            if winner == "w":
                                add_winner(cBoard.player1_name)
                                game_count(cBoard.player1_name, cBoard.player2_name)
                            elif winner == "b":
                                add_winner(cBoard.player2_name)
                                game_count(cBoard.player1_name, cBoard.player2_name)


                        else:
                            cBoard.turn = opp_color





                    if info.count("select") > 0:
                        data = info.split(" ")
                        print(data)
                        col = int(data[1])
                        row = int(data[2])
                        color = data[3]
                        print("this is rowcol", row,col)
                        cBoard.piece_select(col, row, color)
                    if info == "b won":
                        cBoard.winner = "b"
                        print("black won")
                        add_winner(cBoard.player2_name)
                        game_count(cBoard.player1_name, cBoard.player2_name)
                    if info =="w won":
                        cBoard.winner = "w"
                        add_winner(cBoard.player1_name)
                        game_count(cBoard.player1_name, cBoard.player2_name)
                        print("white won")
                    if info == "vcport":
                        vcrequest_flag = True






                    if info.count("name") == 1:
                        name = info.split(" ")[1]
                        if color == "b":
                            cBoard.player2_name = name
                        elif color == "w":
                            cBoard.player1_name = name

                    if info == "update moves":
                        try:
                            cBoard.get_all_moves()
                        except Exception as e:
                            print(e)
                            print(traceback.print_exc())
                    if info == "piece":
                        cBoard.piece_selected = cBoard.board[col][row]

                    if info == "has played":
                        cBoard.piece_selected = None

                    if cBoard.is_full:
                        if cBoard.turn == "w":
                            cBoard.playingtime1 = 900 - (time.time() - cBoard.startTime) - cBoard.time_stored1
                        else:
                            cBoard.playingtime2 = 900 - (time.time() - cBoard.startTime) - cBoard.time_stored2

                    all_data = pickle.dumps(cBoard)



                if vcrequest_flag:
                    for c in conn_list:
                        if c["con"] == con:
                            room = c["room"]
                            if room != -1:
                                voicechat_port = FIRST_VC_PORT + room


                    srl = pickle.dumps(voicechat_port)
                    SendData(con, srl)




                    vcrequest_flag = False
                else:
                    SendData(con, all_data)


            except ConnectionResetError:
                print(f"Connection Was Reset {con}")
                con_room = 0
                for c in conn_list:
                    if c["con"] == con:
                        con_room = c["room"]
                        conn_list.remove(c)
                        break
                con.close()

                room_dict[con_room].winner = "w"








                break


            except Exception as e:
                print(traceback.format_exc())

        conn_ctr -= 1
        try:
            del room_dict[game_num]
            print("game " + game_num +" has ended")
        except:
            pass
        print("player",name , "left the game")
        con.close()


    else:
        av_games = list(room_dict.keys())
        spec_ind = 0
        cBoard = room_dict[av_games[spec_ind]]
        cBoard.start_user = "s"
        send_data = pickle.dumps(cBoard)
        SendData(con, send_data)
        while True:
            av_games = list(room_dict.keys())
            cBoard = room_dict[av_games[spec_ind]]
            try:
                d = RecvData(con,256)
                data_received = d.decode("utf-8")

                if not d:
                    break
                else:
                    try:
                        if data_received == "back":
                            spec_ind -= 1
                            if spec_ind < 0:
                                spec_ind = len(av_games) - 1
                        elif data_received == "forward":
                            spec_ind += 1
                            if spec_ind >= len(av_games):
                                spec_ind = 0
                        cBoard = room_dict[av_games[spec_ind]]
                    except Exception as e:
                        print(e)
                        print(traceback.print_exc())
                    sendData = pickle.dumps(cBoard)
                    SendData(con, sendData)

            except Exception as e:
                print(e)
                print(traceback.print_exc())
    print("Spectator has disconnected from the server", game_num)
    spec_ctr -= 1
    con.close()


def spec_read():
    global specs

    specs= []
    try:
        with open("specs.txt","r") as f:
            for l in f:
                specs.append(l.strip)
    except:
        print("File Not Found")
        open("specs.txt","w")


class Room:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        s = "These are the players in the room" + (self.p1,self.p2)






# this class is incharge of handling the voice chats on the server side
class VCServer:
    def __init__(self, port):
        """
        :param port: the port which thee server connects to
        this function initializes the voice chat server
        """
        self.ip = "0.0.0.0"
        while 1:
            try:
                self.port = port

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))

                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        t = threading.Thread(target=self.accept_connections)
        t.start()

    def accept_connections(self):
        """
        this function accepts client' connection requests
        """
        self.s.listen(100)

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:

            c, addr = self.s.accept()
            print("connection request by", addr)
            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, sock, data):
        """
        :param sock: client socket
        :param data: the data which needs to be sent to the client, bytes
        the function sends the data to the client
        """
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        """
        :param c: socket
        :param addr: ip address of the client
        the function is in charge of handling the clients' connection
        """
        while True:
            try:
                    data = c.recv(1024)
                    x = threading.Thread(target=self.broadcast, args=(c,data)).start()

            except (ConnectionResetError, ConnectionAbortedError):
                c.close()
                self.connections.remove(c)
                print(f"socket {c} was closed due to connection reset")



                break

            except socket.error:
                c.close()
                print(traceback.print_exc())
                break







Rooms=[]
conn_list =[]
temp = []
uid_counter = 0
FIRST_VC_PORT= 8081
try:
    VCSERVER_LIST = [VCServer(port) for port in range(FIRST_VC_PORT,FIRST_VC_PORT + MAX_ROOMS )]
except:
    print(traceback.print_exc())


while True:
    try:


        if conn_ctr < MAX_ROOMS:
            (con,addr) = s.accept()
            conn_list.append({"id": uid_counter, "con": con, "addr": addr, "room": -1, "color": None})
            uid_counter += 1


            first_available_room = -1
            print("New connection made")

            room_keys_list = room_dict.keys()
            for index, game in room_dict.items():
                if not game.is_full:
                    first_available_room = index
                    break
            else:
                first_available_room = len(room_dict.keys())
                room_dict[first_available_room] = Board(8, 8)
            conn_list[-1]["room"] = first_available_room



        print("There are: " + str(conn_ctr + 1) + " current connections")
        print("There are: " + str(len(room_dict)) + "current games going on")
        start_new_thread(make_connection, (con, first_available_room, False))





    except Exception as e:
        print(e)
        print(traceback.print_exc())



















