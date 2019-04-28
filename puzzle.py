from random import shuffle
from copy import deepcopy


class PuzzleHelper:
    """
    Helper class
    Manipulates an 8 puzzle array
    """

    @staticmethod
    def check_puzzle_finished(puzzle):
        """
            Checks if puzzle has been successfully finished.
            @return True if succesfully finished, False if not
        """
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        return puzzle == expected

    @staticmethod
    def move_puzzle(puzzle, direction):
        """
            Moves the zero block for the passed puzzle
            @param puzzle: array containing the puzzle to move
            @param direction: string containing direction to move (only up, down, left, right)
            @returns: Boolean, true if moved, false if not
        """
        puzzle_copy = puzzle
        zero_index = PuzzleHelper.get_zero_block_pos(puzzle)
        zero_row = zero_index // 3
        zero_col = zero_index % 3
        success = False
        if direction == 'UP':
            new_row = zero_row - 1
            if new_row >= 0:
                puzzle_copy[zero_row * 3 + zero_col] = puzzle[new_row * 3 + zero_col]
                puzzle_copy[new_row * 3 + zero_col] = 0
                success = True
        if direction == 'DOWN':
            new_row = zero_row + 1
            if new_row < 3:
                puzzle_copy[zero_row * 3 + zero_col] = puzzle[new_row * 3 + zero_col]
                puzzle_copy[new_row * 3 + zero_col] = 0
                success = True
        if direction == 'LEFT':
            new_col = zero_col - 1
            if new_col >= 0:
                puzzle_copy[zero_row * 3 + zero_col] = puzzle[zero_row * 3 + new_col]
                puzzle_copy[zero_row * 3 + new_col] = 0
                success = True
        if direction == 'RIGHT':
            new_col = zero_col + 1
            if new_col < 3:
                puzzle_copy[zero_row * 3 + zero_col] = puzzle[zero_row * 3 + new_col]
                puzzle_copy[zero_row * 3 + new_col] = 0
                success = True
        if success:
            return puzzle_copy
        return None

    @staticmethod
    def get_zero_block_pos(puzzle):
        """
            Returns the current position of
            the zero block.
            @returns: Tuple contaning zero block's position
        """
        if puzzle is None:
            return None

        return puzzle.index(0)

    @staticmethod
    def generate_random_puzzle():
        """
            Randomly generates a 8 puzzle
            @return:
        """
        random_puzzle = list(range(0, 9))
        shuffle(random_puzzle)
        return random_puzzle

    @staticmethod
    def print_puzzle(puzzle):
        for i in range(3):
            print (puzzle[i*3:i*3+3])
        print('Finished: ', PuzzleHelper.check_puzzle_finished(puzzle))
        print()

