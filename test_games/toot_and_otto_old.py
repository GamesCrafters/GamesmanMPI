#Toot and Otto game implementation for Gamescrafters

#defines the state object for the toot and otto game
#state keeps track of 4 things:
#the player whose turn it is, the board, and both players hands
#additional methods are helper methods for the neccessary solver functions and
class State(object):
    """Base State class"""
    dash = "-"
    T = "T"
    O = "O"
    toot = T+O+O+T
    otto = O+T+T+O
    board_dimension_height = 4
    board_dimension_length = 4
    diagonal_connections_allowed = True

    def __init__(self):
        self.first_player_turn = True
        self.pieces = {}
        for x in range(State.board_dimension_length):
            for y in range(State.board_dimension_height):
                self.pieces[(x,y)] = State.dash

        self.hand1 = {}
        self.hand2 = {}
        self.hand1[State.T] = 6
        self.hand1[State.O] = 6
        self.hand2[State.T] = 6
        self.hand2[State.O] = 6

    #returns a new State object that is a copy of self
    def state_copy(self):
        copy = State()
        copy.first_player_turn = self.first_player_turn
        copy.pieces = self.pieces.copy()
        copy.hand1 = self.hand1.copy()
        copy.hand2 = self.hand2.copy()
        return copy

    #prints the current board with helpful indices on the left and the bottom
    def printBoard(self):
        y = State.board_dimension_height - 1
        while y >= 0:
            partial_string = str(y) + " | "
            for x in range(State.board_dimension_length):
                partial_string += self.pieces[(x, y)] + " "
            y -= 1
            print(partial_string)

        second_bottom = "    "
        for x in range(State.board_dimension_length):
            second_bottom += "__"
        print(second_bottom)
        bottom_line = "    "
        for x in range(State.board_dimension_length):
            bottom_line += str(x) + " "
        print(bottom_line)

    def board_is_full(self):
        for x in range(State.board_dimension_length):
            for y in range(State.board_dimension_height):
                if self.pieces[(x,y)] == State.dash:
                    return False
        return True

    #returns the score dictionary for the number of words, toot and otto
    def check_for_words(self):
        score = {}
        score[State.toot] = 0
        score[State.otto] = 0
        for x in range(self.board_dimension_length):
            for y in range(self.board_dimension_height):
                if self.pieces[(x,y)] != State.dash:
                    word = None
                    if self.pieces[(x,y)] == State.T:
                        word = State.toot
                    elif self.pieces[(x,y)] == State.O:
                        word = State.otto
                    if not word:
                        continue

                    if self.word_test(x+1, y, word, 1, 0, 1):
                        score[word] += 1
                    if self.word_test(x, y+1, word, 0, 1, 1):
                        score[word] += 1
                    if self.word_test(x+1, y+1, word, 1, 1, 1):
                        score[word] += 1
                    if self.word_test(x+1, y-1, word, 1, -1, 1):
                        score[word] += 1
        return score

    #helper function for check_for_words
    def word_test(self, x, y, word, dx, dy, char_pos_in_word):
        if char_pos_in_word >= 4:
            return True
        if self.pieces.get((x,y)) != word[char_pos_in_word]:
            return False
        return self.word_test(x+dx, y+dy, word, dx, dy, char_pos_in_word+1)


#Implementation of the neccessary functions for the solver

#assumes that player1 goes for toot and player2 goes for otto

#assumes that if the score is tied, continue playing no matter how many matches
#takes in a state parameter which is a State object
#returns a string of the options win, loss, tie, draw, unkwown
def primitive(state):
    score = state.check_for_words()
    if score[State.toot] > score[State.otto]:
        print("toot wins")
        if state.first_player_turn:
            return 'win'
        return 'loss'
    elif score[State.toot] < score[State.otto]:
        print("otto wins")
        if state.first_player_turn:
            return 'loss'
        return 'win'
    else:
        if state.board_is_full():
            return 'tie'
        else:
            return 'unknown'

#action is defined as a tuple with the letter, and a board location
#example of an action: ("T", (2,3))

#takes in the parameter state, a State object
#returns a list of actions that are valid to be applied to the parameter state
def gen_moves(state):
    hand = state.hand2
    if state.first_player_turn:
        hand = state.hand1

    possible_actions = []
    for x in range(State.board_dimension_length):
        y = 0
        while not state.pieces[(x,y)] == State.dash and y < State.board_dimension_height:
            y += 1
        if y < State.board_dimension_height:
            for piece in hand:
                if hand[piece]>0:
                    possible_actions.append((piece, (x,y)))
    return possible_actions

#returns the successor given by applying the parameter action to the parameter state
#the parameter action is a tuple with the letter, and a board location
#the parameter state is a State object
#must pass in a valid state and a valid action for that state, does not check
def do_move(state, action):
    successor = state.state_copy()
    piece, loc = action

    successor.first_player_turn = not state.first_player_turn
    successor.pieces[(loc)] = piece
    if state.first_player_turn:
        successor.hand1[piece] -= 1
    else:
        successor.hand2[piece] -= 1
    return successor

initial_position = lambda: State()

#helpful prints for reference, understanding the code, and debugging
"""
def example():
    print 'the initial position is the following:'
    init_pos.printBoard()
    print 'hand1=' + str(init_pos.hand1)
    print 'hand2=' + str(init_pos.hand2)
    print 'first_player_turn=' + str(init_pos.first_player_turn)
    possible_actions = gen_moves(init_pos)
    print 'these are the possible actions:'
    print possible_actions
    print 'primitive value:'
    print primitive(init_pos)
    s = make_move(init_pos, possible_actions[6])
    print 'this is the state after a move has been made'
    s.printBoard()
    print 'hand1=' + str(s.hand1)
    print 'hand2=' + str(s.hand2)
    print 'first_player_turn=' + str(s.first_player_turn)
    possible_actions = gen_moves(s)
    print 'New possible actions:'
    print possible_actions
    print 'primitive value:'
    print primitive(s)
"""
