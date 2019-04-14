from search_node import SearchNodes
from puzzle import PuzzleHelper

# Action constants
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
ACTIONS = [UP, DOWN, LEFT, RIGHT]


class Solver:
    def no_information_solver(self, puzzle, mode):
        """
        Solves the 8-puzzle, can be used for bfs or dfs
        :param puzzle: Array containing 8-puzzle
        :param mode: String containing mode (bfs, dfs)
        :return:
        """
        searches = 0

        # Initializes search nodes and inserts first state into Frontier
        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, searches, []

        search_node = SearchNodes(mode)
        search_node.push_frontier(puzzle, None, None)

        while search_node.frontier_has_next():
            searches += 1
            node_puzzle = search_node.pop_frontier()
            search_node.push_explored(node_puzzle)
            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    if PuzzleHelper.check_puzzle_finished(child_puzzle):
                        return child_puzzle, searches, search_node.get_solution(node_puzzle, action)
                    search_node.push_frontier(child_puzzle, node_puzzle, action)
        return None, searches, []

    def greedy_solver(self, puzzle, mode):
        """
        Solves the 8-puzzle using Greedy Heuristics (passed via mode)

        :param puzzle: Array containing the 8-puzzle
        :param mode: string containing the heuristic mode
        :return:
        """
        def expected_cost(current_puzzle, mode):
            cost = 0
            if mode == 'misplaced':
                for i in range(1, 10):
                    if current_puzzle[i-1] != i % 9:
                        cost += 1
            elif mode == 'manhattan':
                for i in range(1, 10):
                    value = current_puzzle[i-1]
                    expected = i % 9
                    if value != expected:
                        position = value - 1 if value != 0 else 9
                        exp_row, exp_col = (position // 3, position % 3)
                        cur_row, cur_col = ((i - 1) // 3, (i - 1) % 3)
                        cost += abs(cur_row - exp_row) + abs(cur_col - exp_col)
            return cost

        searches = 0

        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, searches, []

        search_node = SearchNodes('greedy_sum')

        cost = expected_cost(puzzle, mode)
        search_node.push_frontier(puzzle, None, None, cost=cost)
        while search_node.frontier_has_next():
            searches += 1
            node_puzzle = search_node.pop_frontier()
            search_node.push_explored(node_puzzle)
            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    if PuzzleHelper.check_puzzle_finished(child_puzzle):
                        return child_puzzle, searches, search_node.get_solution(node_puzzle, action)
                    cost = expected_cost(child_puzzle, mode)
                    search_node.push_frontier(child_puzzle, node_puzzle, action, cost=cost)

        return None, searches, []

    def greedy_sum_of_misplaced(self, puzzle):
        """
        Searches a solution for 8 puzzle using sum of misplaced
        tiles as a cost (aka 1 misplaced tile, + 1 in sum)
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.greedy_solver(puzzle, 'misplaced')

    def greedy_sum_manhattan(self, puzzle):
        """
        Searches a solution for 8 puzzle using manhattam sum
        (sum of distance for each block, with distance being
        how many movements are needed to reach desired state)
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.greedy_solver(puzzle, 'manhattan')

    def bfs(self, puzzle):
        """
        Searches a solution for 8 puzzle, using Breadth-First Search
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.no_information_solver(puzzle, 'bfs')

    def dfs(self, puzzle):
        """
        Searches a solution for 8 puzzle, using Depth-First Search
        :param puzzle:  Array containing the puzzle state
        :return:
        """
        return self.no_information_solver(puzzle, 'dfs')

