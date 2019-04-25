from collections import deque
from heapq import heappush, heappop, heapify

# Constants of search methods
FIFO = 'FIFO'
LIFO = 'LIFO'
UCS = 'UCS'
SUM = 'SUM'
STAR = 'STAR'


class SearchNodes:
    """
    Class responsible for handling search nodes for 8 puzzle.

    This class operates in many modes:
     - BFS: FIFO Frontier
     - DFS: LIFO Frontier
     - UCS: Heap Frontier
     - Greedy: Heap Frontier
     - AStar: Heap Frontier
    """
    def __init__(self, mode):
        self._frontier = deque()
        self._frontier_set = set()
        self._explored = set()
        self._movements = {}
        self._mode = None
        if mode == 'bfs':
            self.mode = FIFO
        elif mode == 'dfs':
            self.mode = LIFO
        elif mode == 'ucs':
            self.mode = UCS
            self._frontier = []
        elif mode == 'greedy_sum':
            self.mode = SUM
            self._frontier = []
        elif mode == 'astar':
            self.mode = STAR
            self._frontier = []

    def push_frontier(self, state, parent, action, cost=None, depth=None):
        parent_as_str = SearchNodes.puzzle_to_key(parent) if parent is not None else ''
        node_as_str = SearchNodes.puzzle_to_key(state)

        # Creates movement history for generating solution later
        if parent is None:
            self._movements[node_as_str] = ''
        else:
            cost = 0 if cost is None else cost
            depth = depth if depth is not None else 0
            history = ''.join([parent_as_str, '|', action[0], '|', str(cost), '|', str(depth)])
            self._movements[node_as_str] = history

        # Adds state to frontier set for easy search
        self._frontier_set.add(node_as_str)

        # Insert into frontier the puzzle
        if self.mode == FIFO:
            self._frontier.append(node_as_str)
        elif self.mode == LIFO:
            self._frontier.append(node_as_str)
        elif self.mode == UCS:
            heappush(self._frontier, (cost, node_as_str))
        elif self.mode == SUM:
            heappush(self._frontier, (cost, node_as_str))
        elif self.mode == STAR:
            heappush(self._frontier, (cost, node_as_str))

    def pop_frontier(self, return_cost=False, return_depth=False):
        content = None
        if self.mode == FIFO:
            content = self._frontier.popleft()
        elif self.mode == LIFO:
            content = self._frontier.pop()
        elif self.mode == UCS:
            cost, content = heappop(self._frontier)
        elif self.mode == SUM:
            cost, content = heappop(self._frontier)
        elif self.mode == STAR:
            cost, content = heappop(self._frontier)

        self._frontier_set.remove(content)

        result = []

        content_as_list = [int(x) for x in list(content)]
        result.append(content_as_list)

        if return_cost:
            result.append(cost)

        if return_depth:
            depth = self.get_depth(content)
            result.append(depth)

        return tuple(result)

    def frontier_has_next(self):
        return len(self._frontier) > 0

    def push_explored(self, state):
        state_as_str = SearchNodes.puzzle_to_key(state)
        if state_as_str not in self._explored:
            self._explored.add(state_as_str)

    def is_explored(self, state):
        state_as_str = SearchNodes.puzzle_to_key(state)
        return state_as_str in self._explored

    def is_in_frontier(self, state):
        state_as_str = ''.join(str(x) for x in state)
        return state_as_str in self._frontier_set

    def swap_frontier_if_better(self, puzzle, parent, action, cost, depth):
        node_as_str = SearchNodes.puzzle_to_key(puzzle)
        parent_as_str = SearchNodes.puzzle_to_key(parent)
        node_hist, action_hist, cost_hist, depth = self._movements[node_as_str].split('|')
        if int(cost_hist) > cost:
            print('HERE')
            self._movements[node_as_str] = ''.join([parent_as_str, '|', action, '|', str(cost), '|', str(depth)])
            index = self._frontier.index((cost_hist, node_as_str))
            self._frontier[index] = (cost, node_as_str)
            heapify(self._frontier)

    def get_solution(self, puzzle, action):
        puzzle_as_str = SearchNodes.puzzle_to_key(puzzle)
        parent = self._movements[puzzle_as_str]
        solution = action[0] if action is not None else ''
        while parent is not None:
            parent_str, movement, cost, depth = parent.split('|')
            solution = ''.join([solution, movement])
            parent = self._movements[parent_str]
            if parent == '':
                parent = None
        return solution[::-1]

    def get_depth(self, puzzle):
        history = self._movements[puzzle]
        if history == '':
            return 0

        _, _, _, depth = history.split('|')
        return int(depth)

    @staticmethod
    def puzzle_to_key(puzzle):
        return ''.join(str(x) for x in puzzle)
