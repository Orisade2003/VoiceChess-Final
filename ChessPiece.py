import pygame
import os
import traceback


b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]
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

    def isSelected(self):
        return self.is_selected

    def get_moves(self, board):
        try:
            self.moves= self.get_valid_moves(board)
        except Exception as e:
            print(e)
            print(traceback.print_exc())


    def draw(self,win,color):
        if self.color =="w":
            this = White_Pieces[self.img]
        else:
            this = Black_Pieces[self.img]

        x = (4 - self.col) + round(self.startX + (self.col * self.rect[2] / 8)) #make sure i understand this part
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))#make sure i understamd this part

        if self.is_selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)
            print(x,y , "fdfdfdfdfdfddamni")

        win.blit(this,(x,y))



        """all_moves = self.moves for move in all_moves:
            x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))#understand better
            y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))#understand better
            pygame.draw.circle(win,(255, 0 ,0),(x,y),10)"""

    def move_to_pos(self,pos):
        try:
            print(self.row, self.col, " this is the current pos")
            self.row=pos[0]
            self.col=pos[1]
            print(self.row,self.col, 2222222)
        except Exception as e:
            print(e)
            print(traceback.print_exc())

    def __str__(self):
        return str(self.col) + ' ' + str(self.row)


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
                add_moves.append(c, r + 1)

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
                add_moves.append((c-1,r-1))
            elif p.color!=self.color:
                add_moves.append((c - 1, r - 1))

        #middle right
        if c<7:
            p=board[r][c+1]
            if p == 0:
                add_moves.append((c+1,r))
            elif self.color != p.color:
                add_moves.append((c + 1, r))

        return add_moves

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
                            elif self.color != p.color:
                                add_moves.append((c,r+2))
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
            print("hereitis")

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
                     above_col = 9
             above_col += 1


         for box in range(r - 1, -1, -1):
             if bottom_col < 8:
                 p=board[box][bottom_col]
                 if p == 0:
                     add_moves.append((bottom_col,box))
                 elif p.color != self.color:
                     add_moves.append((bottom_col,box))
                     break
                 else:
                     bottom_col = -1
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


         for box in range(r+1, 8):
             if bottom_col > -1:
                 p = board[box][bottom_col]
                 if p == 0:
                     add_moves.append((bottom_col, box))
                 elif self.color != p.color:
                     add_moves.append((bottom_col,box))
                     break
                 else:
                     bottom_col = -1
             bottom_col = -1

         # going up
         for box in range(r-1 ,-1 ,-1):
             p = board[box][c]
             if p == 0:
                 add_moves.append((c,box))
             elif self.color != self.color:
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









































