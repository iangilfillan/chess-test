import random
import re

class Empty_Square():
    def __init__(self):
        self.is_piece = False
        self.name = "[]"


let = ['a','b','c','d','e','f','g','h']
num = ['1','2','3','4','5','6','7','8']

turns = {"white_moves": 0,
         "black_moves": 0} #to keep track of moves for later

board_positions = {} #square(string): piece(class object)
board_options = {} #piece pos(string): move_options(list)

for l in let:
    for n in num:
        board_positions[l+n] = Empty_Square() #making positions in board_positions dict

def auto_choice(options): #going to decide the automated choice
    return random.choice(options)

class Pieces():
    def __init__(self,position,colour,):
        self.position = position
        self.colour = colour
        self.is_piece = True

    def move(self,pos="random"):
        global board_positions
        options = self.movement()
        if options != None:
            if len(options) != 0:
                if pos.lower() == "random":
                    new_pos = auto_choice(options)
                elif pos in options:
                    new_pos = pos
                else:
                    print("Invalid Move")
                    return False
                board_positions[self.position] = Empty_Square()
                board_positions[new_pos] = self

                self.position = new_pos
                self.has_moved = True
                return True

    def find_pos(self,add_let,add_num):
        current_pos = self.position

        current_let = let.index(current_pos[0])
        current_num = int(current_pos[1])

        new_let = None
        new_num = None

        if current_let + add_let <= 7 and current_let + add_let >= 0:
            new_let = let[current_let + add_let]
        if current_num + add_num <= 8 and current_num + add_num >= 1:
            new_num = str(current_num + add_num)

        if new_let == None or new_num == None:
            return None
        new_pos = new_let + new_num
        if not board_positions[new_pos].is_piece:
            return new_pos
        if board_positions[new_pos].colour == self.colour:
            return None
        else:
            return new_pos
class pawn(Pieces,):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_pawn"
        self.position = position
        self.value = 1
        self.has_moved = False
        self.bare_name = "p"
        self.is_piece = True
    def movement(self):
        global board_positions
        options = []
        i = 1
        if self.colour == "black":
            i = -1
        if self.has_moved == False:
            check = self.find_pos(0,2*i) # 2 moves forward
            if check != None:
                if not board_positions[check].is_piece:
                    options.append(check)

        check =  self.find_pos(0,1*i) #1 move forward
        if check != None:
            if not board_positions[check].is_piece:
                options.append(check)

        check = self.find_pos(1,1*i) #take to the right
        if check != None:
            if board_positions[check].is_piece:
                options.append(check)

        check = self.find_pos(-1,1*i) #take to the left
        if check != None:
            if board_positions[check].is_piece:
                options.append(check)
        return options

class knight(Pieces):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_knight"
        self.position = position
        self.value = 3
        self.has_moved = False
        self.bare_name = "n"
        self.is_piece = True
    def movement(self):
        global board_positions
        options = []

        for a in [1,-1]:
            for b in [2,-2]:
                check = self.find_pos(a,b)
                if check != None:
                    options.append(check)

        for c in [2,-2]:
            for d in [1,-1]:
                check = self.find_pos(c,d)
                if check != None:
                    options.append(check)
        return options

class bishop(Pieces):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_bishop"
        self.position = position
        self.value = 3
        self.has_moved = False
        self.bare_name = "b"
        self.is_piece = True
    def movement(self):
        global board_positions
        options = []
        for a in [1,-1]:
            for b in [1,-1]:
                for i in range(1,8):
                    check = self.find_pos(a*i,b*i)
                    if check == None:
                        break
                    options.append(check)
                    if board_positions[check].is_piece:
                        break
        return options

class rook(Pieces):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_rook"
        self.position = position
        self.value = 5
        self.has_moved = False
        self.bare_name = "r"
        self.is_piece = True
    def movement(self):
        global board_positions
        options = []
        for lum in ["01","10"]:
            a = int(lum[0])
            b = int(lum[1])
            for i in range(1,8):
                check = self.find_pos(a*i,b*i)
                if check == None:
                    break
                options.append(check)
                if board_positions[check].is_piece:
                    break
            for i in range(1,8):
                check = self.find_pos(-a*i,-b*i)
                if check == None:
                    break
                options.append(check)
                if board_positions[check].is_piece:
                    break
        return options

class queen(Pieces):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_queen"
        self.position = position
        self.value = 9
        self.has_moved = False
        self.bare_name = "q"
        self.is_piece = True

    def movement(self):
        global board_positions
        options = []

        for a in [0,1,-1]:
            for b in [0,1,-1]:
                if a or b != 0:
                    for i in range(1,8):
                        check = self.find_pos(a*i,b*i)
                        if check == None:
                            break
                        options.append(check)
                        if board_positions[check].is_piece:
                            break
        return options

