import unittest
import imp
import os
import sys
import subprocess

out_path = 'game_tests/out.txt'

imp.load_source('src.utils', '../src/utils.py')

os.chdir("../")

class TicTacToeTest(unittest.TestCase):
    def test_four(self):
        """
        Starting position has corners filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/four_to_one.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'WIN in 3 moves\n')

    def test_six(self):
        """
        Starting position has corners filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/four_to_one.py --init_pos six '
                            '--custom game_tests/four_to_one_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'LOSS in 4 moves\n')

    def test_one(self):
        """
        Starting position has corners filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/four_to_one.py --init_pos one '
                            '--custom game_tests/four_to_one_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'WIN in 1 moves\n')

    def test_zero(self):
        """
        Starting position has corners filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/four_to_one.py --init_pos zero '
                            '--custom game_tests/four_to_one_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'LOSS in 0 moves\n')
