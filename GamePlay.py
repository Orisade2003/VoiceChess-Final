import subprocess
import pip
import sys
import imp_pip
import traceback
from ChessBoard import Board
import Globals
import argparse
import os
import pygame
import pickle
from GameClient import Network
import sys
import time

import socket
import threading
import pyaudio


game_running = True
width = 750
height = 750
board = None
chessbg = None
t = ""
rect = None
name = ""
#name = input("Please type your name: ")
wind = None


#this function initializes the pygame window
def init_window():
    global wind
    wind = pygame.display.set_mode((width, height))
#wind = DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

#this function installs pip for the user
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

#this function checks if the user has pygame installed, and if he doesn't it installs it for the user
def install_requirements():
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


#this function initializes the board drawing
def init_board():
    global board, chessbg, rect, t
    pygame.font.init()
    board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
    chessbg = pygame.image.load(os.path.join("img", "ChessKingBG2.png")) #"chessbg.png"
    rect = (113, 113, 525, 525)
    t = "w"



vcclient = None
n = None


#this function ends the game, and disconnects the voicechat client from the server
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


#this is the class for the voice chat client
class VCClient:

    def __init__(self, port):
        """
        :param port: string, the port that the function uses to connect to the server
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.target_ip = "127.0.0.1" #was 10.100.102.6
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
        """
        this function receives data from the server as bytes' and decodes to audio
        """
        while self.voicechat_running:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        """
        this function sends audio as bytes to the server, so it is sent to the other player
        """
        while self.voicechat_running:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

    def dele(self):
        """
        deletes the instance of the object
        """
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
    """

    :param wind: pygame window
    :param name: player name - string
    this function is in charge of setting up the menu screen before the game starts
    """
    global cBoard, chessbg, game_running

    offline = False

    while game_running:
        wind.blit(chessbg,(0,0))
        sFont = pygame.font.SysFont("comicsans", 50)
        bFont = pygame.font.SysFont("comicsans", 100)
        rep = bFont.render("VoiceChess",1,(255,100,30))
        wind.blit(rep,(width/2 - rep.get_width()/2,40))

        if offline:
            rep = sFont.render("Check Your Connection ", 1, (255, 0, 0))
            wind.blit(rep, (width/2 - rep.get_width()/2, 500))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clean_up()
                pygame.quit() ##remove display maybe

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
    """

    :param wind: pygame window
    :param cBoard: instance of Board class, this board represents the board in th game
    :param p1:
    :param p2:
    :param color: the color of the player, string
    :param isReady:bool, true if 2 players are in the room and false otherwise
    the function is in charge of drawing the backbone of the board screen drawing the text and the time/
    """
    wind.blit(board, (0,0))
    cBoard.draw(wind, color,color, Globals.selected)


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
            wind.blit(show, (width/2 - show.get_width()/2 + 50 , 10)) #remove plus 100
        elif color == "b":
            font = pygame.font.SysFont("comicsans", 30)
            rep = "You Are Black!"
            show = font.render(rep, 1, (255, 0 ,0))
            wind.blit(show,(width/2 - show.get_width()/2 + 50, 10))

        if cBoard.turn == color:
            cTime = time.time()

            rep = font.render("It Is Your turn, please proceed", 1, (255, 0 ,0))
            wind.blit(rep, (width/2 - rep.get_width() / 2 - 40,  700))
        else:
            cTime = time.time()
            rep = font.render("It Is their turn", 1, (255, 0, 0))
            wind.blit(rep, (width / 2 - rep.get_width() / 2, 700))
    pygame.display.update()


def end_screen(wind, txt):
    """

    :param wind: pygame window
    :param txt: text to display, string
    the function draws txt on the middle of the window
    """
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
     """

     :param pos: mouse position, tuple
     :param player: string, color of the player
     :return: the function turns the mouse position into a tuple which represents a position on the board.
     """
     y = pos[1]
     x = pos[0]

     if rect[0] < x < rect[2] + rect[0]:
         if rect[1] < y < rect[1] + rect[3]:
             xx = x-rect[0]
             yy = y -rect[1]

             c = int(xx/ (rect[2] / 8))
             r = int(yy / (rect[3] / 8))
             if player == "b":
                 return (7-r, 7-c)
             return (r, c)
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
    """

    :param board: 2 dimensional list, which contains the different pieces on the board
    :return: returns the first empty position on the board as a tuple
    """
    for r in range(8):
        for c in range(8):
            if board[r][c] == 0:
                return (r,c)


ctr = 0
ctr2 = 0
selected = None
def event_handler(color):
    """

    :param color: string, color of the player
    the function is in charge of handling all the different events that can occur during the game
    """
    global ctr,ctr2, selected
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
                if (cBoard.board[r][c] != 0) and (cBoard.board[r][c].color == color):
                    Globals.selected = cBoard.board[r][c]

                else:
                    if Globals.selected:
                        if (c,r) in Globals.selected.moves:

                            n.send(f"move_piece {color} {str(Globals.selected.row)} {str(Globals.selected.col)} {str(r)} {str(c)}")
                            Globals.selected = None
                            #n.send("select " + str(selected.row) + " " + str(selected.col) + " " + color)
                            #n.send("select " + str(r) + " " + str(c) + " " + color)

                """print("is piece selected?", cBoard.piece_selected)
                if not cBoard.piece_selected:
                    print("piece selected/ ", cBoard.piece_selected)
                    if cBoard.board[c][r] != 0 and cBoard.board[c][r].color == color:
                        
                        cBoard.piece_selected = cBoard.board[c][r]
                        n.send("select " + str(r) + " " + str(c) + " " + color)
                        print("sent")
                        print("piece selected2 is", cBoard.piece_selected)
                        n.send("piece")
                        ctr += 1
                elif ctr >0:
                    print("sent here")
                    #ctr2+=1
                    #ctr = 0
                    #ctr2 = 0

                    in_moves = (c,r) in cBoard.piece_selected.moves
                    if (in_moves) or ( cBoard.board[c][r] != 0 and cBoard.board[c][r].color == color):
                        n.send("select " + str(r) + " " + str(c) + " " + color)
                        if in_moves:
                            n.send("has played")
                        else:
                            n.send("piece")
                            




                    ctr = 0

"""


                #if not r not in range(8) or c not in range(8):
                 #   r,c = get_empty(cBoard.board)




data = None
def main_logic():
    """
    :return: the function is in charge of the main logic on the client side, such as deciding what to tsend to the server and when
    """
    global name, t, cBoard, vcclient, n, data
    color = cBoard.start_user
    ct = 0
    print(n)
    voicechat_port = n.send("vcport")
#    print(n.server)

    vcclient = VCClient(voicechat_port)
    cBoard = n.send("update_moves")

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
    """
    the function is in charge of calling other functions, as well as get the arguments from the launcher
    """
    global name
    parser = argparse.ArgumentParser(description='Process args from launcher')
    parser.add_argument("username", help="Client Username")
    parser.add_argument("-ip","--server_ip",action="store" ,help="Server IP")
    args = parser.parse_args()
    name = args.username
    install_requirements()
    init_window()
    init_board()
    Globals.init()
    pygame.display.set_caption("VoiceChess")
    menu(wind=wind, name=name)




if __name__ == "__main__":
    main()

















