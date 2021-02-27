import subprocess
import pip
import sys
import imp_pip
import pygame
import traceback
from ChessBoard import Board
#from network import Network
game_running = True
width = 750
height = 750
name = input("Please type your name: ")
wind = pygame.display.set_mode((width, height))
#wind = DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("Trying to install pygame")
    import pygame
except:
    print("Please install pygame if you want to play")
    try:
        print("Please wait while we try installing pygame")
        import pip
        install("pygame")
        print("Pygame installed successfully")

    except Exception as e:
        print("Seems like print ins't installed on the system' trying to install pip")
        imp_pip.main()
        print("Pip installed, trying to download pygame")
    try:
        import pip
        install("pygame")
        print("pygame has been successfully installed")
    except Exception as e:
        print(e)

import os
import pygame
import pickle
from GameClient import Network
import time
pygame.font.init()

board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))
rect = (113, 113, 525, 525)
t = "w"

import socket
import threading
import pyaudio

vcclient = None
n = None



def clean_up():
    global game_running, vcclient, n
    print("starting clean up")
    #close all threads
    #close all sockets
    #close all open files
    #make game_running false
    game_running = False
    if vcclient:
        vcclient.dele()
    if n:
        del n

    print("clean up finished")


class VCClient:
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.target_ip = "localhost"
            self.target_port = int(port)
            self.voicechat_running = True
            print(self.target_port)
            try:
                print("port is", type(self.target_port))
                print(self.target_port)
                self.s.connect((self.target_ip, self.target_port))
            except Exception as e:
                print(e)
                print(traceback.print_exc())
                print("we are stuck")


        except:
            print("Couldn't connect to server")
            print(traceback.print_exc())

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

        print("Connected to Server")

        # start threads
        self.recv_thread  = threading.Thread(target=self.receive_server_data)
        self.recv_thread.start()
        self.send_thread = threading.Thread(target=self.send_data_to_server)
        self.send_thread.start()
        print("voice chat is working")

    def receive_server_data(self):
        while self.voicechat_running:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while self.voicechat_running:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

    def dele(self):
        #self.s.shutdown()
        print("called")
        self.voicechat_running = False
      #  raise Exception(self.recv_thread)
        self.recv_thread.join()
       # self.send_thread.raise_exception()
        self.send_thread.join()
        self.s.close()
        self.playing_stream.close()
        self.recording_stream.close()
        #self.p.close()

        print("voice chat has shut down")





def menu(wind, name):
    global cBoard, chessbg, game_running

    offline = False

    while game_running:
        wind.blit(chessbg,(0,0))
        sFont = pygame.font.SysFont("comicsans", 50)
        bFont = pygame.font.SysFont("comicsans", 100)
        rep = bFont.render("VoiceChess",1,(255,100,30))
        wind.blit(rep,(width/2 - rep.get_width()/2,40))

        if offline:
            rep = sFont.render("The server is currenly offline, please try again later..", 1, (255, 0, 0))
            wind.blit(rep, (width/2 - rep.get_width()/2, 500))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                clean_up()

                exit(0)


            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    cBoard = connect()
                    run = False
                    main_logic()
                    break

                except Exception as e:
                    print("Server might be offline")
                    print(traceback.print_exc())
                    offline = True


