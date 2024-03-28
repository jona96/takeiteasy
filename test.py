import unittest
from ai import AI
from board import Board, BoardPosition
Pos = BoardPosition.from_string
from tiles import Tile


class TestAI(unittest.TestCase):

    def test_1(self):
        """
        ****************************************************************
        *                               C                              *
        *                            _______                           *
        *                      B    /       \    D                     *
        *                   _______/         \_______                  *
        *             A    /       \         /       \    E            *
        *          _______/    1    \_______/         \_______         *
        *         /       \  2   3  /       \         /       \        *
        *        /    5    \_______/    9    \_______/         \       *
        *        \  2   8  /       \  2   3  /       \         /       *
        *      1  \_______/         \_______/         \_______/  1     *
        *         /       \         /       \         /       \        *
        *        /    5    \_______/         \_______/    1    \       *
        *        \  6   4  /       \         /       \  6   3  /       *
        *      2  \_______/    1    \_______/    5    \_______/  2     *
        *         /       \  7   8  /       \  6   8  /       \        *
        *        /         \_______/         \_______/         \       *
        *        \         /       \         /       \         /       *
        *      3  \_______/         \_______/    5    \_______/  3     *
        *                 \         /       \  7   8  /                *
        *               4  \_______/         \_______/  4              *
        *                          \         /                         *
        *                        5  \_______/  5                       *
        *                                                              *
        ****************************************************************
        
          _______  
         /       \  
        /    5    \  ==>  D2
        \  7   3  / 
         \_______/  
        """
        
        board = Board()
        board.place_tile(Tile(5,2,8), Pos('A1'))
        board.place_tile(Tile(5,6,4), Pos('A2'))
        board.place_tile(Tile(1,2,3), Pos('B1'))
        board.place_tile(Tile(1,7,8), Pos('B3'))
        board.place_tile(Tile(9,2,3), Pos('C2'))
        board.place_tile(Tile(5,6,8), Pos('D3'))
        board.place_tile(Tile(5,7,8), Pos('D4'))
        board.place_tile(Tile(1,6,3), Pos('E2'))
        
        suggested_position = AI.get_best_position(board, Tile(5,7,3))
        
        self.assertEqual(suggested_position, Pos('D2'))

    def test_2(self):
        """
        ****************************************************************
        *                               C                              *
        *                            _______                           *
        *                      B    /       \    D                     *
        *                   _______/    9    \_______                  *
        *             A    /       \  2   4  /       \    E            *
        *          _______/    1    \_______/         \_______         *
        *         /       \  2   3  /       \         /       \        *
        *        /    5    \_______/    9    \_______/         \       *
        *        \  2   8  /       \  2   3  /       \         /       *
        *      1  \_______/         \_______/         \_______/  1     *
        *         /       \         /       \         /       \        *
        *        /    5    \_______/         \_______/    1    \       *
        *        \  6   4  /       \         /       \  6   3  /       *
        *      2  \_______/    1    \_______/    5    \_______/  2     *
        *         /       \  7   8  /       \  6   8  /       \        *
        *        /         \_______/    9    \_______/         \       *
        *        \         /       \  6   8  /       \         /       *
        *      3  \_______/         \_______/    5    \_______/  3     *
        *                 \         /       \  7   8  /                *
        *               4  \_______/    9    \_______/  4              *
        *                          \  6   4  /                         *
        *                        5  \_______/  5                       *
        *                                                              *
        ****************************************************************
        
          _______  
         /       \  
        /    9    \  ==>  B4
        \  6   3  / 
         \_______/  
        """
        
        board = Board()
        board.place_tile(Tile(5,2,8), Pos('A1'))
        board.place_tile(Tile(5,6,4), Pos('A2'))
        board.place_tile(Tile(1,2,3), Pos('B1'))
        board.place_tile(Tile(1,7,8), Pos('B3'))
        board.place_tile(Tile(9,2,4), Pos('C1'))
        board.place_tile(Tile(9,2,3), Pos('C2'))
        board.place_tile(Tile(9,6,8), Pos('C4'))
        board.place_tile(Tile(9,6,4), Pos('C5'))
        board.place_tile(Tile(5,6,8), Pos('D3'))
        board.place_tile(Tile(5,7,8), Pos('D4'))
        board.place_tile(Tile(1,6,3), Pos('E2'))
        
        suggested_position = AI.get_best_position(board, Tile(9,6,4))
        
        self.assertEqual(suggested_position, Pos('B4'))

if __name__ == '__main__':
    unittest.main()
