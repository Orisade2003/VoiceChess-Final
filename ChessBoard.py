import pygame
import os
import time
from copy import deepcopy
from ChessPiece import Bishop
from ChessPiece import King
from ChessPiece import Rook
from ChessPiece import Pawn
from ChessPiece import Queen
from ChessPiece import Knight
import time
import pygame

#this class is in charge of the board object, which represents the board drawn on the client's screen
class Board:
    ROWS=8
    COLUMNS=8
    rect = (113, 113, 525, 525)
    startX = rect[0]
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

    def get_all_moves(self):
        """
        the function adds all the piece's moves to a list
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    self.board[r][c].get_moves(board=self.board)



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
            # do'nt really understand this part
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
                    p.draw(win, color, player, selected)
                    if self.board[r][c].is_selected:
                        t = (r, c)


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
                        for move in self.board[r][c].moves:# was .moves before
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
                        king_pos = (c, r)#was c,r
        if king_pos in kills:
            print("point of no return", king_pos)
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





    def checkmate(self, color):
        flag = False

        if self.checked(color):
            king = None
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.board[r][c] != 0:
                        box = self.board[r][c]
                        if type(box) is King and box.color == color:
                            king = box
            if king != None:
                moves = king.get_valid_moves(board=self.board)

                kills =self.get_kills(color)

                kill_ct = 0
                for move in moves:
                    if move in kills:
                        kill_ct += 1
                flag = False
                if len(moves) == kill_ct:
                    flag = True
                return flag
        """
        nb =self.board[:]
        save = self.board[:]
        if color == "b":
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col]!=0:
                        p = self.board[row][col]
                        if p.color == "b":
                            m = p.moves
                            for i in m:
                                nb[p.row][p.col] = 0
                                nb[i[0]][i[1]] = p
                                self.board=nb
                                if self.checked(color):
                                    flag = True
                                    self.board = save
                                else:
                                    self.board=save
                                    return False
                                    break
        else:
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col] != 0:
                        p = self.board[row][col]
                        if p.color == "b":
                            m = p.moves
                            for i in m:
                                nb[p.row][p.col] = 0
                                nb[i[0]][i[1]] = p
                                self.board = nb
                                if self.checked(color):
                                    flag = True
                                    self.board = save
                                else:
                                    self.board = save
                                    return False
                                    break
        if flag:
            return flag
            """
        return False


    def move(self, start, end, color):
        """

        :param start: tuple, starting position of the selected piece
        :param end: tuple, end position of the selected piece
        :param color: the player's color
        :return: bool, the funcion moves the piece to the end postion if the move is legal and returns true, if the move isn't legal the function returns false
        """
        
        checkedBefore = self.checked(color)
        print("Trying to move to : ", end)

        changed = True
        nBoard = self.board[:]
        
        if nBoard[start[0]][start[1]].is_pawn:
            isfirst = nBoard[start[0]][start[1]].is_first
            nBoard[start[0]][start[1]].is_first = False

        original_piece = nBoard[end[0]][end[1]]
        nBoard[start[0]][start[1]].move_to_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard
        
        if self.checked(color) or (checkedBefore and self.checked(color)):
            changed = False
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
        if changed:
            self.last = [start, end]
            if self.turn == "w":
                self.time_stored1 += (time.time() - self.startTime)
            else:
                self.time_stored2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed


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

                for t in all_moves:
                    if new_board.move((col, row), (t[1],t[0]), color):
                        print("this is where the checkm happens", t, type(p), p.color,(col,row))
                        print(p.moves)

                        return False
        return True
        
        



    def piece_select2(self, col, row, color):
        has_moved = False
        previous = (-1, -1)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[c][r] != 0:
                    if self.board[c][r].is_selected:
                        previous = (c,r)#change to r,c if doesnt work
        print("previous is ", previous)
        if self.board[col][row] == 0 and previous != (-1, -1):
            c = previous[0]
            r = previous[1]
            moves = self.board[c][r].moves
            if (col, row) in moves: # change to col, row
                has_moved = self.move(previous, (row, col), color)#cheack here

        else:
            if previous == (-1, -1):
                self.resetSelect()
                if self.board[col][row] != 0:
                    self.board[col][row].is_selected = True
                    print("changed ", self.board[col][row])
            else:
                     if self.board[previous[0]][previous[1]].color != self.board[col][row].color:
                         moves = self.board[previous[0]][previous[1]].moves
                         if (col, row) in moves:# change to col row
                             has_moved = self.move(previous, (row, col), color)

                         if self.board[col][row].color == color:
                             self.board[col][row].is_selected = True
                      # castle
                     else:
                        if self.board[col][row].color == color:
                             self.resetSelect()
                             if self.board[previous[0]][previous[1]].has_moved == False and self.board[previous[0]][previous[1]].is_rook and self.board[col][row].is_king and col!= previous[1] and previous!=(-1,-1):
                                can_castle = True
                                if previous[1] < col:
                                    for c in range(previous[1]+1, col):
                                        if self.board[row][c] != 0:
                                            can_castle = False
                                    if can_castle:
                                        has_moved = self.move(previous, (row,3), color)
                                        has_moved = self.move((row, col), (row, 2), color)
                                        if has_moved == False:
                                            self.board[row][col].is_selected = True
                                else:
                                    for c in range(col+1, previous[1]):
                                        if self.board[row][c] != 0:
                                            can_castle =False
                                    if can_castle:
                                        has_moved = self.move(previous, (row, 5), color)
                                        has_moved = self.move((row,col), (row, 6), color)
                                    if has_moved == False:
                                        self.board[row][col].is_selected = True
                             else:
                                self.board[col][row].is_selected = True

        if has_moved:
            if self.turn == "b":
                if self.checkmate3("w"):
                    self.winner = "b"

                self.turn = "w"

                self.resetSelect()


            else:
                if self.checkmate3("b"):
                    self.winner = "w"
                self.turn = "b"

                self.resetSelect()
        print("the piece selected is :     ",previous, col, row)
        print("previous : ", previous)
        print("The Piece is now")





















    def piece_select(self, col, row, color): #change col row order if doesnt work
        has_moved = False
        previous = (-1, -1)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    if self.board[r][c].is_selected:
                        previous = (r,c)#change to r,c if doesnt work
        print("previous is ", previous)
        if self.board[row][col] == 0 and previous != (-1, -1):
            r = previous[0]
            c = previous[1]
            moves = self.board[r][c].moves
            if (col, row) in moves: # change to col, row
                has_moved = self.move(previous, (row, col), color)

        else:
            if previous == (-1, -1):
                self.resetSelect()
                if self.board[row][col] != 0:
                    self.board[row][col].is_selected = True
                    print("changed ", self.board[row][col])
            else:
                     if self.board[previous[0]][previous[1]].color != self.board[row][col].color:
                         moves = self.board[previous[0]][previous[1]].moves
                         if (col, row) in moves:# change to col row
                             has_moved = self.move(previous, (row, col), color)

                         if self.board[row][col].color == color:
                             self.board[row][col].is_selected = True
                      # castle
                     else:
                        if self.board[row][col].color == color:
                             self.resetSelect()
                             if self.board[previous[0]][previous[1]].has_moved == False and self.board[previous[0]][previous[1]].is_rook and self.board[row][col].is_king and col!= previous[1] and previous!=(-1,-1):
                                can_castle = True
                                if previous[1] < col:
                                    for c in range(previous[1]+1, col):
                                        if self.board[row][c] != 0:
                                            can_castle = False
                                    if can_castle:
                                        has_moved = self.move(previous, (row,3), color)
                                        has_moved = self.move((row, col), (row, 2), color)
                                        if has_moved == False:
                                            self.board[row][col].is_selected = True
                                else:
                                    for c in range(col+1, previous[1]):
                                        if self.board[row][c] != 0:
                                            can_castle =False
                                    if can_castle:
                                        has_moved = self.move(previous, (row, 5), color)
                                        has_moved = self.move((row,col), (row, 6), color)
                                    if has_moved == False:
                                        self.board[row][col].is_selected = True
                             else:
                                self.board[row][col].is_selected = True

        if has_moved:
            if self.turn == "b":
                if self.checkmate3("w"):
                    self.winner = "b"

                self.turn = "w"

                self.resetSelect()


            else:
                if self.checkmate3("b"):
                    self.winner = "w"
                self.turn = "b"

                self.resetSelect()
        print("the piece selected is :     ",previous, col, row)
        print("previous : ", previous)
        print("The Piece is now")

    def resetSelect(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    self.board[r][c].is_selected = False









""" def move(self, start, end, color):
        cb = self.checked(color)
        has_moved= True
        ub = self.board[:]
        if self.board[start[0]][start[1]].is_pawn:
            self.board[start[0]][start[1]].is_first = False
        ub[start[0]][start[0]].move_to_pos((end[0],end[1]))
        ub[end[0]][end[1]] = ub[start[0]][start[1]]
        ub[start[0]][start[1]] = 0
        self.board = ub
        if self.checked(color) or (cb and self.checked(color)):
            has_moved = False
            ub = self.board[:]
            if ub[start[0]][start[1]].is_pawn:
                self.board[start[0]][start[1]].is_first = True
            ub[end[0]][end[1]].move_to_pos((start[0], start[1]))
            ub[end[0]][end[1]] = ub[start[0]][start[1]]
            ub[end[0]][end[1]] = 0
            self.board = ub
        else:
            self.resetSelect()
        self.get_all_moves()
        if has_moved:
            self.last=[start, end]
            if self.turn == "w":
                self.time_stored1 += (time.time() - self.startTime)
            else:
                self.time_stored2 += (time.time() - self.startTime)
            self.startTime = time.time()
        if has_moved:
            print("Moved From       ", start, end)
        return has_moved"""