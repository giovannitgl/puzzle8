from puzzle import PuzzleHelper
from solver import Solver
import itertools

if __name__ == '__main__':
    # puzzle = PuzzleHelper.generate_random_puzzle()
    puzzle = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    solver = Solver()
    PuzzleHelper.print_puzzle(puzzle)
    x = solver.bfs(puzzle)
    if x[0] is None:
        print('ERROR: Could not solve')
        print('Expansions:', x[1])
    else:
        PuzzleHelper.print_puzzle(x[0])
        print('Expansions:', x[1])
        print('Solution:', x[2])
