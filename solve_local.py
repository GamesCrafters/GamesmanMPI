from collections import deque
import sys
import imp
game_module = imp.load_source('game_module', sys.argv[1])

LOSS, WIN, TIE, DRAW, UNDECIDED = "LOSS", "WIN", "TIE", "DRAW", "UNDECIDED"

class Solver:
    solved = False
    known_states = {}
    @staticmethod
    def solve():
        root = GameTree(initial_position)
        queue = deque([root])
        while len(queue) > 0 and Solver.solved == False:
            node = queue.popleft()
            moves = game_module.gen_moves(node.data)
            next_states = []
            for m in moves:
                next = GameTree(game_module.do_move(node.data, m))
                next.parent = node
                next_states.append(next)
            node.children = next_states
            if (game_module.primitive(node.data) != UNDECIDED or node.data in Solver.known_states):
                Solver.record(node)
            else:
                for c in node.children:
                    queue.append(c)
        if (initial_position in Solver.known_states):
            if Solver.known_states[initial_position] == WIN:
                print("Winning position")
            elif Solver.known_states[initial_position] == LOSS:
                print("Losing position")
            elif Solver.known_states[initial_position] == LOSS:
                print("Tie")
            else:
                print("Draw")

        else:
            print("Unable to solve game")

    @staticmethod
    def record(node):
        if (game_module.primitive(node.data) != UNDECIDED):
            Solver.known_states[node.data] = game_module.primitive(node.data)
        elif not(node.data in Solver.known_states):
            all_children_win = True
            for c in node.children:
                if c.data in Solver.known_states:
                    if Solver.known_states[c.data] == LOSS:
                        all_children_win = False
                        Solver.known_states[node.data] = WIN
                        if node.data == initial_position:
                            Solver.solved = True
                else:
                    all_children_win = False
            if all_children_win:
                Solver.known_states[node.data] = LOSS
                if node.data == initial_position:
                            Solver.solved = True
        if node.data != initial_position:
            Solver.record(node.parent)


class GameTree:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

initial_position = game_module.initial_position()
Solver.solve()
