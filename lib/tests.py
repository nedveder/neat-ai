
import unittest
from typing import List

def is_partial_solution(board: List[List[int]]) -> bool:
    """
    checks if the solution is the only solution or only a partial one
    :param board: a board with some solution, partial or full
    :return: True if partial solution, False if only solution
    """
    for row in board:
        for cell in row:
            if cell == -1:
                return True
    return False

class PartialSolutionTest(unittest.TestCase):
    def test_partial_solution(self):
        # Test with a board containing some incomplete rows and without -1s.
        board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertTrue(is_partial_solution(board))
        
        # Test with a board containing some incomplete rows and with -1s.
        board = [[1, 2, 3], [4, -1, 6], [7, 8, 9]]
        self.assertTrue(is_partial_solution(board))
        
        # Test with a board that's fully complete and without -1s.
        board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertFalse(is_partial_solution(board))
        
        # Test with a board that's fully complete and with -1s.
        board = [[1, 2, 3], [4, 5, -1], [7, 8, 9]]
        self.assertFalse(is_partial_solution(board))
        
        # Test with an empty board.
        board = [[]]
        self.assertFalse(is_partial_solution(board))
        
        # Test with a board containing only -1s.
        board = [[-1, -1], [-1, -1]]
        self.assertTrue(is_partial_solution(board))
        
        # Test with a board containing only one row and column.
        board = [[1], [-1]]
        self.assertTrue(is_partial_solution(board))
        
        # Test with a board containing one row and column and no -1s.
        board = [[1], [2]]
        self.assertFalse(is_partial_solution(board))
        
        # Test with a board that contains only -1s and has no rows or columns.
        board = [[]]
        self.assertTrue(is_partial_solution(board))
        
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
