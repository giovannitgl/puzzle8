from search_node import SearchNodes
from puzzle import PuzzleHelper

# Action constants
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
ACTIONS = [UP, DOWN, LEFT, RIGHT]


class Solver:
    def __init__(self):
        self.searches = 0

    def bfs(self, puzzle):

        # Initializes search nodes and inserts first state into Frontier
        if PuzzleHelper.check_puzzle_finished(puzzle):
            return puzzle, self.searches, []

        search_node = SearchNodes('bfs')
        search_node.push_frontier(puzzle, None, None)

        while search_node.frontier_has_next():
            self.searches += 1
            node_puzzle = search_node.pop_frontier()
            search_node.push_explored(node_puzzle)
            for action in ACTIONS:
                child_puzzle = PuzzleHelper.move_puzzle(node_puzzle[:], action)
                if child_puzzle is not None \
                   and not search_node.is_explored(child_puzzle) \
                   and not search_node.is_in_frontier(child_puzzle):
                    if PuzzleHelper.check_puzzle_finished(child_puzzle):
                        return child_puzzle, self.searches, search_node.get_solution(node_puzzle, action)
                    search_node.push_frontier(child_puzzle, node_puzzle, action)
        return None, self.searches, []
