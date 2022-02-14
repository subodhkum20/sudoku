SUDOKU-PAIR SOLVER
Command-line tools for solving sudoku-pair puzzles of variable size with unique solutions.

Implemented in python using SAT solvers.

To install PySAT use following command:

pip install python-sat

then change the location of input file in file sudoku-pair.py at 49th line to select a particular input file from the test folder.

then run

python3 sudoku-pair_solver.py

then input the dimension of the sudoku (k) in the terminal to get a k^2-by-k^2 solved sudoku pair in the terminal.