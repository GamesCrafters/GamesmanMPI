import unittest
import imp
import os
import sys
import subprocess

out_path = 'game_tests/out.txt'

imp.load_source('src.utils', '../src/utils.py')

os.chdir("../")

class TicTacToeTest(unittest.TestCase):
    def test_blank(self):
        """
        Starting position is just a blank board.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/mttt.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'TIE in 9 moves\n')

    def test_tie_in_one(self):
        """
        Starting position forces a tie for the next player.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/mttt.py --init_pos tie_in_one '
                            '--custom game_tests/mttt_test_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'TIE in 1 moves\n')

    def test_win_in_one(self):
        """
        Starting position allows next player to win.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/mttt.py --init_pos win_in_one '
                            '--custom game_tests/mttt_test_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'WIN in 1 moves\n')

    def test_side_columns(self):
        """
        The sides of columns are filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/mttt.py --init_pos side_columns '
                            '--custom game_tests/mttt_test_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'TIE in 3 moves\n')

    def test_one_row(self):
        """
        The sides of columns are filled.
        """
        subprocess.call('make clean'.split())
        with open(out_path, 'w') as f:
            subprocess.call('mpiexec --oversubscribe -n 2 python solver_launcher.py '
                            'test_games/mttt.py --init_pos one_row '
                            '--custom game_tests/mttt_test_init_pos.py'.split(), stdout = f)
        with open(out_path, 'r') as f:
            self.assertEqual(f.read(), 'TIE in 3 moves\n')
