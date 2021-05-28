import pygame
import os
import time
from copy import deepcopy
from ChessPiece import Knight
from ChessPiece import King
from ChessPiece import Rook
from ChessPiece import Pawn
from ChessPiece import Queen
from ChessPiece import Bishop
import time
import pygame

#this class is in charge of the board object, which represents the board drawn on the client's screen
class Board:
    ROWS=8
    COLUMNS=8
    rect = (113, 113, 525, 525)
    startX = rect[0]
    save_moves=[]
    startY = rect[1]
    f=[]
    def __init__(self, rows, cols):
        """

        :param rows: number of rows on the board, int
        :param cols: number of columns on the board, int
        """
        rows, cols = (8, 8)
        self.board = [[0] * cols] * rows
        print(self.board)
        self.turn="w"
        self.is_full=False
        self.winner=None
        self.last = None
        self.copy = True
        self.piece_selected = None
        self.rows = rows
        self.cols = cols
        self.board = [[0 for x in range(8)] for y in range(rows)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.turn = "w"
        self.playingtime1 = 900
        self.playingtime2 = 900
        self.time_stored1 = 0
        self.time_stored2 = 0

        self.winner = None
        self.startTime = time.time()
        self.get_all_moves()





    def draw(self, win, color, player="w", selected=None):
        """

        :param win:pygame window
        :param color: what color is the client,string
        :param player: whose turn is it, string
        :param selected: bool, which piece is selected
        the function is charge of drawing blue circles around the 2 spots involved in the opponent's last move, and red squares around the current piece selected by the user
        """
        z=()
        if self.last and color == self.turn:
            if player == "w":
                y,x =self.last[0]
                y1, x1 = self.last[1]
            else:
                y, x = (7 - self.last[0][0] , 7 - self.last[0][1])
                y1, x1 = (7 - self.last[1][0], 7 - self.last[1][1])

            xx = (4 - x) + round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx + 32, yy + 30), 34, 4)
            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3 + round(self.startY + (y1 * self.rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)


            t = ()

        for r in range(self.rows):
            for c in range(self.cols):
                p = self.board[r][c]
                if type(p) != int:
                    p.draw(win, color, player, selected, [], self.checked(color))
                    if self.board[r][c].is_selected:
                        t = (r, c)



    def get_all_moves(self):
        """
        the function adds all the piece's moves to a list
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    self.board[r][c].get_moves(board=self.board)




    def get_save(self, color):
        new_board = deepcopy(self)
        boardlist = new_board.board
        print(boardlist)
        for col in range(len(boardlist)):
            for row in range(len(boardlist[col])):
                if type(new_board.board[col][row]) == int:
                    continue
                if not new_board.board[col][row].color == color:
                    continue

                p = new_board.board[col][row]
                all_moves = p.get_valid_moves(boardlist)
                self.save_moves = []
                for t in all_moves:
                  boardlist[t[0]][t[1]] = boardlist[col][row]
                  temp = boardlist[t[1]][t[0]]
                  if not new_board.checked(color):
                      self.save_moves.append((t[1],t[0]))
                      boardlist[col][row] = boardlist[t[1]][t[0]]
                      boardlist[t[1]][t[0]]= temp


        return self.save_moves


    def get_kills(self, color):
        """
        :param color: color of the player
        :return: a list of all the moves in which the client can capture the other player's pieces.
        """
        kills = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    if self.board[r][c].color != color:
                        for move in self.board[r][c].moves:
                            kills.append(move)
        return kills



    def checked(self, color):
        """

        :param color: color of the player
        :return: a boolean, True if there is a check and false otherwise
        """
        self.get_all_moves()
        kills = self.get_kills(color)
        king_pos = (9, 9)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    if type(self.board[r][c]) is King and self.board[r][c].color == color:
                        king_pos = (c, r)
        if king_pos in kills:
            self.f.append(king_pos)
            return True
        return False



    def resetSelect(self):
        """
        the function makes sure no piece is currently selected, and un selects selected pieces
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    self.board[r][c].is_selected = False
        self.piece_selected = False



    def move(self, start, end, color):
        """

        :param start: tuple, starting position of the selected piece
        :param end: tuple, end position of the selected piece
        :param color: the player's color
        :return: bool, the funcion moves the piece to the end postion if the move is legal and returns true, if the move isn't legal the function returns false
        """
        
        was_checked = self.checked(color)
        print("Trying to move to : ", end)

        has_moved = True
        nBoard = self.board[:]
        
        if type(nBoard[start[0]][start[1]])!= int and nBoard[start[0]][start[1]].is_pawn:
            isfirst = nBoard[start[0]][start[1]].is_first
            nBoard[start[0]][start[1]].is_first = False

        original_piece = nBoard[end[0]][end[1]]
        nBoard[start[0]][start[1]].move_to_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard
        
        if self.checked(color) or (was_checked and self.checked(color)):
            has_moved = False
            nBoard = self.board[:]
            if not type(nBoard[end[0]][end[1]]) == int:
                if nBoard[end[0]][end[1]].is_pawn:
                    nBoard[end[0]][end[1]].is_first = isfirst

                nBoard[end[0]][end[1]].move_to_pos((start[0], start[1]))
                nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
                nBoard[end[0]][end[1]] = original_piece
                self.board = nBoard
        else:
            self.resetSelect()

        self.get_all_moves()
        if has_moved:
            self.last = [start, end]
            if self.turn == "w":
                self.time_stored1 += (time.time() - self.startTime)
            else:
                self.time_stored2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return has_moved


    def checkmate3(self,color):
        """

        :param color: player's color, string
        :return: bool, true if there is a checkmate, false otherwise
        """
        self.f = []
        if not self.checked(color):
            return False
    
        new_board = deepcopy(self)
        boardlist = new_board.board
        print(boardlist)
        for col in range(len(boardlist)):
            for row in range(len(boardlist[col])):
                if type(boardlist[col][row]) == int:
                    continue
                if not boardlist[col][row].color == color:
                    continue
                    
                p = boardlist[col][row]
                all_moves = p.get_valid_moves(boardlist)
                self.save_moves = []
                for t in all_moves:
                    if new_board.move((col, row), (t[1],t[0]), color):
                        print("this is where the checkm happens", t, type(p), p.color,(col,row))
                        self.save_moves.append((t[1],t[0]))
                        return False
        return True
        
        










