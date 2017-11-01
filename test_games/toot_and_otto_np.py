import src.utils
from mpi4py import MPI
import numpy as np

toot = np.array([1,2,2,1])
otto = np.array([2,1,1,2])

#feel free to change the height to reduce the problem size
height = 4
length = 6

initial_pos = np.zeros((height+1,length), dtype = np.int8)
# top row is number of T for P1, O for P1, T for P2, O for P3, 
# which players turn it is
# assumes that player 1 always goes for toot
initial_pos[0,] = [6, 6, 6, 6, 1, 1]

def initial_position():
	return initial_pos

def print_board(board):
	#prints the current board with helpful indices on the left and the bottom
	print(board[1:,:])

# def board_is_full(board):
# 	bool_pieces = (board[1:height+1,]  == 0)
# 	return bool_pieces.sum() == 0

def board_is_full(board):
	return np.count_nonzero(board[1:height+1,:]) == height*length

def check_for_words(board):
	# first entry is number of toot's, second is otto's
	score = np.zeros(2, dtype = np.int8)
	for x in range(1,height+1):
		for y in range(length):
			if board[x,y] != 0:
				word = None
				if board[x,y] == 1:
					word = toot
					index = 0
				elif board[x,y] == 2:
					word = otto
					index = 1
				if word is None:
					continue

				if word_test(board, x+1, y, word, 1, 0, 1):
					score[index] += 1
				if word_test(board, x, y+1, word, 0, 1, 1):
					score[index] += 1
				if word_test(board, x+1, y+1, word, 1, 1, 1):
					score[index] += 1
				if word_test(board, x+1, y-1, word, 1, -1, 1):
					score[index] += 1
	return score

def word_test(board, x, y, word, dx, dy, char_pos_in_word):
	if char_pos_in_word == 4:
		return True
	if x >= height+1 or y >= length or x < 1 or y < 0:
		return False
	if board[x,y] != word[char_pos_in_word]:
		return False
	return word_test(board, x+dx, y+dy, word, dx, dy, char_pos_in_word+1)

#assumes that player1 goes for toot and player2 goes for otto

#assumes that if
#takes in a state parameter which is a numpy array
#returns a string of the options win, loss, tie, draw, unkwown

def primitive(board):
	score = check_for_words(board)
	if score[1] >= 1 and score[0] >= 1:
		return src.utils.TIE
	if score[0] >= 1:
		print("toot wins")
		if board[0,4] == 1:
			return src.utils.WIN
		return src.utils.LOSS
	elif score[0] >= 1:
		print("otto wins")
		if board[0,4] == 1:
			return src.utils.LOSS
		return src.utils.WIN
	if board_is_full(board):
		return src.utils.LOSS
	else:
		return src.utils.UNDECIDED

#action is defined as a tuple with the letter, and a board location
#example of an action: (2, (2,3))

#takes in the parameter state, a State object
#returns a list of actions that are valid to be applied to the parameter state
def gen_moves(board):
	hand = np.append(board[0,2],board[0,3])
	if board[0,4] == 1:
		hand = np.append(board[0,0],board[0,1])

	possible_actions = []
	for y in range(length):
		x = height
		while x > 0 and not board[x,y] == 0:
			x -= 1
		if x > 0:
			for i in range(2):
				if hand[i]>0:
					possible_actions.append((i+1, (x,y)))
	return possible_actions

#returns the successor given by applying the parameter action to the parameter state
#the parameter action is a tuple with the letter, and a board location
#the parameter state is a State object
#must pass in a valid state and a valid action for that state, does not check
def do_move(board, action):
	# valid_moves = gen_moves(board)
	# if action not in valid_moves:
	# 	print 'INVALID MOVE'
	# 	return board

	successor = np.copy(board)
	piece, loc = action

	successor[loc] = piece
	if successor[0,4] == 1 and piece == 1:
		successor[0,0] -= 1
	elif successor[0,4] == 1 and piece == 2:
		successor[0,1] -= 1
	elif successor[0,4] == 2 and piece == 1:
		successor[0,2] -= 1
	else:
		successor[0,3] -= 1

	successor[0,4] = 1 + (successor[0,4] % 2)
	return successor


#helpful prints for reference, understanding the code, and debugging
def example():
	print 'the initial position is the following:'
	print_board(initial_pos)
	print 'hand1T=' + str(initial_pos[0,0])
	print 'hand1O=' + str(initial_pos[0,1])
	print 'hand2T=' + str(initial_pos[0,2])
	print 'hand2O=' + str(initial_pos[0,3])
	print 'firstPlayerTurn=' + str(initial_pos[0,4]==1)
	possible_actions = gen_moves(initial_pos)
	print 'these are the possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(initial_pos)

	board_turn_1 = do_move(initial_pos, possible_actions[6])
	print 'this is the state after a move has been made'
	print_board(board_turn_1)
	print 'hand1T=' + str(board_turn_1[0,0])
	print 'hand1O=' + str(board_turn_1[0,1])
	print 'hand2T=' + str(board_turn_1[0,2])
	print 'hand2O=' + str(board_turn_1[0,3])
	print 'firstPlayerTurn=' + str(board_turn_1[0,4]==1)
	possible_actions = gen_moves(board_turn_1)
	print 'New possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(board_turn_1)

	board = do_move(board_turn_1, possible_actions[4])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(board)

	board = do_move(board, possible_actions[5])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions length:'
	print len(possible_actions)
	print 'primitive value:'
	print primitive(board)

	board = do_move(board, possible_actions[5])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions length:'
	print len(possible_actions)
	print 'primitive value:'
	print primitive(board)

	board = do_move(board, possible_actions[4])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions length:'
	print len(possible_actions)
	print 'primitive value:'
	print primitive(board)




