from matplotlib import pyplot as plt
from puzzle import PuzzleHelper
from solver import Solver
from time import time

METHODS = ['bfs', 'ucs', 'sum', 'man', 'star_man', 'star_mis', 'hill']
# METHODS = ['bfs', 'dfs', 'sum', 'man']
# METHODS = ['bfs', 'dfs', 'ucs']
# METHODS = ['sum', 'man']
# METHODS = ['man']
# METHODS = ['ucs']
# METHODS = ['star_man', 'star_mis']
# METHODS = ['sum', 'man', 'star_man', 'star_mis']
# METHODS = ['bfs', 'star_man', 'sum']
# METHODS = ['hill']

LABELS = {
    'bfs': 'Breadth-First Search',
    'dfs': 'Iterative Deepening Search',
    'ucs': 'Uniform Cost Search',
    'sum': 'Greedy (Misplaced)',
    'man': 'Greedy (Manhattan)',
    'star_man': 'A* Search (Manhattan)',
    'star_mis': 'A* (Misplaced)',
    'hill': 'Hill Climbing'
}

if __name__ == '__main__':
    puzzles = [
        # [1, 2, 3, 4, 5, 6, 7, 8, 0], # 0
        # [1, 2, 3, 4, 5, 6, 7, 0, 8], # 1
        # [1, 2, 3, 4, 0, 5, 7, 8, 6], # 2
        # [1, 0, 3, 4, 2, 5, 7, 8, 6], # 3
        # [1, 5, 2, 4, 0, 3, 7, 8, 6], # 4
        # [1, 5, 2, 0, 4, 3, 7, 8, 6], # 5
        # [1, 5, 2, 4, 8, 3, 7, 6, 0], # 6
        # [1, 5, 2, 4, 8, 0, 7, 6, 3], # 7
        # [0, 5, 2, 1, 8, 3, 4, 7, 6], # 8
        # [1, 0, 2, 8, 5, 3, 4, 7, 6], # 9
        # [5, 8, 2, 1, 0, 3, 4, 7, 6], # 10
        # [5, 8, 2, 1, 7, 3, 4, 0, 6], # 11
        # [5, 8, 2, 1, 7, 3, 0, 4, 6], # 12
        # [5, 8, 2, 0, 7, 3, 1, 4, 6], # 13
        # [5, 8, 2, 7, 0, 3, 1, 4, 6], # 14
        # [8, 0, 2, 5, 7, 3, 1, 4, 6], # 15
        # [8, 7, 2, 5, 0, 3, 1, 4, 6], # 16
        # [5, 0, 8, 7, 3, 2, 1, 4, 6], # 17
        # [8, 7, 2, 5, 4, 3, 1, 6, 0], # 18
        # [8, 0, 7, 5, 3, 2, 1, 4, 6], # 19
        # [8, 7, 0, 5, 4, 2, 1, 6, 3], # 20
        # [8, 0, 7, 5, 4, 2, 1, 6, 3], # 21
        # [0, 8, 7, 5, 4, 2, 1, 6, 3], # 22
        # [8, 4, 7, 5, 6, 2, 1, 0, 3], # 23
        # [8, 4, 7, 5, 6, 2, 1, 3, 0], # 24
        # [8, 4, 7, 5, 6, 0, 1, 3, 2], # 25
        # [0, 4, 7, 8, 6, 2, 5, 1, 3], # 26
        # [8, 0, 7, 5, 4, 6, 1, 3, 2], # 27
        # [8, 4, 7, 6, 2, 3, 5, 1, 0], # 28
        # [8, 0, 6, 5, 7, 3, 1, 2, 4], # 29
        # [0, 8, 7, 5, 6, 4, 1, 2, 3], # 30
        [8, 6, 7, 2, 5, 4, 3, 0, 1], # 31
    ]
    index = 0
    solutions = dict()
    for method in METHODS:
        solutions[method] = {'time': [], 'expansion': [], 'movements': [], 'movements_str': []}
    for puzzle in puzzles:
        solver = Solver()

        # PuzzleHelper.print_puzzle(puzzle)
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
            elif method == 'hill':
                solution = solver.hill_climb(puzzle, 100)

            solutions[method]['time'].append(time() - start)
            solutions[method]['expansion'].append(solution[1])
            solutions[method]['movements'].append(len(solution[2]))
            solutions[method]['movements_str'].append(solution[2])

            # print('METHOD:', method)
            # if solution[0] is None:
            #     print('ERROR: Could not solve')
            #     print('Expansions:', solution[1])
            # else:
            #     PuzzleHelper.print_puzzle(solution[0])
            #     print('Expansions:', solution[1])
            #     print('Solution:', solution[2])
            #     print('Solution Size:', len(solution[2]))
            # print('Took', time() - start, 'seconds')
            # print('/' * 20)
            # print()

    # # Plots execution time
    # for method in METHODS:
    #     plt.plot(solutions[method]['time'], label=LABELS[method])
    #     plt.title('Execution time x Optimal solution size')
    #     plt.ylabel('Execution time in seconds (s)')
    # plt.legend(loc='best')
    # plt.savefig('graphs/time.png')
    # plt.clf()
    # # Plots size of solution
    # for method in METHODS:
    #     plt.plot(solutions[method]['movements'], label=LABELS[method])
    #     plt.title('Solution size x Optimal solution size')
    #     plt.ylabel('Quantity of movements')
    # plt.legend(loc='best')
    # plt.savefig('graphs/size.png')
    # plt.clf()
    # # Plots number of expansion
    # for method in METHODS:
    #     plt.plot(solutions[method]['expansion'], label=LABELS[method])
    #     plt.title('Expanded nodes x Optimal solution size')
    #     plt.ylabel('Quantity of expanded nodes')
    # plt.legend(loc='best')
    # plt.savefig('graphs/expansion.png')
    # plt.clf()

    # Creates latex table
    for method in METHODS:
        print(LABELS[method], '&', solutions[method]['time'][0], '&', solutions[method]['expansion'][0], '&', solutions[method]['movements_str'][0], '\\\\')

