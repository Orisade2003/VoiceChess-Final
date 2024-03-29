import pygame
import os
import traceback
import Globals


wbishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
wking = pygame.image.load(os.path.join("img", "white_king.png"))
wknight = pygame.image.load(os.path.join("img", "white_knight.png"))
wpawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
wqueen = pygame.image.load(os.path.join("img", "white_queen.png"))
wrook = pygame.image.load(os.path.join("img", "white_rook.png"))


bbishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
bking = pygame.image.load(os.path.join("img", "black_king.png"))
bknight = pygame.image.load(os.path.join("img", "black_knight.png"))
bpawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
bqueen = pygame.image.load(os.path.join("img", "black_queen.png"))
brook = pygame.image.load(os.path.join("img", "black_rook.png"))



b = [bbishop, bking, bknight, bpawn, bqueen, brook]
w = [wbishop, wking, wknight, wpawn, wqueen, wrook]
Black_Pieces=[]
White_Pieces=[]

for img in w:
    White_Pieces.append(pygame.transform.scale(img, (55, 55)))

for img in b:
    Black_Pieces.append(pygame.transform.scale(img, (55, 55)))



class Piece:
    img=-1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]



    def __init__(self,row, col,color):
        self.row=row
        self.col=col
        self.color=color
        self.moves=[]
        self.is_selected=False
        self.is_king=False
        self.is_pawn = False
        self.has_moved = False
        self.is_rook = False


    def get_pixels(self, row, col,):

        if self.color == "w":
            y, x = row, col

        else:
            y, x = (7 - row, 7 - col)


        xx = (4 - x) + round(self.rect[0] + (x * self.rect[2] / 8))
        yy = 3 + round(self.startY + (y * self.rect[3] / 8))
        return xx+32, yy+30

    def draw(self,win,color, player="w", selected=None, save_moves = None, is_checked = False):
        if self.color =="w":
            this = White_Pieces[self.img]
        else:
            this = Black_Pieces[self.img]

        if player == "b":
            newcol = 7 - self.col
            newrow = 7 - self.row
        else:
            newcol = self.col
            newrow = self.row

        x = (4 - newcol) + round(self.startX + (newcol * self.rect[2] / 8))
        y = 3 + round(self.startY + (newrow * self.rect[3] / 8))

        if selected and str(self) == str(selected) and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

            if not is_checked:
                for move in self.moves:
                        xx1, yy1 = self.get_pixels(move[0],move[1])
                        pygame.draw.circle(win, (0, 255, 255), (yy1,xx1 ), 10, 10)
            else:
                for move in self.moves:
                    if move in save_moves:
                        xx1, yy1 = self.get_pixels(move[0], move[1])
                        pygame.draw.circle(win, (0, 255, 255), (yy1, xx1), 10, 10)





        win.blit(this,(x,y))

    def isSelected(self):
        return self.is_selected

    def move_to_pos(self, pos):
        try:
            print(self.row, self.col, " this is the current pos")
            self.row = pos[0]
            self.col = pos[1]
        except Exception as e:
            print(e)
            print(traceback.print_exc())



    def get_moves(self, board):
        try:
            self.moves = self.get_valid_moves(board)
        except Exception as e:
            print(e)
            print(traceback.print_exc())




    def __str__(self):
        return str(self.row) + ' ' + str(self.col)



class Knight(Piece):

    img = 2

    def get_valid_moves(self,board):
        r = self.row
        c = self.col
        add_moves=[]

        #down left
        if r < 6 and c > 0:
            p = board[r+2][c-1]
            if p == 0:
                add_moves.append((c-1,r+2))
            elif self.color != p.color:
                add_moves.append((c - 1, r + 2))
            p = board[r + 2][c - 1]

        #down right
        if r<6 and c<7:
            p=board[r+2][c+1]
            if p ==0:
                add_moves.append((c+1,r+2))
            elif self.color != p.color:
                add_moves.append((c+1,r+2))

         #up left
        if r > 1 and c > 0:
             p=board[r-2][c-1]
             if p == 0:
                 add_moves.append((c-1,r-2))
             elif p.color != self.color:
                 add_moves.append((c - 1, r - 2))

        #up right
        if r > 1 and c < 7:
            p=board[r-2][c+1]
            if p == 0:
                add_moves.append((c+1,r-2))
            elif self.color != p.color:
                add_moves.append((c + 1, r - 2))

        #left - up
        if c > 1 and r > 0:
            p=board[r-1][c-2]
            if p == 0:
                add_moves.append((c-2,r-1))
            elif self.color != p.color:
                add_moves.append((c-2,r-1))

        #right-up
        if c < 6 and r > 0:
            p=board[r-1][c+2]
            if p == 0:
                add_moves.append((c+2,r-1))
            elif self.color != p.color:
                add_moves.append((c+2,r-1))

        #left-down
        if c > 1 and r < 7:
            p=board[r+1][c-2]
            if p == 0:
                add_moves.append((c-2,r+1))
            elif self.color != p.color:
                add_moves.append((c-2,r+1))
        #right - down
        if c < 6 and r < 7:
            p=board[r+1][c+2]
            if p == 0:
                add_moves.append((c+2,r+1))
            elif self.color !=  p.color:
                add_moves.append((c+2,r+1))

        return add_moves





