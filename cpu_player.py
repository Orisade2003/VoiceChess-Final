from ChessBoard import Board
from ChessPiece import Piece

import pygame
from copy import deepcopy
import socket
import os
import time
import Globals
import traceback
import random
width = 750
height = 750
game_running = True
cBoard = Board(8,8)
cBoard.is_full =True

def get_AI_moves():
    l2 = []
    if not cBoard.checked("b"):
        for co in range(cBoard.rows):
            for r in range(cBoard.cols):
                if type(cBoard.board[co][r]) != int and cBoard.board[co][r].color == "b" and len(cBoard.board[co][r].moves) != 0:
                        l2.append(cBoard.board[co][r])
        p = l2[random.randint(0,len(l2)-1)]


        rand_move = random.randint(0,len(p.moves)-1)

        return (p.col,p.row),(p.moves[rand_move])

    elif not cBoard.checkmate3("b"):
        moving_piece = None
        new_board = deepcopy(cBoard)
        boardlist = new_board.board
        pos = random.choice(list(cBoard.save_moves.keys()))
        return pos, cBoard.save_moves[pos]


    """elif not cBoard.checkmate3("b"):
        print("started")
        p = None
        b = False
        current = []
        moving_piece = None
        new_board = deepcopy(cBoard)
        boardlist = new_board.board
        for col in range(len(boardlist)):
            for row in range(len(boardlist[col])):
                if type(boardlist[col][row]) == int:
                    continue
                if not boardlist[col][row].color == "b":
                    continue

                p = boardlist[col][row]
                all_moves = p.get_valid_moves(boardlist)

                for t in all_moves:
                    if new_board.move((col, row), (t[1], t[0]), "b"):
                        moving_piece = new_board.board[col][row]
                        l2.append(t)
                        b = True
                        return (row,col),(t[1],t[0])
                if b:
                    break
        rand_move = l2[random.randint(0,len(l2)-1)]
        print("this is it", (moving_piece.col,moving_piece.row),rand_move)
        return (moving_piece.col,moving_piece.row),rand_move
    else:
        if cBoard.checkmate3("w"):
            cBoard.winner = "b"
        elif cBoard.checkmate3("b"):
            cBoard.winner = "w"""






def init_window():
    global wind
    wind = pygame.display.set_mode((width, height))

def init_board():
    global board, chessbg, rect, t
    pygame.font.init()
    board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
    chessbg = pygame.image.load(os.path.join("img", "ChessKingBG2.png")) #"chessbg.png"
    rect = (113, 113, 525, 525)
    t = "w"

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

                pygame.quit()

                exit(0)


            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:

                    run = False
                    main_logic()
                    break

                except Exception as e:
                    #print("Server might be offline")
                    print(traceback.print_exc())
                    offline = True


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
            xx = x - rect[0]
            yy = y - rect[1]

            c = int(xx / (rect[2] / 8))
            r = int(yy / (rect[3] / 8))
            if player == "b":
                return (7 - r, 7 - c)
            return (r, c)
    else:
        return (-1, -1)
    """a (-1,-1) means that the position is not on the chess board"""


def event_handler(color):
    """

    :param color: string, color of the player
    the function is in charge of handling all the different events that can occur during the game
    """
    global ctr,ctr2, selected
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if color == "w":
                cBoard.winner="b"
            elif color == "b":
                cBoard.winner = "w"
            # quit()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and color != "s":
                if color == "w":
                    cBoard.winner = "b"
                elif color == "b":
                    cBoard.winner="b"

            if event.key == pygame.K_RIGHT:
                #n.send("forward")
                pass
            if event.key == pygame.K_LEFT:
                #n.send("back")
                 pass

        if event.type == pygame.MOUSEBUTTONDOWN and color != "s":
            if color == cBoard.turn and cBoard.is_full:
                mouse_pos = pygame.mouse.get_pos()
                print("here")
                cBoard.get_all_moves()

                r, c = select(mouse_pos, color)
                if (cBoard.board[r][c] != 0) and (cBoard.board[r][c].color == color):
                    Globals.selected = cBoard.board[r][c]

                else:
                    if Globals.selected:
                        if (c,r) in Globals.selected.moves:

                            info = f"move_piece {color} {str(Globals.selected.row)} {str(Globals.selected.col)} {str(r)} {str(c)}"
                            move(info,"b")
                            start, end = get_AI_moves()

                            info = f"move_piece b {str(start[1])} {str(start[0])} {str(end[1])} {end[0]}"
                            move(info, "w")


                            Globals.selected = None


def move(info,opp_color):
    data = info.split(" ")
    print(data)
    color = data[1]
    current_row = int(data[2])
    current_col = int(data[3])

    new_row = int(data[4])
    new_col = int(data[5])

    if color != cBoard.turn:
        print()

    start = (current_row, current_col)
    end = (new_row, new_col)
    print("current row and col:", cBoard.board[current_row][current_col])
    if not cBoard.move(start, end, color):
        print()

    opp_color = "b" if color == "w" else "w"

    if cBoard.checkmate3(opp_color):
        cBoard.winner = color
        winner = cBoard.winner

    else:
        cBoard.turn = opp_color





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





                pygame.quit()
                display_end_screen = False

            elif event.type == pygame.KEYDOWN:
                display_end_screen = False
            elif event.type == pygame.USEREVENT:
                display_end_screen = False
    exit(0)








def main_logic():
    """
     the function is in charge of the main logic on the client side, such as deciding what to send to the server and when
    """
    global name, t, cBoard, vcclient, data
    color = "w"
    ct = 0

    #voicechat_port = n.send("vcport")
#    print(n.server)


    cBoard.get_all_moves()

    cBoard.player1_name = name

    clock = pygame.time.Clock()

    #threading.Thread(target=game_event_handler, args=(color)).start()
    #n.send("ready")
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


                #vcclient.dele()
            except:
                print(traceback.print_exc())




        if cBoard.winner is not None:
            break

        if color != "s":
            if cBoard.playingtime1 <= 0:
                cBoard.winner = "b"
                break
            elif cBoard.playingtime2 <= 0:
                cBoard.winner = "w"
                break



        ct += 1
        if ct % 5 == 0:
            cBoard.get_all_moves()
            ct = 0

        draw_game_window(wind, cBoard, cBoard.playingtime1, cBoard.playingtime2, color, True)



        time.sleep(0.1)

      #data = n.recv(data)



def draw_game_window(wind, cBoard, p1, p2, color, isReady = True):
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
        rep1 = font.render(cBoard.player1_name + r"\'s time: " + str(formatTime1) ,1 ,(255,255,255))
        rep2 = font.render(cBoard.player2_name + r"\'s time: "+ str(formatTime2),1, (255,255,255))
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
            wind.blit(show, (width/2 - show.get_width()/2 + 50 , 10))
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




import argparse
wind = None


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
    init_window()
    init_board()
    Globals.init()
    pygame.display.set_caption("VoiceChess")
    menu(wind, name)

main()