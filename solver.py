from search_node import SearchNodes
from puzzle import PuzzleHelper

# Action constants
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
ACTIONS = [UP, DOWN, LEFT, RIGHT]


class Solver:
    def heuristic_cost(self, puzzle, heuristic):
        """
        Calculates the costs for 8 puzzle state, based on some heuristics
        :param puzzle:
        :param heuristic:
        :return:
        """
        cost = 0
        if heuristic == 'misplaced':
            for i in range(1, 10):
                if puzzle[i-1] != i % 9:
                    cost += 1
        elif heuristic == 'manhattan':
            for i in range(1, 10):
                value = puzzle[i-1]
                expected = i % 9
                if value != expected:
                    position = value - 1 if value != 0 else 9
                    exp_row, exp_col = (position // 3, position % 3)
                    cur_row, cur_col = ((i - 1) // 3, (i - 1) % 3)
                    cost += abs(cur_row - exp_row) + abs(cur_col - exp_col)
        return cost

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
            node_puzzle = search_node.pop_frontier()[0]
            search_node.push_explored(node_puzzle)
            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    # If finished, returns solution
                    if PuzzleHelper.check_puzzle_finished(child_puzzle):
                        return child_puzzle, searches, search_node.get_solution(node_puzzle, action)
                    # Else, add to frontier
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
            return self.heuristic_cost(current_puzzle, mode)

        searches = 0

        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, searches, []

        search_node = SearchNodes('greedy_sum')

        cost = expected_cost(puzzle, mode)
        search_node.push_frontier(puzzle, None, None, cost=cost, depth=0)
        while search_node.frontier_has_next():
            searches += 1
            node_puzzle, parent_depth = search_node.pop_frontier(return_depth=True)
            search_node.push_explored(node_puzzle)

            if PuzzleHelper.check_puzzle_finished(node_puzzle):
                return node_puzzle, searches, search_node.get_solution(node_puzzle, None)

            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)

                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    depth = 1 + parent_depth
                    cost = depth + expected_cost(child_puzzle, mode)
                    search_node.push_frontier(child_puzzle, node_puzzle, action, cost=cost, depth=depth)

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
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.no_information_solver(puzzle, 'dfs')

    def ids(self, puzzle):
        """
        Searches multiple depths of a DFS search, looking
        for solutions of 8 puzzle
        :param puzzle: Array containing the puzzle state
        :return:
        """
        cumulative_searches = 0
        for i in range(0, 64):
            solution, searches, movements = self.ids_recursive(puzzle, i)
            cumulative_searches += searches
            if solution is not None:
                return solution, cumulative_searches, movements
        return None, cumulative_searches, []

    def ids_recursive(self, puzzle, limit):
        """
        Recursive Function for searching using DFS with a limited depth.

        Used for IDS.
        :param puzzle: Array containing the puzzle state
        :param limit:
        :return:
        """
        searches = 0

        # Initializes search nodes and inserts first state into Frontier
        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, searches, []

        search_node = SearchNodes('dfs')
        search_node.push_frontier(puzzle, None, None, depth=0)

        while search_node.frontier_has_next():
            searches += 1
            node_puzzle, parent_depth = search_node.pop_frontier(return_depth=True)
            search_node.push_explored(node_puzzle)
            for action in ACTIONS:
                child_depth = parent_depth + 1
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    # If finished, returns solution
                    if PuzzleHelper.check_puzzle_finished(child_puzzle):
                        return child_puzzle, searches, search_node.get_solution(node_puzzle, action)
                    # Else, add to frontier
                    if child_depth <= limit:
                        search_node.push_frontier(child_puzzle, node_puzzle, action, depth=child_depth)
        return None, searches, []

    def ucs(self, puzzle):
        """
        Searches a solution for 8 puzzle, using Universal Cost Search
        :param puzzle: Array containing the puzzle state
        :return:
        """
        searches = 0

        # Initializes search nodes and inserts first state into Frontier
        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, searches, []

        search_node = SearchNodes('ucs')
        search_node.push_frontier(puzzle, None, None, cost=0)

        while search_node.frontier_has_next():
            searches += 1
            node_puzzle, parent_cost = search_node.pop_frontier(return_cost=True)
            search_node.push_explored(node_puzzle)

            if PuzzleHelper.check_puzzle_finished(node_puzzle):
                return node_puzzle, searches, search_node.get_solution(node_puzzle, None)

            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                cost = parent_cost + 1

                if child_puzzle is not None \
                        and not search_node.is_explored(child_puzzle) \
                        and not search_node.is_in_frontier(child_puzzle):
                    # If finished, returns solution
                    # Else, add to frontier
                    search_node.push_frontier(child_puzzle, node_puzzle, action, cost=cost)
                elif child_puzzle is not None and search_node.is_in_frontier(child_puzzle):
                    search_node.swap_frontier_if_better(child_puzzle, node_puzzle, action, cost, cost)
        return None, searches, []

    def A_star(self, puzzle, mode):
        """
        Searches a solution for 8 puzzle, using A Star algorithm.
        :param puzzle: Array containing the puzzle state
        :return:
        """
        searches = 0
        search_node = SearchNodes('astar')

        current_cost = self.heuristic_cost(puzzle, mode)
        search_node.push_frontier(puzzle, None, None, current_cost, 0)

        while search_node.frontier_has_next():
            searches += 1
            node_puzzle, depth = search_node.pop_frontier(return_depth=True)

            if PuzzleHelper.check_puzzle_finished(node_puzzle):
                return node_puzzle, searches, search_node.get_solution(node_puzzle, None)

            search_node.push_explored(node_puzzle)

            for action in ACTIONS:
                child_depth = depth + 1
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)

                if child_puzzle is not None:
                    if not search_node.is_explored(child_puzzle):
                        cost = child_depth + self.heuristic_cost(child_puzzle, mode)
                        if not search_node.is_in_frontier(child_puzzle):
                            search_node.push_frontier(child_puzzle, node_puzzle, action, cost, child_depth)
                        else:
                            search_node.swap_frontier_if_better(child_puzzle, node_puzzle, action, cost, child_depth)
        return None, searches, []

    def A_star_manhattan(self, puzzle):
        """
        Calls A* search with Manhattan Distance Heuristic
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.A_star(puzzle, 'manhattan')

    def A_star_misplaced(self, puzzle):
        """
        Calls A* search with Misplaced Tiles Heuristic
        :param puzzle: Array containing the puzzle state
        :return:
        """
        return self.A_star(puzzle, 'misplaced')

    def hill_climb(self, puzzle, k):
        """
        Searches for solutions using hill climb, in order to find
        local best solutions.
        :param puzzle: Array containing the puzzle state
        :return:
        """
        searches = 0
        search_node = SearchNodes('hill')
        current_cost = self.heuristic_cost(puzzle, 'manhattan')
        search_node.push_frontier(puzzle, None, None, current_cost)
        side_move = -1
        movements = []
        while True:
            searches += 1
            neighbor, neighbor_cost, neigh_action = search_node.pop_frontier(return_cost=True)
            if neigh_action is not None:
                movements.append(neigh_action)

            if PuzzleHelper.check_puzzle_finished(neighbor):
                return neighbor, searches, movements

            if neighbor_cost >= current_cost:
                side_move += 1
                if side_move == k:
                    break

            current_cost = neighbor_cost

            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(neighbor[:], action)
                if child_puzzle is not None:
                    child_cost = self.heuristic_cost(child_puzzle, 'misplaced')
                    search_node.push_frontier(child_puzzle, neighbor, action, child_cost)
        return None, searches, []
