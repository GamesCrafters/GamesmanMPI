import gamesman
import numpy as np

#state is simply a 3x3 numpy array 
#0 is empty, 1 and 2 correspond to the players
initialPosition = np.zeros((3,3), dtype=np.int8)

#action is tuple: (player, (x,y))
#it returns a list of all valid action tuples
def generateMoves(state):
	possibleActions = []
	currPlayer = 1
	#determine which players turn it is
	num1 = 0
	num2 = 0
	for x in range(3):
		for y in range(3):
			if state[x][y] == 1:
				num1 += 1
			if state[x][y] == 2:
				num2 += 1
	if num1 > num2:
		currPlayer = 2
	#determine the possible actions
	for x in range(3):
		for y in range(3):
			if state[x][y] == 0:
				possibleActions.append((currPlayer, (x,y)))
	return possibleActions

#executes the move given by parameter action on the parameter state
#returns the successor state generated
def doMove(state, action):
	successor = np.copy(state)
	player, loc = action
	successor[loc[0],loc[1]] = player
	return successor

#returns the gamesman values of WIN, TIE, or UNDECIDED depending on the state
def primitive(state):
	def connectionTest(x, y, player, dx, dy, numPiecesTillConnection):
		if numPiecesTillConnection <= 0:
			return True
		if x not in range(3) or y not in range(3) or state[x][y] != player:
			return
		return connectionTest(x+dx, y+dy, player, dx, dy, numPiecesTillConnection-1)

	board_full = True
	for x in range(3):
		for y in range(3):
			if not state[x][y] == 0:
				if connectionTest(x+1, y, state[x][y], 1, 0, 2) or connectionTest(x, y+1, state[x][y], 0, 1, 2) \
				or connectionTest(x+1, y+1, state[x][y], 1, 1, 2) or connectionTest(x+1, y-1, state[x][y], 1, -1, 2):
					return gamesman.LOSE
			else:
				board_full = False
	if board_full:
		return gamesman.TIE
	return gamesman.UNDECIDED


#can help optimize the solver by also knowing the lastAction
def primitiveLastAction(state, lastAction):
	def connectionTest(x, y, player, dx, dy, numPiecesTillConnection):
		if numPiecesTillConnection <= 0:
			return True
		if x not in range(3) or y not in range(3) or state[x][y] != player:
			return
		return connectionTest(x+dx, y+dy, player, dx, dy, numPiecesTillConnection-1)

	player, loc = lastAction
	x, y = loc

	if connectionTest(x+1, y, player, 1, 0, 2) or connectionTest(x, y+1, player, 0, 1, 2) \
	or connectionTest(x+1, y+1, player, 1, 1, 2) or connectionTest(x+1, y-1, player, 1, -1, 2) \
	or connectionTest(x-1, y+1, player, -1, 1, 2) or connectionTest(x-1, y-1, player, -1, -1, 2) \
	or connectionTest(x-1, y, player, -1, 0, 2) or connectionTest(x, y-1, player, 0, -1, 2):
		return gamesman.LOSE

	if np.count_nonzero(state) == 0:
		return gamesman.TIE
	return gamesman.UNDECIDED

#proves that all functions are working as they should be
def test():
	print "position:"
	print initialPosition
	print "primitive:"
	print primitive(initialPosition)
	print "possible moves:"
	posMoves = generateMoves(initialPosition)
	print posMoves

	print "position:"
	s = doMove(initialPosition, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves

	print "position:"
	s = doMove(s, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves

	print "position:"
	s = doMove(s, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves

	print "position:"
	s = doMove(s, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves

	print "position:"
	s = doMove(s, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves

	print "position:"
	s = doMove(s, posMoves[2])
	print s
	print "primitive:"
	print primitive(s)
	print primitiveLastAction(s, posMoves[2])
	print "possible moves:"
	posMoves = generateMoves(s)
	print posMoves
