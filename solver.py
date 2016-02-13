#################################################
# 4 - 1 Portion
# TODO: Move out of this file
#################################################

LOSS, WIN, TIE, DRAW = "LOSS", "WIN", "TIE", "DRAW"

initial_position = 4

def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]

def do_move(x, move):
    return x + move

def primitive(x):
    if x <= 0:
        return LOSS

#################################################
# SOLVER PORTION
#################################################

#################################################
# INITIALIZE
# We need to have the rank0 process start everyt-
# hing.
#################################################

from mpi4py import MPI
import hashlib
from Queue import PriorityQueue

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

class GameState:
    """
    Wrapper for the idea of a GameState, not needed
    by the user, just makes things easier for the
    framework.
    """
    def __init__(self, pos, parent):
        self.pos    = pos
        self.parent = parent

    def get_hash(self):
        """
        Returns the appropriate hash of a given GameState object.
        Based off of the value of it's position.
        """
        return int(hashlib(self.pos).hexdigest(), 16) % size


    def expand(self):
        """
        Takes the current position and generates the
        children positions.
        """
        # Raw, in other words, not a GameState object.
        raw_states = map(lambda m: do_moves(pos, m), gen_moves(pos))
        # Wrapped, in other words, a GameState object.
        wrapped_states = map(lambda m: GameState(m, rank))
        return wrapped_states

class Job:
    """
    A job is a game state, parent, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """
    def __init__(self, state, parent, priority=0):
        self.state = state
        self.parent = parent
        self.priority = priority

    def __cmp__(self, other):
        """ 
        Compares two Job objects based off the priority
        they have.
        """
        return cmp(self.priority, other.priority)

class Process:
    """
    Class that defines the behavior what each process should do
    """

    def run(self):
        """
        Main loop for each process
        """
        # TODO
        pass

    def __init__(self, rank):
        self.rank = rank
        self.work = PriorityQueue()
        self.resolved = {}
        # Keep a list of sent requests, and received requests,
        # if sending fails, should be able to handle it some-
        # how.
        # As for recieving, should test them when appropriate
        # in the run loop.
        self.sent = []
        self.received = []
        # Main process will terminate everyone by bcasting the value of
        # finished to True.
        self.finished = False

    def add_job(self, job):
        self.work.put(job)

    def lookup(self, game_state):
        """
        Takes a GameState object and determines if it is in the 
        resolved list. Returns the result if this is the case, None
        otherwise.
        """
        return resolved[game_state.pos]

    def distribute(self, game_state):
        """
        Given a gamestate distributes the results to the appropriate
        children.
        """
        children = game_state.expand()
        # Keep a list of the requests made by isend. Something may
        # fail, so we will need to worry about error checking at
        # some point.
        for child in children:
            self.sent.append(comm.isend(child, dest = child.get_hash()))

    def check_for_updates(self):
        """
        Checks if there is new data from other Processes that needs to
        be received and prepares to recieve it if there is any new data.
        Returns True if there is new data to be recieved.
        Returns None if there is nothing to be recieved.
        """
        # Probe for any sources
        if comm.iprobe(source=comm.MPI_ANY_SOURCE):
            # If there are sources recieve them.
            self.received.append(comm.irecv(source=comm.MPI_ANY_SOURCE))
            return True
        return None

process = Process(rank)
if process.rank == 0:
    initial_gamestate = GameState(initial_position, process.rank)
    initial_job = Job(process.rank, initial_gamestate)
    process.add_job(initial_job)

process.run()

comm.Barrier()
