from puzzle import PuzzleHelper
from solver import Solver
from time import time

METHODS = ['bfs', 'dfs', 'ucs', 'sum', 'man', 'star_man', 'star_mis']
# METHODS = ['bfs', 'dfs', 'sum', 'man']
# METHODS = ['bfs', 'dfs', 'ucs']
# METHODS = ['sum', 'man']
# METHODS = ['man']
# METHODS = ['ucs']
# METHODS = ['star_man', 'star_mis']
# METHODS = ['sum', 'man', 'star_man', 'star_mis']
# METHODS = ['bfs', 'dfs']

if __name__ == '__main__':
    # puzzle = PuzzleHelper.generate_random_puzzle()
    puzzle = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    # puzzle = [8, 0, 6, 5, 7, 3, 1, 2, 4]
    solver = Solver()

    PuzzleHelper.print_puzzle(puzzle)
    for method in METHODS:
        solution = None
        start = time()
        if method == 'bfs':
            solution = solver.bfs(puzzle)
        elif method == 'dfs':
            solution = solver.ids(puzzle)
        elif method == 'ucs':
            solution = solver.ucs(puzzle)
        elif method == 'sum':
            solution = solver.greedy_sum_of_misplaced(puzzle)
        elif method == 'man':
            solution = solver.greedy_sum_manhattan(puzzle)
        elif method == 'star_man':
            solution = solver.A_star_manhattan(puzzle)
        elif method == 'star_mis':
            solution = solver.A_star_misplaced(puzzle)

        print('METHOD:', method)
        if solution[0] is None:
            print('ERROR: Could not solve')
            print('Expansions:', solution[1])
        else:
            PuzzleHelper.print_puzzle(solution[0])
            print('Expansions:', solution[1])
            print('Solution:', solution[2])
            print('Solution Size:', len(solution[2]))
        print('Took', time() - start, 'seconds')
        print('/' * 20)
        print()
