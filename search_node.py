from collections import deque
from heapq import heappush, heappop

# Constants of search methods
FIFO = 'FIFO'
LIFO = 'LIFO'
SUM = 'SUM'


class SearchNodes:
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
        elif mode == 'greedy_sum':
            self.mode = SUM
            self._frontier = []

    def push_frontier(self, state, parent, action, cost=None):
        parent_as_str = SearchNodes.puzzle_to_key(parent) if parent is not None else ''
        node_as_str = SearchNodes.puzzle_to_key(state)

        # Creates movement history for generating solution later
        if parent is None:
            self._movements[node_as_str] = ''
        else:
            history = ''.join([parent_as_str, '|', action[0]])
            self._movements[node_as_str] = history

        # Adds state to frontier set for easy search
        self._frontier_set.add(node_as_str)

        # Insert into frontier the puzzle
        if self.mode == FIFO:
            self._frontier.append(node_as_str)
        elif self.mode == LIFO:
            self._frontier.append(node_as_str)
        elif self.mode == SUM:
            heappush(self._frontier, (cost, node_as_str))

    def pop_frontier(self):
        content = None
        if self.mode == FIFO:
            content = self._frontier.popleft()
        elif self.mode == LIFO:
            content = self._frontier.pop()
        elif self.mode == SUM:
            content = heappop(self._frontier)[1]

        self._frontier_set.remove(content)
        return [int(x) for x in list(content)]

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

    def get_solution(self, puzzle, action):
        puzzle_as_str = SearchNodes.puzzle_to_key(puzzle)
        parent = self._movements[puzzle_as_str]
        solution = action[0]
        while parent is not None:
            parent_str, movement = parent.split('|')
            solution = ''.join([solution, movement])
            parent = self._movements[parent_str]
            if parent == '':
                parent = None
        return solution[::-1]

    @staticmethod
    def puzzle_to_key(puzzle):
        return ''.join(str(x) for x in puzzle)
