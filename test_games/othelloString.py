import src.utils
import collections
import numpy as np

#feel free to adjust height and length to reduce problem size
height, length = 8,8

def initial_position():
    #state is a string with each row concatenated together and the player's turn and the number of passes in a row added on the end
    #1 is black, 2 is white, 
    #black goes first
    initial_pos = ""
    for i in range(height*length):
        initial_pos += "0"
    initial_pos += "10"
    initial_pos = initial_pos[:(height/2-1)*length+length/2-1] + "2" + initial_pos[(height/2-1)*length+length/2:]
    initial_pos = initial_pos[:(height/2-1)*length+length/2] + "1" + initial_pos[(height/2-1)*length+length/2+1:]
    initial_pos = initial_pos[:(height/2)*length+length/2-1] + "1" + initial_pos[(height/2)*length+length/2:]
    initial_pos = initial_pos[:(height/2)*length+length/2] + "2" + initial_pos[(height/2)*length+length/2+1:]
    return initial_pos

def print_board(state):
    #prints the current board and players turn
    print "Player's turn: ", state[height*length]
    for x in range(height):
        print state[x*length:x*length+length]

#returns the primitive value of the parameter board
def primitive(board):
    def determine_winner():
        black_count = 0
        white_count = 0
        for x in range(height):
            for y in range(length):
                if board[x*length+y] == '1':
                    black_count += 1
                elif board[x*length+y] == '2':
                    white_count += 1
        if black_count == white_count:
            return src.utils.TIE
        if black_count > white_count:
            if board[height*length] == '1':
                return src.utils.WIN
            return src.utils.LOSS
        if board[height*length] == '1':
            return src.utils.LOSS
        return src.utils.WIN

    if not '0' in board[:-2]:
        return determine_winner()
    if int(board[height*length+1]) >= 2:
        return determine_winner()
    return src.utils.UNDECIDED

#generates all possible moves of the parameter board and returns a list of them,
#if there are no possible moves, returns a list with one item that is None
#In other words, a pass is implemented by a move with None as a value instead of an (x,y) tuple
def gen_moves(board):
    def legit_move(x,y):
        if board[x*length+y] != '0':
            return False
        dx = -1
        while dx <= 1:
            dy = -1
            while dy <= 1:
                if not (dx == 0 and dy == 0):
                    if legit_helper(x+dx,y+dy,dx,dy,True):
                        return True
                dy += 1
            dx += 1

    def legit_helper(x,y,dx,dy,first):
        if x >= height or y >= length or x < 0 or y < 0:
            return False
        opponent_color = str(1 + (int(board[height*length]) % 2))
        if first:
            if board[x*length+y] != opponent_color:
                return False
            return legit_helper(x+dx,y+dy,dx,dy,False)
        if board[x*length+y] == board[height*length]:
            return True
        if board[x*length+y] == opponent_color:
            return legit_helper(x+dx,y+dy,dx,dy,False)
        return False

    possible_moves = []
    for x in range(height):
        for y in range(length):
            if legit_move(x,y):
                possible_moves.append((x,y))
    #pass case
    if len(possible_moves) == 0:
        possible_moves.append(None)
    return possible_moves

#param board: string with each row concatenated togther and the player's turn and the number of passes in a row added on the end
#param move: action as a tuple with the position that the player moves to
#returns the successor state as a string in the same format as the parameter board
def do_move(board, move):
    def flip_pieces(state,x,y):
        state = state[:x*length+y] + board[height*length] + state[x*length+y+1:]
        dx = -1
        while dx <= 1:
            dy = -1
            while dy <= 1:
                if not (dx == 0 and dy == 0):
                    s = flip_helper(state,x+dx,y+dy,dx,dy)
                    if s:
                        state = s
                dy += 1
            dx += 1
        return state

    def flip_helper(state,x,y,dx,dy):
        if x >= height or y >= length or x < 0 or y < 0:
            return
        opponent_color = str(1 + (int(board[height*length]) % 2))
        if state[x*length+y] != opponent_color:
            return
        to_flip = []
        to_flip.append((x,y))
        return flip_helper2(state,x+dx,y+dy,dx,dy,to_flip)

    def flip_helper2(state,x,y,dx,dy,to_flip):
        if x >= height or y >= length or x < 0 or y < 0:
            return
        if state[x*length+y] == board[height*length]:
            for i,j in to_flip:
                state = state[:i*length+j] + board[height*length] + state[i*length+j+1:]
            return state
        opponent_color = str(1 + (int(board[height*length]) % 2))
        if state[x*length+y] == opponent_color:
            to_flip.append((x,y))
            return flip_helper2(state,x+dx,y+dy,dx,dy, to_flip)
        return

    successor = board[:]
    successor = successor[:height*length] + str(1 + (int(board[height*length]) % 2)) + successor[height*length+1:]
    #account for pass case
    if move == None:
        successor = successor[:height*length+1] + str(int(successor[height*length+1])+1)
        return successor
    successor = successor[:height*length+1] + '0'

    x, y = move
    successor = flip_pieces(successor, x, y)
    return successor




def example():
    print('the initial position is the following:')
    print_board(initial_position())
    possible_actions = gen_moves(initial_position())
    print('these are the possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(initial_position()))

    board_turn_1 = do_move(initial_position(), possible_actions[2])
    print_board(board_turn_1)
    possible_actions = gen_moves(board_turn_1)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board_turn_1))

    board = do_move(board_turn_1, possible_actions[0])
    print_board(board)
    possible_actions = gen_moves(board)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board))

    board = do_move(board, possible_actions[3])
    print_board(board)
    possible_actions = gen_moves(board)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board))

    board = do_move(board, possible_actions[1])
    print_board(board)
    possible_actions = gen_moves(board)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board))

    board = do_move(board, possible_actions[2])
    print_board(board)
    possible_actions = gen_moves(board)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board))

    board = do_move(board, possible_actions[4])
    print_board(board)
    possible_actions = gen_moves(board)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(board))

