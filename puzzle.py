from random import shuffle

class Puzzle:
    def  __init__(self, puzzle):
        Puzzle.validate_puzzle(puzzle)
        self.puzzle = puzzle
        self.zero_block_pos = None
        self.zero_block_pos = self.get_zero_block_pos()
        self.finished = self.check_puzzle_finished()

    def check_puzzle_finished(self):
        """
            Checks if puzzle has been successfully finished.
            @return True if succesfully finished, False if not
        """
        flattened_checker = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        flattened_puzzle = [y for x in self.puzzle for y in x]
        for i, value in enumerate(flattened_checker):
            if flattened_puzzle[i] != value:
                return False
        return True

    def move_puzzle(self, value):
        """
            Swaps the passed value with the
            0 value block.
            @param value: The value block to swap with the 0 block
            @returns: Boolean, true if moved, false if not
        """
        zero_row, zero_col = self.get_zero_block_pos()
        neighborsIndex = Puzzle.generate_neighbors_index(zero_row, zero_col)
        for i,j in neighborsIndex:
            if self.puzzle[i][j] == value:
                self.puzzle[zero_row][zero_col] = self.puzzle[i][j]
                self.puzzle[i][j] = 0
                self.zero_block_pos = (i, j)
                self.finished = self.check_puzzle_finished()
                return True
        return False

    def validate_puzzle(puzzle):
        """
            Validates if a puzzle is valid.
            If not valid, raises an Exception
            @param puzzle: puzzle object to validate
        """
        # Flattens the puzzle matrix
        flatten =  [y for x in puzzle for y in x]
        # Validate if quantity of blocks is correct
        if len(flatten) != 9:
            raise Exception('Invalid Puzzle')
        flatten.sort()
        # Validate if values are correct
        for i in range(0, 9):
            if flatten[i] != i:
                Exception('Invalid Puzzle')
        # Validate if format is correct
        for i in range(0, 3):
            if len(puzzle[i]) != 3:
                Exception('Invalid Puzzle')

    def get_zero_block_pos(self):
        """
            Returns the current position of
            the zero block.
            @returns: Tuple contaning zero block's position
        """
        if self.puzzle is None:
            return None
        if self.zero_block_pos is not None:
            return self.zero_block_pos

        for i in range(0, 3):
            for j in range(0, 3):
                if self.puzzle[i][j] == 0:
                    return (i, j)

    def generate_random_puzzle():
        """
            Randomly generates a 8 puzzle
            @return:
        """
        numbers = list(range(0, 10))
        shuffle(numbers)
        puzzle = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range (0, 3):
            for j in range (0, 3):
                puzzle[i][j] = numbers.pop()
        return puzzle

    def generate_neighbors_index(row, col):
        """
            Generates the indexes of a block's
            neighbors.
            @param row: block's row
            @param col: block's col
            @returns: list of block's neighbors indexes
        """
        neigh_index = []
        for i in range(-1, 2):
            for j in range(-1,2):
                row_sum = row + i
                col_sum = col + j
                if row_sum > 2 or row_sum < 0:
                    continue
                if col_sum > 2 or col_sum < 0:
                    continue
                if i == 0 and j == 0:
                    continue
                neigh_index.append((row_sum, col_sum))
        return neigh_index

if __name__ == '__main__':
    # puzzle = Puzzle(Puzzle.generate_random_puzzle())
    # puzzle = Puzzle([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    puzzle = Puzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
    puzzle.move_puzzle(1)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
    puzzle.move_puzzle(2)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
    puzzle.move_puzzle(1)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
    puzzle.move_puzzle(5)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
    puzzle.move_puzzle(8)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print(puzzle.finished)
    print()
