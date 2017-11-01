#4 to 0 unit tests
echo Testing four to zero
python solve_local.py test_games/four_to_one.py
mpiexec -n 5 python solver_launcher.py test_games/four_to_one.py
