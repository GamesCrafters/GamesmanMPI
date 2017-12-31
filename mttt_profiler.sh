mpiexec -n $1 python3 -m cProfile -s 'time' solver_launcher.py test_games/mttt.py --cp > $2
