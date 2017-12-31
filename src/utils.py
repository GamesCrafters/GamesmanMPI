from functools import reduce
from hashlib import md5

WIN, LOSS, TIE, DRAW, UNDECIDED = 0, 1, 2, 3, 4
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW) # To remove
DWULT                           = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py


# Used for logging/display purposes
STATE_MAP = {
        WIN:"win",
        LOSS:"loss",
        TIE:"tie",
        DRAW:"draw",
        UNDECIDED:"undecided"
}


def encode_int(f):
    """
    All methods must return an encodable object to be saved to a database.
    Functions that return an integer do not satisfy this condition. this
    decorator takes a function that returns integers and changes it to
    return strings.
    """
    def encoded_f(*args):
        result = f(*args)
        if type(result) is list:
            return map(str, result)
        return str(result)
    return encoded_f


def decode_int(f):
    """
    All methods must have an encodable object, ints are not encodable
    calling decode changes encoded (now string objects) to be just
    integers now.
    """
    def decoded_f(*args):
        decoded_args = [int(arg) for arg in args]
        return f(*decoded_args)
    return decoded_f


def negate(state):
    """
    'Negate' a state.
    In otherwords, a WIN becomes a LOSS, otherwise preserve the states:
    TIE -> TIE
    DRAW -> DRAW
    UNDECIDED -> UNDECIDED
    """
    neg = (1, 0, 2, 3, 4)
    return neg[state]


def to_str(state):
    """
    Give an intuitive string WIN, LOSS, TIE, DRAW, UNDECIDED representation
    for a state.
    """
    str_rep = ("WIN", "LOSS", "TIE", "DRAW", "UNDECIDED")
    return str_rep[state]


def reduce_singleton(function, data):
    """
    Applies a function to *1* or more elements of a list
    as opposed to two or more for the standard reduce.
    """
    if len(data) == 1:
        return function(data[0], None)
    return reduce(function, data)


def get_hash(gamestate_pos, world_size):
        """
        Returns the appropriate hash of a given GameState position and world size.
        """
        return int(
            md5(str(gamestate_pos).encode('utf-8')).hexdigest(),
            16
        ) % world_size


def argmin(tup1, tup2, index):
        """
        Returns the argmin tuple
        """
        if tup1[index] <= tup2[index]:
            return tup1
        return tup2


def argmax(tup1, tup2, index):
        """
        Returns the argman tuple
        """
        if tup1[index] >= tup2[index]:
            return tup1
        return tup2