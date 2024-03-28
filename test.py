import unittest
from ai import AI
from board import Board, BoardPosition
from tiles import Tile


class TestAI(unittest.TestCase):

    def test_with_two_spaces(self):
        # prepare board
        board = Board()
        board.place_tile(Tile(9,7,8), BoardPosition('A', 1))
        
        # run ai with (1,2,3)
        ai = AI()
        suggested_position = ai.get_best_position(board, Tile(1,2,3))
        self.assertEqual(suggested_position, BoardPosition('E', 3))

if __name__ == '__main__':
    unittest.main()
