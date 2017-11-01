import src.utils

WIDTH = 3
HEIGHT = 3

BORDER = 'B'
X = 'X'
O = 'O'
BLANK = '_'

def initial_position():
    return BLANK * WIDTH * HEIGHT

def to_loc(i):
    x = i % WIDTH
    y = i // WIDTH
    return (x, y)

def to_index(loc):
    x, y = loc
    return x + (y * WIDTH)

def find_spaces(pos):
    for i, p in enumerate(pos):
        if p == BLANK:
            yield i

def find_non_spaces(pos):
    for i, p in enumerate(pos):
        if p != BLANK:
            yield i

def get_piece(pos, x, y):
    if x < 0 or x > 2 or y < 0 or y > 2:
        return 'B'
    else:
        return pos[to_index((x, y))]

def get_player(pos):
    if pos.count(O) >= pos.count(X):
        return X
    else:
        return O

def primitive(pos):
    '''
    >>> primitive(BLANK * 9)
    'undecided'
    >>> primitive(X * 9)
    'lose'
    >>> primitive(X + X + O +
    ...           O + O + X +
    ...           X + O + X)
    'tie'
    >>> primitive(X + X + X +
    ...           O + O + X +
    ...           X + O + O)
    'lose'
    >>> primitive(O + X + X +
    ...           O + O + X +
    ...           X + O + X)
    'lose'
    >>> primitive(X + O + O +
    ...           O + X + X +
    ...           X + O + X)
    'lose'
    >>> primitive(O + O + X +
    ...           O + X + X +
    ...           X + X + O)
    'lose'
    '''
    for x, y in [to_loc(i) for i in
                 find_non_spaces(pos)]:
        piece = get_piece(pos, x, y)
        if ((get_piece(pos, x + 1, y) == piece and
             get_piece(pos, x + 2, y) == piece) or
            (get_piece(pos, x, y + 1) == piece and
             get_piece(pos, x, y + 2) == piece) or
            (get_piece(pos, x + 1, y + 1) == piece and
             get_piece(pos, x + 2, y + 2) == piece) or
            (get_piece(pos, x - 1, y + 1) == piece and
             get_piece(pos, x - 2, y + 2) == piece)):
            return src.utils.LOSS
    if BLANK in pos:
        return src.utils.UNDECIDED
    else:
        return src.utils.TIE

def gen_moves(pos):
    '''
    >>> len(generateMoves('_' * 9))
    9
    >>> generateMoves('_' * 9)[:3]
    [(0, 0), (1, 0), (2, 0)]
    >>> generateMoves('_' * 9)[3:6]
    [(0, 1), (1, 1), (2, 1)]
    >>> generateMoves('_' * 9)[6:]
    [(0, 2), (1, 2), (2, 2)]
    >>> generateMoves('XOX'
    ...               'OXO'
    ...               'X__')
    [(1, 2), (2, 2)]
    '''
    return [to_loc(i) for i in find_spaces(pos)]

def do_move(position, move):
    '''
    >>> doMove('_', (0, 0))
    'X'
    >>> doMove('X_O', (1, 0))
    'XXO'
    >>> doMove('XOX'
    ...        'OXO'
    ...        'X__', (1, 2))
    'XOXOXOXO_'
    >>> doMove('XOX'
    ...        'OXO'
    ...        'X__', (2, 2))
    'XOXOXOX_O'
    >>> doMove('XOX'
    ...        'OXO'
    ...        '___', (0, 2))
    'XOXOXOX__'
    '''
    player = get_player(position)
    index = to_index(move)
    return position[:index] + player + position[index + 1:]
