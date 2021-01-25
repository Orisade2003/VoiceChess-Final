import socket
from _thread import *
import time
import pickle
from ChessBoard import Board
from network import *
import traceback
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


room_dict = {0:Board(8, 8)}

spec_ctr = 0
specs= []
conn_ctr = 0
vcslist=[]


def times_in_dictlist(l, room):
    c=0
    for d in l:
        if d["room"] == room:
            c+=1
    return c == 2 or c == 0
def make_connection(con, game_num, isSpec = False):
    voicechat_port = "8081"
    vcrequest_flag = False
    name = ""
    global conn_ctr, room_dict, spec_ctr, pos, currentId, color
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
        print(color)
        serilNum = pickle.dumps(cBoard)

        if color == "b":
            cBoard.is_full = True
            cBoard.startTime = time.time()

        con.send(serilNum)
        con.send(str(8081).encode())
        voice_chat_ack = con.recv(1024).decode()
        if voice_chat_ack != "ok":
            #to do
            pass

        conn_ctr += 1
        isRunning = True
        while isRunning:
            if game_num not in room_dict:
                break
            try:
                info = con.recv(8192 * 4)
                check = info
                info = info.decode("utf-8")

                if not check:
                    break
                else:
                    if info.count("select") > 0:
                        data = info.split(" ")
                        print(data)
                        col = int(data[1])
                        row = int(data[2])
                        color = data[3]
                        cBoard.piece_select(col, row, color)
                        print(col,row,color)
                        print(cBoard.board)
                    if info == "b won":
                        cBoard.winner = "b"
                        print("black won")
                    if info =="w won":
                        cBoard.winner = "w"
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

                        # print("herehere")
                        # if times_in_dictlist(conn_list, room):
                        # vcs = threading.Thread(target=VCServer, args=(voicechat_port))
                        # vcslist.append(vcs)
                        # vcslist[-1].start()
                        # temp_port = int(voicechat_port)
                        # voicechat_port =str(temp_port+1)
                        # print("The port here is type", type(voicechat_port))

                    srl = pickle.dumps(voicechat_port)
                    con.sendall(srl)
                    # go over conlist and


                            #voicechat_port = c[]
                    vcrequest_flag = False
                else:
                    con.sendall(all_data)


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



                """ for c in conn_list:
                    if c["room"] == con_room:
                        c["con"].sendall("you won".encode())
                        print("you won sent")"""






                break


            except Exception as e:
                print(traceback.format_exc())
                print(3)
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
        con.send(send_data)
        while True:
            av_games = list(room_dict.keys())
            cBoard = room_dict[av_games[spec_ind]]
            try:
                d = con.recv(256)
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
                    con.sendall(sendData)

            except Exception as e:
                print(e)
                print(traceback.print_exc())
    print("Spectator has disconnected from the server", game_num)
    spec_ctr -= 1
    con.close()

"""def broadcast(self, sock, data):
    for client in self.connections:
        if client != self.s and client != sock:
            try:
                client.send(data)
            except:
                pass"""






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
       # self.server = Server((p1,p2))
    def __str__(self):
        s = "These are the players in the room" + (self.p1,self.p2)







class VCServer:
    def __init__(self, port):
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
        self.s.listen(100)

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:

            c, addr = self.s.accept()
            print("connection request by", addr)
            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
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
                print("erorrrr")
                print(traceback.print_exc())
                break







Rooms=[]
conn_list =[]
temp = []
uid_counter = 0
FIRST_VC_PORT= 8081
VCSERVER_LIST = [VCServer(port) for port in range(FIRST_VC_PORT,FIRST_VC_PORT + MAX_ROOMS )]

#start_new_thread(VCServer, (8081,))
while True:
    try:
        #spec_read()

        if conn_ctr < MAX_ROOMS:
            (con,addr) = s.accept()
            conn_list.append({"id": uid_counter, "con": con, "addr": addr, "room": -1, "color": None})
            uid_counter += 1
            #player = (con,addr)
            #temp = temp.append(player)
            """if type(temp) is list:
               if len(temp) % 2 == 0:
                    r = Room((temp[0]),(temp[1]))
                    server = Server((temp[0],temp[1]))
                    Rooms.append(r)
                    temp = []
                    print("THESE ARE THE CURRENNT ROOMS", Rooms)
            """
            #is_spec = False
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
            #conn_list[-1]["color"]


        print("There are: " + str(conn_ctr + 1) + " current connections")
        print("There are: " + str(len(room_dict)) + "current games going on")
        start_new_thread(make_connection, (con, first_available_room, False))
        #start_new_thread(Server)




    except Exception as e:
        print(e)
        print(traceback.print_exc())



















