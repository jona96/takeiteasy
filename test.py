import unittest
from ai import AI
from board import Board, BoardPosition
Pos = BoardPosition.from_string
from tiles import Tile


def board_A() -> Board:
    board = Board()
    board.place_tile(Tile(9,7,8), Pos('A1'))
    return board

class TestAI(unittest.TestCase):

    def test_with_two_spaces(self):
        suggested_position = AI.get_best_position(board_A(), Tile(1,2,3))
        self.assertEqual(suggested_position, Pos('E3'))

if __name__ == '__main__':
    unittest.main()
