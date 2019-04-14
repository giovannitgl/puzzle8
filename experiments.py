from puzzle import PuzzleHelper
from solver import Solver

METHODS = ['bfs', 'dfs', 'sum', 'man']
# METHODS = ['bfs', 'dfs', 'sum']
# METHODS = ['sum', 'man']

if __name__ == '__main__':
    # puzzle = PuzzleHelper.generate_random_puzzle()
    puzzle = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    solver = Solver()

    PuzzleHelper.print_puzzle(puzzle)

    for method in METHODS:
        solution = None
        if method == 'bfs':
            solution = solver.bfs(puzzle)
        elif method == 'dfs':
            solution = solver.dfs(puzzle)
        elif method == 'sum':
            solution = solver.greedy_sum_of_misplaced(puzzle)
        elif method == 'man':
            solution = solver.greedy_sum_manhattan(puzzle)

        print('METHOD:', method)
        if solution[0] is None:
            print('ERROR: Could not solve')
            print('Expansions:', solution[1])
        else:
            PuzzleHelper.print_puzzle(solution[0])
            print('Expansions:', solution[1])
            print('Solution:', solution[2])
            print('Solution Size:', len(solution[2]))
            print('/' * 20)
            print()