def draw_game_window(wind, cBoard, p1, p2, color, isReady):
    wind.blit(board, (0,0))
    cBoard.draw(wind, color,color)


    formatTime1 = str(int(p1 // 60)) + ":" + str(int(p1 % 60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))

    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]
    font = pygame.font.SysFont("comicsans", 30)
    try:
        rep1 = font.render(cBoard.player1_name + r"\'s time: " + str(formatTime2) ,1 ,(255,255,255))
        rep2 = font.render(cBoard.player2_name + r"\'s time: "+ str(formatTime1),1, (255,255,255))
    except Exception as e:
        print(e)
        print(2)

    wind.blit(rep1 ,( 520,10))
    wind.blit(rep2 , (520, 700))
    rep = font.render(("Press q or close the window to quit"), 1, (255,255,255))
    wind.blit(rep, (10, 20))
    if color == "s":
        rep3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        wind.blit(rep3, (width / 2 - rep3.get_width() / 2, 10))

    if isReady == False:
        message = "Waiting for player"
        if color == "s":
            message = "Waiting for players!"
        font = pygame.font.SysFont("comicans", 80)
        rep = font.render(message, 1, (255, 0 ,0 ))
        wind.blit(rep,(width/2 - rep.get_width()/2,300))
    if color != "s":
        if color == "w":
            font = pygame.font.SysFont("comicsans", 30)
            rep = "You Are White!"
            show = font.render(rep, 1, (255, 0 ,0))
            wind.blit(show, (width/2 - show.get_width()/2, 10))
        elif color == "b":
            font = pygame.font.SysFont("comicsans", 30)
            rep = "You Are Black!"
            show = font.render(rep, 1, (255, 0 ,0))
            wind.blit(show,(width/2 - show.get_width()/2, 10))

        if cBoard.turn == color:
            cTime = time.time()

            rep = font.render("It Is Your turn, please proceed", 1, (255, 0 ,0))
            wind.blit(rep, (width/2 - rep.get_width() / 2, 700))
        else:
            cTime = time.time()
            rep = font.render("It Is their turn", 1, (255, 0, 0))
            wind.blit(rep, (width / 2 - rep.get_width() / 2, 700))
    pygame.display.update()


def end_screen(wind, txt):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    rep = font.render(txt, 1, (255, 0 ,0))
    wind.blit(rep, (width/2 - rep.get_width()/2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)
    display_end_screen = True
    while display_end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                #n.send("b won")
                #print("trying here")


                pygame.quit()
                display_end_screen = False

            elif event.type == pygame.KEYDOWN:
                display_end_screen = False
            elif event.type == pygame.USEREVENT:
                display_end_screen = False
    clean_up()
    exit(0)

"""this fuction will return a position on the board"""
def select(pos, player="w"):
     y = pos[1]
     x = pos[0]

     if rect[0] < x < rect[2] + rect[0]:
         if rect[1] < y < rect[1] + rect[3]:
             xx = x-rect[0]
             yy = y -rect[1]

             i = int(xx/ (rect[2] / 8))
             j = int(yy / (rect[3] / 8))
             if player == "b":
                 return (7-i, 7-j)
             return (i, j)
     else:
         return (-1,-1)
     """a (-1,-1) means that the position is not on the chess board"""

def connect():
    global n
    n = Network()
    return n.board




"""def game_event_handler(color):
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT and color !="s":
                # quit()
                if color == "w":
                    n.send("b won")
                    print("trying here")
                    #clean_up()
                elif color == "b":
                    n.send("w won")
                    print("trying here 2")
                clean_up()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    if color == "w":
                        n.send("b won")
                    elif color == "b":
                        n.send("w won")

                if event.key == pygame.K_RIGHT:
                     n.send("forward")

                if event.key == pygame.K_LEFT:
                     n.send("back")

            if event.type == pygame.MOUSEBUTTONDOWN and color != "s":
                if color == cBoard.turn and cBoard.is_full:
                    mouse_pos = pygame.mouse.get_pos()
                    n.send("update moves")
                    r, c = select(mouse_pos, color)
                    n.send("select " + str(r) + " " + str(c) + " " + color)
        time.sleep(0.1)
"""

def get_empty(board):
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:
                return (r,c)


ctr = 0
ctr2 = 0
def event_handler(color):
    global ctr,ctr2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if color == "w":
                n.send("b won")
            elif color == "b":
                n.send("w won")
            # quit()
            clean_up()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and color != "s":
                if color == "w":
                    n.send("b won")
                elif color == "b":
                    n.send("w won")

            if event.key == pygame.K_RIGHT:
                n.send("forward")

            if event.key == pygame.K_LEFT:
                n.send("back")

        if event.type == pygame.MOUSEBUTTONDOWN and color != "s":
            if color == cBoard.turn and cBoard.is_full:
                mouse_pos = pygame.mouse.get_pos()
                n.send("update moves")

                r, c = select(mouse_pos, color)
                print("is piece selected?", cBoard.piece_selected)
                if not cBoard.piece_selected:
                    print("piece selected/ ", cBoard.piece_selected)
                    if cBoard.board[c][r] != 0 and cBoard.board[c][r].color == color:
                        cBoard.piece_selected = True
                        n.send("select " + str(r) + " " + str(c) + " " + color)
                        print("sent")
                        print("piece selected2 is", cBoard.piece_selected)
                        n.send("piece")
                        ctr += 1
                elif ctr >0:
                    n.send("select " + str(r) + " " + str(c) + " " + color)
                    print("sent here")

                    #ctr2+=1
                    #ctr = 0
                    #ctr2 = 0

                    if cBoard.board[c][r] == 0 or (not type(cBoard.board[c][r]) == int and cBoard.board[c][r].color != color ):
                        n.send("has played")
                        ctr = 0




                #if not r not in range(8) or c not in range(8):
                 #   r,c = get_empty(cBoard.board)




data = None
def main_logic():
    global name, t, cBoard, vcclient, n, data
    color = cBoard.start_user
    ct = 0
    print(n)
    voicechat_port = n.send("vcport")
#    print(n.server)

    #vcclient = VCClient(voicechat_port) add back
    cBoard = n.send("update_moves")  # if doesnt work: try without the underscore

    cBoard = n.send("name " + name)

    clock = pygame.time.Clock()

    #threading.Thread(target=game_event_handler, args=(color)).start()
    n.send("ready")
    while game_running: # main loop
        event_handler(color)
        if cBoard.winner == color:
            if color =="w":
                end_screen(wind,"White won")
            elif color == "b":
                end_screen(wind,"Black Won")
            try:
                if pygame.event.get() == pygame.KEYDOWN and pygame.event.get().key == pygame.K_f:
                    #menu(wind,name)
                    menu(wind=wind, name=name)
                    n.disconnect()
                clean_up()
                #vcclient.dele()
            except:
                print(traceback.print_exc())
            #time.sleep(5)
            #menu(wind,name)
            n.disconnect()
            clean_up()

        if cBoard.winner is not None:
            break

        if color != "s":
            if cBoard.playingtime1 <= 0:
                cBoard = n.send("b won")
                break
            elif cBoard.playingtime2 <= 0:
                cBoard = n.send("w won")
                break



        ct += 1
        if ct % 5 == 0 and n:
            cBoard = n.send("update moves")
            ct = 0

        draw_game_window(wind, cBoard, cBoard.playingtime1, cBoard.playingtime2, color, cBoard.is_full)



        time.sleep(0.1)

      #data = n.recv(data)
    n.disconnect()



    if cBoard.winner == "w":
        end_screen(wind=wind, txt="White Won!")

    elif cBoard.winner == "b":
        end_screen(wind=wind, txt="Black Won!")



def main():
    width = 750
    height = 750
    pygame.display.set_caption("Chess Game")
    menu(wind=wind, name=name)



if __name__ == "__main__":
    main()

















