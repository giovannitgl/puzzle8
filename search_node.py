from collections import deque

# Constants of search methods
FIFO = 'FIFO'


class SearchNodes:
    def __init__(self, mode):
        self._frontier = deque()
        self._frontier_set = set()
        self._explored = set()
        self._movements = {}
        self._mode = None
        if mode == 'bfs':
            self.mode = FIFO

    def push_frontier(self, state, parent, action):
        parent_as_str = ''.join(str(x) for x in parent) if parent is not None else ''
        node_as_str = ''.join(str(x) for x in state)
        if parent is None:
            self._movements[node_as_str] = ''
        else:
            history = ''.join([parent_as_str, '|', action[0]])
            self._movements[node_as_str] = history
        self._frontier_set.add(node_as_str)
        if self.mode == FIFO:
            self._frontier.append(node_as_str)

    def pop_frontier(self):
        content = None
        if self.mode == FIFO:
            content = self._frontier.pop()

        self._frontier_set.remove(content)
        return [int(x) for x in list(content)]

    def frontier_has_next(self):
        return len(self._frontier) > 0

    def push_explored(self, state):
        state_as_str = ''.join(str(x) for x in state)
        if state_as_str not in self._explored:
            self._explored.add(state_as_str)

    def is_explored(self, state):
        state_as_str = ''.join(str(x) for x in state)
        return state_as_str in self._explored

    def is_in_frontier(self, state):
        state_as_str = ''.join(str(x) for x in state)
        return state_as_str in self._frontier_set

    def get_solution(self, puzzle, action):
        puzzle_as_str = ''.join(str(x) for x in puzzle)
        parent = self._movements[puzzle_as_str]
        solution = action[0]
        while parent is not None:
            parent_str, movement = parent.split('|')
            solution = ''.join([solution, movement])
            parent = self._movements[parent_str]
            if parent == '':
                parent = None
        return solution[::-1]