class Bishop(Piece):
    img=0

    def get_valid_moves(self,board):
        try:
            r=self.row
            c=self.col
            add_moves=[]
            above_col=c+1
            bottom_col=c-1
            # top right
            for box in range(r-1,-1,-1):
                if above_col<8:
                    p=board[box][above_col]
                    if p==0:
                        add_moves.append((above_col,box))
                    elif self.color!= p.color:
                        add_moves.append((above_col,box))
                        break
                    else:
                        break
                above_col+=1

            #bottom right
            for box in range(r - 1, -1, -1):
                if bottom_col >-1:
                    p = board[box][bottom_col]
                    if p == 0:
                        add_moves.append((bottom_col, box))
                    elif self.color != p.color:
                        add_moves.append((bottom_col,box))
                        break
                    else:
                        break
                bottom_col -= 1

            above_col=c+1
            bottom_col=c-1
            # top left
            for box in range(r +1, 8):
                if above_col<8:
                    p = board[box][above_col]
                    if p == 0:
                        add_moves.append((above_col,box))
                    elif self.color != p.color:
                        add_moves.append((above_col,box))
                        break
                    else:
                        break
                above_col += 1
            #bottom left
            for box in range(r + 1, 8):
                if bottom_col>-1:
                    p = board[box][bottom_col]
                    if p == 0:
                        add_moves.append((bottom_col,box))
                    elif self.color != p.color:
                        add_moves.append((bottom_col,box))
                        break
                    else:
                        break
                bottom_col-=1

            return add_moves
        except Exception as e:
            print(e)
            print(traceback.print_exc())



class King(Piece):
    img=1
    def __init__(self, row, col, color):
        super().__init__(row,col,color)
        self.is_king=True

    def get_valid_moves(self,board):
        r=self.row
        c=self.col
        add_moves=[]
        #top left
        if r>0:
            if c>0:
                p=board[r-1][c-1]
                if p == 0:
                    add_moves.append((c-1,r-1))
                elif p.color!=self.color:
                    add_moves.append((c - 1, r - 1))

        # top mid  --> notice how it is included in the top if checking if r>0
            p = board[r-1][c]
            if p == 0 :
                add_moves.append((c,r-1))
            elif p.color != self.color:
                add_moves.append((c,r-1))

        #top right
            if c<7:
                p=board[r-1][c+1]
                if p == 0:
                    add_moves.append((c+1,r-1))
                elif p.color != self.color:
                    add_moves.append((c + 1, r - 1))
        #bottom left
        if r<7:
            if c>0:
                p=board[r+1][c-1]
                if p == 0:
                  add_moves.append((c-1,r+1))
                elif p.color != self.color:
                    add_moves.append((c - 1, r + 1))

        #bottom mid
            p = board[r+1][c]
            if p == 0:
                add_moves.append((c,r+1))
            elif p.color != self.color:
                add_moves.append((c, r + 1))

        #bottom right
            if c<7:
                p = board[r+1][c+1]
                if p == 0:
                    add_moves.append((c+1,r+1))
                elif p.color != self.color:
                    add_moves.append((c + 1, r + 1))
        # middle left
        if c>0:
            p = board[r][c-1]
            if p==0:
                add_moves.append((c-1,r))
            elif p.color != self.color:
                add_moves.append((c - 1, r ))

        #middle right
        if c<7:
            p=board[r][c+1]
            if p == 0:
                add_moves.append((c+1,r))
            elif self.color != p.color:
                add_moves.append((c + 1, r))

        return add_moves





