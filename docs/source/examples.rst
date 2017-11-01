Game Examples
=============

Four-to-One
^^^^^^^^^^^
::

    import src.utils
    
    def initial_position():
        return 4

    def gen_moves(x):
        if x == 1:
            return [-1]
        return [-1, -2]

    def do_move(x, move):
        return x + move

    def primitive(x):
        if x <= 0:
            return src.utils.LOSS
        else:
            return src.utils.UNDECIDED