class king(Pieces):
    def __init__(self,colour,position):
        self.colour = colour
        self.name = colour + "_king"
        self.position = position
        self.value = 0
        self.has_moved = False
        self.bare_name = "k"
        self.is_piece = True
    def movement(self):
        global board_positions
        options = []
        for a in [0,1,-1,]:
            for b in [0,1,-1]:
                if a != 0 or b != 0:
                    check = self.find_pos(a,b)
                    if check != None:
                        options.append(check)
        return options

def make_board():
    global board_positions
    board_positions["a2"]= pawn("white","a2")
    board_positions["b2"]= pawn("white","b2")
    board_positions["c2"]= pawn("white","c2")
    board_positions["d2"]= pawn("white","d2")
    board_positions["e2"]= pawn("white","e2")
    board_positions["f2"]= pawn("white","f2")
    board_positions["g2"]= pawn("white","g2")
    board_positions["h2"]= pawn("white","h2")

    board_positions["a1"]= rook("white","a1")
    board_positions["h1"]= rook("white","h1")
    board_positions["b1"]= knight("white","b1")
    board_positions["g1"]= knight("white","g1")
    board_positions["c1"]= bishop("white","c1")
    board_positions["f1"]= bishop("white","f1")

    board_positions["e1"]= king("white","e1")
    board_positions["d1"]= queen("white","d1")


    board_positions["a7"] = pawn("black", "a7")
    board_positions["b7"] = pawn("black", "b7")
    board_positions["c7"] = pawn("black", "c7")
    board_positions["d7"] = pawn("black", "d7")
    board_positions["e7"] = pawn("black", "e7")
    board_positions["f7"] = pawn("black", "f7")
    board_positions["g7"] = pawn("black", "g7")
    board_positions["h7"] = pawn("black", "h7")

    board_positions["a8"] = rook("black","a8")
    board_positions["h8"] = rook("black","h8")
    board_positions["b8"] = knight("black","b8")
    board_positions["g8"] = knight("black","g8")
    board_positions["c8"] = bishop("black","c8")
    board_positions["f8"] = bishop("black","f8")

    board_positions["e8"] = king("black","e8")
    board_positions["d8"] = queen("black","d8")

def move_piece(pos,new_pos):
    global board_positions
    global turns
    piece = board_positions[pos]
    if not piece.is_piece:
        print("283")
        return

    if piece.colour != current_move():
        return
        print("288")

    valid = False
    valid = piece.move(new_pos)
    if valid == True:
        if piece.colour == "white":
            turns["white_moves"] += 1
        elif piece.colour == "black":
            turns["black_moves"] += 1

def get_board_status(colour = "all"):
    global board_positions
    global board_options
    for pos, piece in board_positions.items():
        if not piece.is_piece:
            board_options[pos] = []
            continue
        board_options[pos] = piece.movement()
def check():
    global board_positions
    global board_options
    result = False
    options = board_options.copy()
    #print(options)
    for piece, positions in options.items():
        attacker = board_positions[piece]
        if not attacker.is_piece:
            continue
        for pos in positions:
            victim = board_positions[pos]
            if not victim.is_piece:
                continue
            if attacker.colour == victim.colour:
                continue
            if victim.name == "white_king" and attacker.colour == "black":
                print("White king in Check")
                result = True
            if victim.name == "black_king" and attacker.colour == "white":
                print("Black king in Check")
                result = True
        
    return result

def print_board():
    global board_positions
    for pos,piece in board_positions.items():
        print(f"{pos}: {piece.name}")
def draw_board(): #here to modify visual board
    global board_positions
    string = ""
    for n in reversed(num):
        for l in let:
            if not board_positions[l+n].is_piece:
                string += "|   "
            else:
                if board_positions[l+n].colour == "white":
                    string += ("| "+board_positions[l+n].bare_name+" ").upper()
                else:
                    string += "| "+board_positions[l+n].bare_name+" "
        string += "|" + n + "\n"
#        string += "--------------------------------"
        string += "________________________________"
        string += "|\n"
    string += "  a   b   c   d   e   f   g   h"
    print(string)
def current_move():
    global turns
    if turns["white_moves"] == turns["black_moves"]:
        return "white"
    return "black"
def frompt(input):
    result = re.search(r" *([abcdefgh]) *([12345678]) *([abcdefgh]) *([12345678]) *$",input.lower())
    if result == None:
        print("348")
        return None, None
    result = result.groups()
    return result[0] + result[1], result[2] + result[3]

def take_move():
    move = input("Move: ")
    move = move.upper().strip()
    if move == "O-O" or move == "O-O-O":
        castle(move)
        return
    a,b = frompt(move)
    if a == None and b == None:
        print("360")
        return
    move_piece(a,b)
def castle(side):
    print("CASTLING")
def move_from_options(input):
    pass
make_board() #ESSENTIAL
draw_board()

while True:
    #print_board()
    print(f"{current_move()}'s turn to move:")
    check()
    take_move()
    draw_board()
    check()
    get_board_status()
