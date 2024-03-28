import unittest
from ai import AI
from board import Board, BoardPosition
Pos = BoardPosition.from_string
from tiles import Tile


class TestAI(unittest.TestCase):

    def test_placement_1(self):
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

    def test_placement_2(self):
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

    def test_placement_3(self):
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
        *      1  \_______/    9    \_______/    9    \_______/  1     *
        *         /       \  2   8  /       \  7   3  /       \        *
        *        /    5    \_______/         \_______/    1    \       *
        *        \  6   4  /       \         /       \  6   3  /       *
        *      2  \_______/    1    \_______/    5    \_______/  2     *
        *         /       \  7   8  /       \  6   8  /       \        *
        *        /         \_______/    9    \_______/    1    \       *
        *        \         /       \  6   8  /       \  6   8  /       *
        *      3  \_______/         \_______/    5    \_______/  3     *
        *                 \         /       \  7   8  /                *
        *               4  \_______/    9    \_______/  4              *
        *                          \  6   4  /                         *
        *                        5  \_______/  5                       *
        *                                                              *
        ****************************************************************
        
          _______  
         /       \  
        /    1    \  ==>  D1
        \  2   4  / 
         \_______/  
        """
        
        board = Board()
        board.place_tile(Tile(5,2,8), Pos('A1'))
        board.place_tile(Tile(5,6,4), Pos('A2'))

        board.place_tile(Tile(1,2,3), Pos('B1'))
        board.place_tile(Tile(9,2,8), Pos('B2'))
        board.place_tile(Tile(1,7,8), Pos('B3'))
        
        board.place_tile(Tile(9,2,4), Pos('C1'))
        board.place_tile(Tile(9,2,3), Pos('C2'))
        board.place_tile(Tile(9,6,8), Pos('C4'))
        board.place_tile(Tile(9,6,4), Pos('C5'))
        
        board.place_tile(Tile(9,7,3), Pos('D2'))
        board.place_tile(Tile(5,6,8), Pos('D3'))
        board.place_tile(Tile(5,7,8), Pos('D4'))
        
        board.place_tile(Tile(1,6,3), Pos('E2'))
        board.place_tile(Tile(1,6,8), Pos('E3'))
        
        suggested_position = AI.get_best_position(board, Tile(1,2,4))
        
        self.assertEqual(suggested_position, Pos('D1'))

    def test_placement_4(self):
        """
        ****************************************************************
        *                               C                              *
        *                            _______                           *
        *                      B    /       \    D                     *
        *                   _______/    9    \_______                  *
        *             A    /       \  2   4  /       \    E            *
        *          _______/    1    \_______/    1    \_______         *
        *         /       \  2   3  /       \  2   4  /       \        *
        *        /    5    \_______/    9    \_______/         \       *
        *        \  2   8  /       \  2   3  /       \         /       *
        *      1  \_______/    9    \_______/    9    \_______/  1     *
        *         /       \  2   8  /       \  7   3  /       \        *
        *        /    5    \_______/         \_______/    1    \       *
        *        \  6   4  /       \         /       \  6   3  /       *
        *      2  \_______/    1    \_______/    5    \_______/  2     *
        *         /       \  7   8  /       \  6   8  /       \        *
        *        /         \_______/    9    \_______/    1    \       *
        *        \         /       \  6   8  /       \  6   8  /       *
        *      3  \_______/         \_______/    5    \_______/  3     *
        *                 \         /       \  7   8  /                *
        *               4  \_______/    9    \_______/  4              *
        *                          \  6   4  /                         *
        *                        5  \_______/  5                       *
        *                                                              *
        ****************************************************************
        
          _______  
         /       \  
        /    1    \  ==>  E1
        \  7   4  / 
         \_______/  
        """
        
        board = Board()
        board.place_tile(Tile(5,2,8), Pos('A1'))
        board.place_tile(Tile(5,6,4), Pos('A2'))

        board.place_tile(Tile(1,2,3), Pos('B1'))
        board.place_tile(Tile(9,2,8), Pos('B2'))
        board.place_tile(Tile(1,7,8), Pos('B3'))
        
        board.place_tile(Tile(9,2,4), Pos('C1'))
        board.place_tile(Tile(9,2,3), Pos('C2'))
        board.place_tile(Tile(9,6,8), Pos('C4'))
        board.place_tile(Tile(9,6,4), Pos('C5'))
        
        board.place_tile(Tile(1,2,4), Pos('D1'))
        board.place_tile(Tile(9,7,3), Pos('D2'))
        board.place_tile(Tile(5,6,8), Pos('D3'))
        board.place_tile(Tile(5,7,8), Pos('D4'))
        
        board.place_tile(Tile(1,6,3), Pos('E2'))
        board.place_tile(Tile(1,6,8), Pos('E3'))
        
        suggested_position = AI.get_best_position(board, Tile(1,7,4))
        
        self.assertEqual(suggested_position, Pos('E1'))

    def test_placement_5(self):
        """
        ****************************************************************
        *                               C                              *
        *                            _______                           *
        *                      B    /       \    D                     *
        *                   _______/    9    \_______                  *
        *             A    /       \  2   4  /       \    E            *
        *          _______/    1    \_______/    1    \_______         *
        *         /       \  2   3  /       \  2   4  /       \        *
        *        /    5    \_______/    9    \_______/    1    \       *
        *        \  2   8  /       \  2   3  /       \  7   4  /       *
        *      1  \_______/    9    \_______/    9    \_______/  1     *
        *         /       \  2   8  /       \  7   3  /       \        *
        *        /    5    \_______/         \_______/    1    \       *
        *        \  6   4  /       \         /       \  6   3  /       *
        *      2  \_______/    1    \_______/    5    \_______/  2     *
        *         /       \  7   8  /       \  6   8  /       \        *
        *        /    5    \_______/    9    \_______/    1    \       *
        *        \  6   3  /       \  6   8  /       \  6   8  /       *
        *      3  \_______/         \_______/    5    \_______/  3     *
        *                 \         /       \  7   8  /                *
        *               4  \_______/    9    \_______/  4              *
        *                          \  6   4  /                         *
        *                        5  \_______/  5                       *
        *                                                              *
        ****************************************************************
        
          _______  
         /       \  
        /    5    \  ==>  B4
        \  7   4  / 
         \_______/  
        """
        
        board = Board()
        board.place_tile(Tile(5,2,8), Pos('A1'))
        board.place_tile(Tile(5,6,4), Pos('A2'))
        board.place_tile(Tile(5,6,3), Pos('A3'))

        board.place_tile(Tile(1,2,3), Pos('B1'))
        board.place_tile(Tile(9,2,8), Pos('B2'))
        board.place_tile(Tile(1,7,8), Pos('B3'))
        
        board.place_tile(Tile(9,2,4), Pos('C1'))
        board.place_tile(Tile(9,2,3), Pos('C2'))
        board.place_tile(Tile(9,6,8), Pos('C4'))
        board.place_tile(Tile(9,6,4), Pos('C5'))
        
        board.place_tile(Tile(1,2,4), Pos('D1'))
        board.place_tile(Tile(9,7,3), Pos('D2'))
        board.place_tile(Tile(5,6,8), Pos('D3'))
        board.place_tile(Tile(5,7,8), Pos('D4'))
        
        board.place_tile(Tile(1,7,4), Pos('E1'))
        board.place_tile(Tile(1,6,3), Pos('E2'))
        board.place_tile(Tile(1,6,8), Pos('E3'))
        
        suggested_position = AI.get_best_position(board, Tile(5,7,4))
        
        self.assertEqual(suggested_position, Pos('B4'))

if __name__ == '__main__':
    unittest.main()
