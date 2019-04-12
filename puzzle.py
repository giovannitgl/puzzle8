from random import shuffle

class Puzzle:
    def  __init__(self, puzzle):
        self.puzzle = puzzle
        self.zero_block_pos = None
        self.zero_block_pos = self.get_zero_block_pos()

    def move_puzzle(self, value):
        """
            Swaps the passed value with the
            0 value block.
            @param value: The value block to swap with the 0 block
            @returns: Boolean, true if moved, false if not
        """
        zero_row, zero_col = self.get_zero_block_pos()
        neighborsIndex = Puzzle.generateNeighborsIndex(zero_row, zero_col)
        for i,j in neighborsIndex:
            if self.puzzle[i][j] == value:
                self.puzzle[zero_row][zero_col] = self.puzzle[i][j]
                self.puzzle[i][j] = 0
                self.zero_block_pos = (i, j)
                return True
        return False

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

    def generateRandomPuzzle():
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

    def generateNeighborsIndex(row, col):
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
    # puzzle = Puzzle(Puzzle.generateRandomPuzzle())
    puzzle = Puzzle([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    for i in range(0,3):
        print(puzzle.puzzle[i])
    print()
    puzzle.move_puzzle(1)
    for i in range(0,3):
        print(puzzle.puzzle[i])
    puzzle.move_puzzle(2)
    print()
    for i in range(0,3):
        print(puzzle.puzzle[i])