class Queen(Piece):
    img = 4


    def get_valid_moves(self, board):
         r = self.row
         c = self.col
         add_moves=[]

         # Moving TopRight
         above_col = c+1
         bottom_col = c-1
         for box in range(r - 1, -1, -1):
             if above_col < 8:
                 p = board[box][above_col]
                 if p == 0:
                     add_moves.append((above_col,box))
                 elif self.color != p.color:
                     add_moves.append((above_col, box))
                     break
                 else:
                     break
             above_col += 1
         bottom_col = c - 1
         above_col = c + 1


         for box in range(r - 1, -1, -1):
             if bottom_col > -1:
                 p=board[box][bottom_col]
                 if p == 0:
                     add_moves.append((bottom_col,box))
                 elif p.color != self.color:
                     add_moves.append((bottom_col,box))
                     break
                 else:
                     break
             bottom_col -= 1

         bottom_col = c - 1
         above_col = c + 1

         for box in range( r +1, 8):
             if above_col < 8:
                 p= board[box][above_col]
                 if p == 0:
                     add_moves.append((above_col, box))
                 elif self.color != p.color:
                     add_moves.append((above_col,box))
                     break
                 else:
                     above_col = 8
             above_col += 1
         bottom_col = c - 1
         above_col = c + 1

         for box in range(r+1, 8):
             if bottom_col > -1:
                 p = board[box][bottom_col]
                 if p == 0:
                     add_moves.append((bottom_col, box))
                 elif self.color != p.color:
                     add_moves.append((bottom_col,box))
                     break
                 else:
                     break
             bottom_col -= 1



             #bottom_col -=1
         bottom_col = c - 1
         above_col = c + 1

         # going up
         for box in range(r-1 ,-1 ,-1):
             p = board[box][c]
             if p == 0:
                 add_moves.append((c,box))
             elif self.color != p.color:
                 add_moves.append((c,box))
                 break
             else:
                 break


         for box in range(r+1,8):
            p=board[box][c]
            if p == 0:
                add_moves.append((c,box))
            elif self.color != p.color:
                add_moves.append((c,box))
                break
            else:
                break

         # going right
         for y in range(c+1, 8):
             p = board[r][y]
             if p == 0:
                 add_moves.append((y,r))
             elif self.color != p.color:
                 add_moves.append((y, r))
                 break
             else:
                 break

         # going left
         for y in range (c-1, -1, -1):
             p=board[r][y]
             if p == 0:
                 add_moves.append((y,r))
             elif self.color != p.color:
                 add_moves.append((y,r))
                 break
             else:
                 break
         illegal_pos = (self.col-3, self.row+2)
         illegal_pos2 = (self.col-5,self.row + 3)
         if illegal_pos in add_moves:
             add_moves.remove(illegal_pos)
         if illegal_pos2 in add_moves:
             add_moves.remove(illegal_pos2)
         return add_moves


class Rook(Piece):
    img = 5


    def get_valid_moves(self, board):
        r = self.row
        c = self.col
        add_moves = []
        self.is_rook = True

        # up
        for y in range(r-1, -1, -1):
            p = board[y][c]
            if p == 0:
                add_moves.append((c, y))
            elif p.color != self.color:
                add_moves.append((c, y))

            else:
                break

        # down
        for y in range(r + 1, 8):
            p = board[y][c]
            if p == 0:
                add_moves.append((c, y))
            elif p.color != self.color:
                add_moves.append((c, y))
                break
            else:
                break

        #right
        for y in range(c+1, 8):
            p=board[r][y]
            if p == 0:
                add_moves.append((y, r))
            elif p.color != self.color:
                add_moves.append((y, r))
                break
            else:
                break


        # left
        for y in range(c-1 ,-1, -1):
            p = board[r][y]
            if p == 0:
                add_moves.append((y, r))
            elif self.color != p.color:
                add_moves.append((y,r))
                break
            else:
                break

        return add_moves



class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row,col,color)
        self.is_pawn = True
        self.is_queen = False
        self.is_first = True

    def get_valid_moves(self, board):
        r= self.row
        c=self.col
        add_moves=[]
        # straight
        try:
            if self.color == "b":
                if r < 7:
                    p = board[r+1][c]
                    if p == 0:
                        add_moves.append((c,r+1))
                    #diagonal
                    if c < 7:
                        p = board[r+1][c+1]
                        if p !=0:
                            if p.color != self.color:
                                add_moves.append((c+1,r+1))

                    if c > 0:
                        p=board[r+1][c-1]
                        if p!=0:
                            if p.color != self.color:
                                add_moves.append((c-1,r+1))
                if self.is_first:
                    if r < 6:
                        if r <6:
                            p=board[r+2][c]
                            if p == 0:
                                if board[r+1][c] == 0:
                                    add_moves.append((c,r+2))
                            #elif self.color != p.color:
                                #add_moves.append((c,r+2))
            # white moves

            else:
                if r > 0:
                    p=board[r-1][c]
                    if p == 0:
                        add_moves.append((c,r-1))
                if c < 7:
                    p=board[r-1][c+1]
                    if p != 0:
                        if p.color != self.color:
                            add_moves.append((c+1,r-1))
                if c > 0:
                    p=board[r-1][c-1]
                    if p != 0:
                        if self.color !=p.color:
                            add_moves.append((c-1,r-1))

                if self.is_first:
                    if r > 1:
                        p=board[r-2][c]
                        if p == 0:
                            if board[r-1][c] == 0:
                                add_moves.append((c,r-2))
                        elif self.color != p.color:
                            add_moves.append((c,r-2))
        except Exception as e:
            print(e)
            print(traceback.format_exc())


        return add_moves






































