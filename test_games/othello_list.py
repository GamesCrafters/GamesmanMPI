import src.utils
from mpi4py import MPI
import numpy as np

height, length = 8, 8

def initial_position():
	#1 is black, 2 is white, players turn bit is the number in position (0,0), black goes first
	#position (0,1) is used as a counter for the number of passes in a row
	initial_pos = [[0 for x in range(height)] for y in range(length)]
	initial_pos[height/2-1][length/2-1] = 2
	initial_pos[height/2-1][length/2] = 1
	initial_pos[height/2][length/2-1] = 1
	initial_pos[height/2][length/2] = 2
	pturn, pcount = 1,0
	return [initial_pos, pturn, pcount]

board_state_element_type = MPI.CHAR

def print_board(board):
	#prints the current board and players turn
	for i in range(height):
		print(board[0][i])
	print("Player's turn: ", board[1])

def primitive(board):
	def determine_winner():
		black_count = 0
		white_count = 0
		for x in range(height):
			for y in range(length):
				if board[0][x][y] == 1:
					black_count += 1
				elif board[0][x][y] == 2:
					white_count += 1
		if black_count == white_count:
			return scr.utils.TIE
		if (black_count > white_count) ^ (board[1] == 1):
			return src.utils.LOSS
		return src.utils.WIN

	non_zero_count = 0

	for x in range(height):
		for y in range(length):
			if board[0][x][y] != 0:
				non_zero_count+=1

	if non_zero_count == height*length or board[2] >= 2:
		return determine_winner()

	return src.utils.UNDECIDED

#generates all possible moves of the parameter board and returns a list of them,
#if there are no possible moves, returns a list with one item that is None
#In other words, a pass is implemented by a move with None as a value instead of an (x,y) tuple
def gen_moves(board):
	def legit_move(x,y):
		if board[0][x][y] != 0:
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
		opponent_color = 1 + (board[1] % 2)
		if first:
			if board[0][x][y] != opponent_color:
				return False
			return legit_helper(x+dx,y+dy,dx,dy,False)
		if board[0][x][y] == board[1]:
			return True
		if board[0][x][y] == opponent_color:
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

#param board: numpy array of the board and the 0 row including the players turn and numPasses in a row
#param move: action as a tuple with the position that the player moves to
#returns the successor state as a numpy array e to the board
def do_move(board, move):
	def flip_pieces(state,x,y):
		state[0][x][y] = 1 + ((board[1] + 1) % 2)
		dx = -1
		while dx <= 1:
			dy = -1
			while dy <= 1:
				if not (dx == 0 and dy == 0):
					flip_helper(state,x+dx,y+dy,dx,dy)
				dy += 1
			dx += 1

	def flip_helper(state,x,y,dx,dy):
		if x >= height or y >= length or x < 0 or y < 0:
			return
		opponent_color = 1 + (board[1] % 2)
		if state[0][x][y] != opponent_color:
			return
		to_flip = [(x, y)]
		flip_helper2(state,x+dx,y+dy,dx,dy,to_flip)

	def flip_helper2(state,x,y,dx,dy,to_flip):
		if x >= height or y >= length or x < 0 or y < 0:
			return
		if state[0][x][y] == 1 + ((board[1] + 1) % 2):
			for i,j in to_flip:
				state[0][i][j] = 1 + ((board[1] + 1) % 2)
			return
		opponent_color = 1 + (board[1] % 2)
		if state[0][x][y] == opponent_color:
			to_flip.append((x,y))
			flip_helper2(state,x+dx,y+dy,dx,dy, to_flip)

	successor = board[:]
	successor[0] = board[0][:]
	#account for pass case
	if move == None:
		successor[2] += 1
		return successor
	successor[2] = 0 # Since we didn't pass, reset the pass count

	x, y = move
	flip_pieces(successor, x, y)
	successor[1] = 1 + (successor[1] % 2)
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
