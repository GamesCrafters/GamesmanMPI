mpiexec -tag-output -np $1 python3 -m cProfile solver_launcher.py test_games/mttt.py >> $2
echo "Testing Tic Tac Toe with $1 processes" >> $3
python3 cpy_parser.py $2 >> $3
