#!/usr/bin/env python3

from mpi4py import MPI
import imp
import argparse

import src.utils

parser = argparse.ArgumentParser()
parser.add_argument(
    'game_file',
    help='Game to solve for.'
)

parser.add_argument(
    '--debug',
    help='Enables or disables logging.',
    action='store_true'
)

parser.add_argument(
    '-sd',
    '--statsdir',
    help='Location to store statistics about game.',
    action='store'
)

parser.add_argument(
    '--custom',
    help='Specifies custom file to modify provided game file.'
)

parser.add_argument(
    '--init_pos',
    help='Initial position to start at for the game. If none is specified, the default is used.'
)

args = parser.parse_args()

comm = MPI.COMM_WORLD

# May be later modified for debugging purposes.
# Because comm.send is read only we need to make a
# new variable.

isend = comm.isend
recv = comm.recv
abort = comm.Abort

# Load file and give it to each process.
game_module = imp.load_source('game_module', args.game_file)
src.utils.game_module = game_module

# Make sure every process has a copy of this.
comm.Barrier()

# Now it is safe to import the classes we need as everything
# has now been initialized correctly.
from src.game_state import GameState  # NOQA
from src.new_job import Job  # NOQA
from src.new_process import Process  # NOQA
import src.debug  # NOQA


def validate(mod):
    try:
        getattr(mod, 'initial_position')
        getattr(mod, 'do_move')
        getattr(mod, 'gen_moves')
        getattr(mod, 'primitive')
    except AttributeError as e:
        print('Could not find method'), e.args[0]
        raise

# Make sure the game is properly defined
validate(src.utils.game_module)

def load_custom(mod):
    try:
        custom = imp.load_source('custom', mod)
        return custom
    except AttributeError as e:
        print('Custom file with new initial position not specified. '
              'Using default initial position instead.')
        return None
    except FileNotFoundError as e:
        print('Custom file was not found. '
              'Using default initial position instead.')
        return None

def load_init_pos(mod):
    try:
        init_pos = getattr(custom, mod)
        return init_pos
    except AttributeError as e:
        print('Initial position was not found in custom file. '
              'Using default initial position instead.')
        return None

# Patch the game_module as necessary
if args.init_pos:
    custom = load_custom(args.custom)
    if custom != None:
        init_pos = load_init_pos(args.init_pos)
        if init_pos != None:
            src.utils.game_module.initial_position = init_pos

# Make sure every process has a copy of this.
comm.Barrier()

# Now it is safe to import the classes we need as everything
# has now been initialized correctly.
from src.game_state import GameState  # NOQA
from src.job import Job  # NOQA
from src.process import Process  # NOQA
import src.debug  # NOQA

# For debugging with heapy.
if args.debug:
    src.debug.init_debug(comm.Get_rank())
    isend = src.debug.debug_send(comm.isend)
    recv = src.debug.debug_recv(comm.recv)
    abort = src.debug.debug_abort(comm.Abort)

initial_position = src.utils.game_module.initial_position()

process = Process(
    comm.Get_rank(),
    comm.Get_size(),
    comm,
    isend,
    recv,
    abort,
    stats_dir=args.statsdir
)

if process.rank == process.root:
    initial_gamestate = GameState(GameState.INITIAL_POS)

    tup = (initial_gamestate.to_tuple())
    # Uncomment for new_solver
    initial_job = Job(
        Job.LOOK_UP,
        process.rank,
        Job.INITIAL_JOB_ID,
        tup
    )
    # initial_job = Job(
    #     Job.LOOK_UP,
    #     initial_gamestate,
    #     process.rank,
    #     Job.INITIAL_JOB_ID,
    # )
    process.work.put(initial_job)

process.run()

comm.Barrier()
