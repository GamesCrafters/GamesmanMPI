#################################################
# 4 - 1 Portion
#################################################

import src.utils


@src.utils.encode_int
def initial_position():
    return 4


@src.utils.encode_int
def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]


@src.utils.decode_int
@src.utils.encode_int
def do_move(x, move):
    return x + move


@src.utils.decode_int
def primitive(x):
    if x <= 0:
        return src.utils.LOSS
    else:
        return src.utils.UNDECIDED
