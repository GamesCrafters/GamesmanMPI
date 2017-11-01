Building Game Modules
=====================

The GamesmanMPI solver is a powerful tool, but without games to solve, it's an engine without a chassis. This document will explain how to build game modules compatible with the GamesmanMPI solver.

Game Module Specs
^^^^^^^^^^^^^^^^^

Currently, the GamesmanMPI solver only supports Python game implementations.

The game file requires four attributes: ``initial_position``, ``gen_moves``, ``do_move``, and ``primitive``.

The game file also requires the attributes ``LOSS``, ``WIN``, ``TIE``, ``DRAW``. These attributes serve as primitives describing the game result of a position.  

initial_position()
^^^^^^^^^^^^^^^^^^

The function ``initial_position`` returns the game's starting position.

gen_moves(position)
^^^^^^^^^^^^^^^^^^^

``gen_moves`` is a function that takes as input a game position, ``position``. It returns a list of moves that can be taken from ``position``.

do_move(position, move)
^^^^^^^^^^^^^^^^^^^^^^^

``do_move`` is a function that takes as input a game position, ``position``, and a move, ``move``. It returns the game position that results from making ``move`` from ``position``.

primitive(position)
^^^^^^^^^^^^^^^^^^^

``primitive`` is a function that takes as input a game position, ``position``. It returns whether ``position`` is a ``LOSS``, ``WIN``, ``TIE``, or ``DRAW``.
