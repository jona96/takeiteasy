from copy import copy
from statistics import mean
import unittest
from ai import AI
from board import Board, BoardPosition
Pos = BoardPosition.from_string
from tiles import Tile, Tiles
from game import Game

def full_board(n:int = 1):
    boards = {}

    """ board 1
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/    1    \_______                  *
    *             A    /       \  6   3  /       \    E            *
    *          _______/    5    \_______/    1    \_______         *
    *         /       \  6   8  /       \  2   3  /       \        *
    *        /    9    \_______/    1    \_______/    5    \       *
    *        \  7   3  /       \  2   8  /       \  2   3  /       *
    *      1  \_______/    5    \_______/    1    \_______/  1     *
    *         /       \  2   8  /       \  6   8  /       \        *
    *        /    9    \_______/    9    \_______/    5    \       *
    *        \  2   4  /       \  6   4  /       \  7   8  /       *
    *      2  \_______/    1    \_______/    1    \_______/  2     *
    *         /       \  2   4  /       \  7   8  /       \        *
    *        /    9    \_______/    1    \_______/    5    \       *
    *        \  2   3  /       \  7   4  /       \  7   3  /       *
    *      3  \_______/    5    \_______/    5    \_______/  3     *
    *                 \  6   3  /       \  7   4  /                *
    *               4  \_______/    1    \_______/  4              *
    *                          \  7   3  /                         *
    *                        5  \_______/  5                       *
    *                                                              *
    ****************************************************************
    """

    boards[1] = Board()

    boards[1].place_tile(Tile(9,7,3), Pos('A1'))
    boards[1].place_tile(Tile(9,2,4), Pos('A2'))
    boards[1].place_tile(Tile(9,2,3), Pos('A3'))

    boards[1].place_tile(Tile(5,6,8), Pos('B1'))
    boards[1].place_tile(Tile(5,2,8), Pos('B2'))
    boards[1].place_tile(Tile(1,2,4), Pos('B3'))
    boards[1].place_tile(Tile(5,6,3), Pos('B4'))

    boards[1].place_tile(Tile(1,6,3), Pos('C1'))
    boards[1].place_tile(Tile(1,2,8), Pos('C2'))
    boards[1].place_tile(Tile(9,6,4), Pos('C3'))
    boards[1].place_tile(Tile(1,7,4), Pos('C4'))
    boards[1].place_tile(Tile(1,7,3), Pos('C5'))

    boards[1].place_tile(Tile(1,2,3), Pos('D1'))
    boards[1].place_tile(Tile(1,6,8), Pos('D2'))
    boards[1].place_tile(Tile(1,7,8), Pos('D3'))
    boards[1].place_tile(Tile(5,7,4), Pos('D4'))

    boards[1].place_tile(Tile(5,2,3), Pos('E1'))
    boards[1].place_tile(Tile(5,7,8), Pos('E2'))
    boards[1].place_tile(Tile(5,7,3), Pos('E3'))

    return boards[n]
     
def half_board(n:int = 1):
    boards = {}

    """ board 1
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

    """

    boards[1] = Board()

    boards[1].place_tile(Tile(5,2,8), Pos('A1'))
    boards[1].place_tile(Tile(5,6,4), Pos('A2'))

    boards[1].place_tile(Tile(1,2,3), Pos('B1'))
    boards[1].place_tile(Tile(1,7,8), Pos('B3'))

    boards[1].place_tile(Tile(9,2,3), Pos('C2'))

    boards[1].place_tile(Tile(5,6,8), Pos('D3'))
    boards[1].place_tile(Tile(5,7,8), Pos('D4'))

    boards[1].place_tile(Tile(1,6,3), Pos('E2'))

    """ board 2
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
    """

    boards[2] = Board()

    boards[2].place_tile(Tile(5,2,8), Pos('A1'))
    boards[2].place_tile(Tile(5,6,4), Pos('A2'))

    boards[2].place_tile(Tile(1,2,3), Pos('B1'))
    boards[2].place_tile(Tile(1,7,8), Pos('B3'))

    boards[2].place_tile(Tile(9,2,4), Pos('C1'))
    boards[2].place_tile(Tile(9,2,3), Pos('C2'))
    boards[2].place_tile(Tile(9,6,8), Pos('C4'))
    boards[2].place_tile(Tile(9,6,4), Pos('C5'))

    boards[2].place_tile(Tile(5,6,8), Pos('D3'))
    boards[2].place_tile(Tile(5,7,8), Pos('D4'))

    boards[2].place_tile(Tile(1,6,3), Pos('E2'))

    """ board 3
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
    """

    boards[3] = Board()

    boards[3].place_tile(Tile(5,2,8), Pos('A1'))
    boards[3].place_tile(Tile(5,6,4), Pos('A2'))

    boards[3].place_tile(Tile(1,2,3), Pos('B1'))
    boards[3].place_tile(Tile(9,2,8), Pos('B2'))
    boards[3].place_tile(Tile(1,7,8), Pos('B3'))

    boards[3].place_tile(Tile(9,2,4), Pos('C1'))
    boards[3].place_tile(Tile(9,2,3), Pos('C2'))
    boards[3].place_tile(Tile(9,6,8), Pos('C4'))
    boards[3].place_tile(Tile(9,6,4), Pos('C5'))

    boards[3].place_tile(Tile(9,7,3), Pos('D2'))
    boards[3].place_tile(Tile(5,6,8), Pos('D3'))
    boards[3].place_tile(Tile(5,7,8), Pos('D4'))

    boards[3].place_tile(Tile(1,6,3), Pos('E2'))
    boards[3].place_tile(Tile(1,6,8), Pos('E3'))

    """ board 4
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
    """

    boards[4] = Board()

    boards[4].place_tile(Tile(5,2,8), Pos('A1'))
    boards[4].place_tile(Tile(5,6,4), Pos('A2'))

    boards[4].place_tile(Tile(1,2,3), Pos('B1'))
    boards[4].place_tile(Tile(9,2,8), Pos('B2'))
    boards[4].place_tile(Tile(1,7,8), Pos('B3'))
        
    boards[4].place_tile(Tile(9,2,4), Pos('C1'))
    boards[4].place_tile(Tile(9,2,3), Pos('C2'))
    boards[4].place_tile(Tile(9,6,8), Pos('C4'))
    boards[4].place_tile(Tile(9,6,4), Pos('C5'))
        
    boards[4].place_tile(Tile(1,2,4), Pos('D1'))
    boards[4].place_tile(Tile(9,7,3), Pos('D2'))
    boards[4].place_tile(Tile(5,6,8), Pos('D3'))
    boards[4].place_tile(Tile(5,7,8), Pos('D4'))
        
    boards[4].place_tile(Tile(1,6,3), Pos('E2'))
    boards[4].place_tile(Tile(1,6,8), Pos('E3'))
        
    """ board 5
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
    """

    boards[5] = Board()

    boards[5].place_tile(Tile(5,2,8), Pos('A1'))
    boards[5].place_tile(Tile(5,6,4), Pos('A2'))
    boards[5].place_tile(Tile(5,6,3), Pos('A3'))

    boards[5].place_tile(Tile(1,2,3), Pos('B1'))
    boards[5].place_tile(Tile(9,2,8), Pos('B2'))
    boards[5].place_tile(Tile(1,7,8), Pos('B3'))

    boards[5].place_tile(Tile(9,2,4), Pos('C1'))
    boards[5].place_tile(Tile(9,2,3), Pos('C2'))
    boards[5].place_tile(Tile(9,6,8), Pos('C4'))
    boards[5].place_tile(Tile(9,6,4), Pos('C5'))

    boards[5].place_tile(Tile(1,2,4), Pos('D1'))
    boards[5].place_tile(Tile(9,7,3), Pos('D2'))
    boards[5].place_tile(Tile(5,6,8), Pos('D3'))
    boards[5].place_tile(Tile(5,7,8), Pos('D4'))

    boards[5].place_tile(Tile(1,7,4), Pos('E1'))
    boards[5].place_tile(Tile(1,6,3), Pos('E2'))
    boards[5].place_tile(Tile(1,6,8), Pos('E3'))

    """ board 6
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/         \_______                  *
    *             A    /       \         /       \    E            *
    *          _______/    1    \_______/         \_______         *
    *         /       \  6   3  /       \         /       \        *
    *        /         \_______/    9    \_______/    5    \       *
    *        \         /       \  6   3  /       \  7   4  /       *
    *      1  \_______/         \_______/         \_______/  1     *
    *         /       \         /       \         /       \        *
    *        /    9    \_______/         \_______/    5    \       *
    *        \  6   4  /       \         /       \  7   3  /       *
    *      2  \_______/    1    \_______/    5    \_______/  2     *
    *         /       \  2   4  /       \  7   8  /       \        *
    *        /    9    \_______/    9    \_______/    5    \       *
    *        \  2   8  /       \  7   4  /       \  6   3  /       *
    *      3  \_______/    9    \_______/    1    \_______/  3     *
    *                 \  7   8  /       \  6   4  /                *
    *               4  \_______/    1    \_______/  4              *
    *                          \  6   8  /                         *
    *                        5  \_______/  5                       *
    *                                                              *
    ****************************************************************
    """

    boards[6] = Board()

    boards[6].place_tile(Tile(9,6,8), Pos('A2'))
    boards[6].place_tile(Tile(9,2,8), Pos('A3'))

    boards[6].place_tile(Tile(1,6,3), Pos('B1'))
    boards[6].place_tile(Tile(1,2,4), Pos('B3'))
    boards[6].place_tile(Tile(9,7,8), Pos('B4'))

    boards[6].place_tile(Tile(9,6,3), Pos('C2'))
    boards[6].place_tile(Tile(9,7,4), Pos('C4'))
    boards[6].place_tile(Tile(1,6,8), Pos('C5'))

    boards[6].place_tile(Tile(5,7,8), Pos('D3'))
    boards[6].place_tile(Tile(1,6,4), Pos('D4'))

    boards[6].place_tile(Tile(5,7,4), Pos('E1'))
    boards[6].place_tile(Tile(5,7,4), Pos('E2'))
    boards[6].place_tile(Tile(5,6,3), Pos('E3'))
        
    # select board
        
    return boards[n]

def almost_full_board(n:int = 1):
    boards = {}

    """ board 1
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/         \_______                  *
    *             A    /       \         /       \    E            *
    *          _______/         \_______/    5    \_______         *
    *         /       \         /       \  6   4  /       \        *
    *        /    5    \_______/    1    \_______/         \       *
    *        \  7   4  /       \  6   3  /       \         /       *
    *      1  \_______/    9    \_______/    5    \_______/  1     *
    *         /       \  6   3  /       \  6   3  /       \        *
    *        /    5    \_______/    1    \_______/    9    \       *
    *        \  6   8  /       \  7   3  /       \  2   3  /       *
    *      2  \_______/    9    \_______/    1    \_______/  2     *
    *         /       \  2   4  /       \  2   3  /       \        *
    *        /    5    \_______/    1    \_______/    5    \       *
    *        \  7   8  /       \  2   4  /       \  2   8  /       *
    *      3  \_______/    9    \_______/    5    \_______/  3     *
    *                 \  6   8  /       \  7   3  /                *
    *               4  \_______/    1    \_______/  4              *
    *                          \  2   8  /                         *
    *                        5  \_______/  5                       *
    *                                                              *
    ****************************************************************"""

    boards[1] = Board()

    boards[1].place_tile(Tile(5,7,4), Pos('A1'))
    boards[1].place_tile(Tile(5,6,8), Pos('A2'))
    boards[1].place_tile(Tile(5,7,8), Pos('A3'))

    boards[1].place_tile(Tile(9,6,3), Pos('B2'))
    boards[1].place_tile(Tile(9,2,4), Pos('B3'))
    boards[1].place_tile(Tile(9,6,8), Pos('B4'))

    boards[1].place_tile(Tile(1,6,3), Pos('C2'))
    boards[1].place_tile(Tile(1,7,3), Pos('C3'))
    boards[1].place_tile(Tile(1,2,4), Pos('C4'))
    boards[1].place_tile(Tile(1,2,8), Pos('C5'))

    boards[1].place_tile(Tile(5,6,8), Pos('D1'))
    boards[1].place_tile(Tile(5,6,3), Pos('D2'))
    boards[1].place_tile(Tile(1,2,3), Pos('D3'))
    boards[1].place_tile(Tile(5,7,3), Pos('D4'))

    boards[1].place_tile(Tile(9,2,3), Pos('E2'))
    boards[1].place_tile(Tile(5,2,8), Pos('E3'))

    """ board 2
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/    5    \_______                  *
    *             A    /       \  2   3  /       \    E            *
    *          _______/         \_______/    5    \_______         *
    *         /       \         /       \  6   4  /       \        *
    *        /    5    \_______/    1    \_______/         \       *
    *        \  7   4  /       \  6   3  /       \         /       *
    *      1  \_______/    9    \_______/    5    \_______/  1     *
    *         /       \  6   3  /       \  6   3  /       \        *
    *        /    5    \_______/    1    \_______/    9    \       *
    *        \  6   8  /       \  7   3  /       \  2   3  /       *
    *      2  \_______/    9    \_______/    1    \_______/  2     *
    *         /       \  2   4  /       \  2   3  /       \        *
    *        /    5    \_______/    1    \_______/    5    \       *
    *        \  7   8  /       \  2   4  /       \  2   8  /       *
    *      3  \_______/    9    \_______/    5    \_______/  3     *
    *                 \  6   8  /       \  7   3  /                *
    *               4  \_______/    1    \_______/  4              *
    *                          \  2   8  /                         *
    *                        5  \_______/  5                       *
    *                                                              *
    ****************************************************************
    """

    boards[2] = Board()

    boards[2].place_tile(Tile(5,7,4), Pos('A1'))
    boards[2].place_tile(Tile(5,6,8), Pos('A2'))
    boards[2].place_tile(Tile(5,7,8), Pos('A3'))

    boards[2].place_tile(Tile(9,6,3), Pos('B2'))
    boards[2].place_tile(Tile(9,2,4), Pos('B3'))
    boards[2].place_tile(Tile(9,6,8), Pos('B4'))

    boards[2].place_tile(Tile(5,2,3), Pos('C1'))
    boards[2].place_tile(Tile(1,6,3), Pos('C2'))
    boards[2].place_tile(Tile(1,7,3), Pos('C3'))
    boards[2].place_tile(Tile(1,2,4), Pos('C4'))
    boards[2].place_tile(Tile(1,2,8), Pos('C5'))

    boards[2].place_tile(Tile(5,6,8), Pos('D1'))
    boards[2].place_tile(Tile(5,6,3), Pos('D2'))
    boards[2].place_tile(Tile(1,2,3), Pos('D3'))
    boards[2].place_tile(Tile(5,7,3), Pos('D4'))

    boards[2].place_tile(Tile(9,2,3), Pos('E2'))
    boards[2].place_tile(Tile(5,2,8), Pos('E3'))

    """ board 3
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/    5    \_______                  *
    *             A    /       \  2   3  /       \    E            *
    *          _______/         \_______/    5    \_______         *
    *         /       \         /       \  6   4  /       \        *
    *        /    5    \_______/    1    \_______/    5    \       *
    *        \  7   4  /       \  6   3  /       \  2   4  /       *
    *      1  \_______/    9    \_______/    5    \_______/  1     *
    *         /       \  6   3  /       \  6   3  /       \        *
    *        /    5    \_______/    1    \_______/    9    \       *
    *        \  6   8  /       \  7   3  /       \  2   3  /       *
    *      2  \_______/    9    \_______/    1    \_______/  2     *
    *         /       \  2   4  /       \  2   3  /       \        *
    *        /    5    \_______/    1    \_______/    5    \       *
    *        \  7   8  /       \  2   4  /       \  2   8  /       *
    *      3  \_______/    9    \_______/    5    \_______/  3     *
    *                 \  6   8  /       \  7   3  /                *
    *               4  \_______/    1    \_______/  4              *
    *                          \  2   8  /                         *
    *                        5  \_______/  5                       *
    *                                                              *
    ****************************************************************
    """

    boards[3] = Board()

    boards[3].place_tile(Tile(5,7,4), Pos('A1'))
    boards[3].place_tile(Tile(5,6,8), Pos('A2'))
    boards[3].place_tile(Tile(5,7,8), Pos('A3'))

    boards[3].place_tile(Tile(9,6,3), Pos('B2'))
    boards[3].place_tile(Tile(9,2,4), Pos('B3'))
    boards[3].place_tile(Tile(9,6,8), Pos('B4'))

    boards[3].place_tile(Tile(5,2,3), Pos('C1'))
    boards[3].place_tile(Tile(1,6,3), Pos('C2'))
    boards[3].place_tile(Tile(1,7,3), Pos('C3'))
    boards[3].place_tile(Tile(1,2,4), Pos('C4'))
    boards[3].place_tile(Tile(1,2,8), Pos('C5'))

    boards[3].place_tile(Tile(5,6,8), Pos('D1'))
    boards[3].place_tile(Tile(5,6,3), Pos('D2'))
    boards[3].place_tile(Tile(1,2,3), Pos('D3'))
    boards[3].place_tile(Tile(5,7,3), Pos('D4'))

    boards[3].place_tile(Tile(5,2,4), Pos('E1'))
    boards[3].place_tile(Tile(9,2,3), Pos('E2'))
    boards[3].place_tile(Tile(5,2,8), Pos('E3'))

    # select board
        
    return boards[n]

    
class TestScore(unittest.TestCase):

    def test_score_1(self):
        board = full_board(1)
        self.assertEqual(board.score(), 137)


class TestPlacement(unittest.TestCase):

    def test_1(self):
        """
        half board 1
          _______  
         /       \  
        /    5    \  ==>  D2
        \  7   3  / 
         \_______/  
        """
        
        board = half_board(1)
        
        suggested_position = AI.get_best_position(board, Tile(5,7,3))
        
        self.assertEqual(suggested_position, Pos('D2'))

    def test_2(self):
        """
        half board 2
          _______  
         /       \  
        /    9    \  ==>  B4
        \  6   3  / 
         \_______/  
        """
        
        board = half_board(2)
        
        suggested_position = AI.get_best_position(board, Tile(9,6,4))
        
        self.assertEqual(suggested_position, Pos('B4'))

    def test_3(self):
        """
        half board 3
          _______  
         /       \  
        /    1    \  ==>  D1
        \  2   4  / 
         \_______/  
        """
        
        board = half_board(3)
        
        suggested_position = AI.get_best_position(board, Tile(1,2,4))
        
        self.assertEqual(suggested_position, Pos('D1'))

    def test_4(self):
        """
        half board 4
          _______  
         /       \  
        /    1    \  ==>  E1
        \  7   4  / 
         \_______/  
        """
        
        board = half_board(4)
        
        suggested_position = AI.get_best_position(board, Tile(1,7,4))
        
        self.assertEqual(suggested_position, Pos('E1'))

    def test_5(self):
        """
        half board 5
          _______  
         /       \  
        /    5    \  ==>  B4
        \  7   4  / 
         \_______/  
        """
        
        board = half_board(5)
        
        suggested_position = AI.get_best_position(board, Tile(5,7,4))
        
        self.assertEqual(suggested_position, Pos('B4'))

class TestGameScore(unittest.TestCase):

    def test_score_1(self):
        """At least score 130 at depth 2"""
        board = Board()
        tiles = [
            Tile(5,2,3),
            Tile(1,6,8),
            Tile(5,2,4),
            Tile(1,6,3),
            Tile(9,6,4),
            Tile(9,7,8),
            Tile(5,7,8),
            Tile(5,6,8),
            Tile(5,2,8),
            Tile(9,2,4),
            Tile(5,6,3),
            Tile(5,6,4),
            Tile(1,2,4),
            Tile(9,6,3),
            Tile(1,7,8),
            Tile(9,7,4),
            Tile(5,7,3),
            Tile(9,2,8),
            Tile(1,2,3),
            Tile(1,6,4),
            Tile(9,2,3),
            Tile(9,6,8),
            Tile(9,7,3),
            Tile(1,7,3),
            Tile(1,2,8),
            Tile(5,7,4),
            Tile(1,7,4),
        ]
        
        while any(board.open_positions()):
            tile = tiles.pop()
            position = AI.get_best_position(board, tile)
            board.place_tile(tile, position)
            # board.draw()
        
        self.assertGreater(board.score(), 130)

    def test_score_2(self):
        """At least score 130 at depth 2"""
        board = Board()
        tiles = [
            Tile(9,2,8),
            Tile(5,7,4),
            Tile(1,2,3),
            Tile(9,2,4),
            Tile(9,7,8),
            Tile(9,6,8),
            Tile(1,6,3),
            Tile(1,7,4),
            Tile(5,7,3),
            Tile(5,6,8),
            Tile(5,2,3),
            Tile(1,6,8),
            Tile(9,6,3),
            Tile(5,7,8),
            Tile(1,6,4),
            Tile(9,7,3),
            Tile(5,2,4),
            Tile(9,7,4),
            Tile(9,2,3),
            Tile(5,6,4),
            Tile(9,6,4),
            Tile(1,7,8),
            Tile(1,7,3),
            Tile(5,2,8),
            Tile(1,2,4),
            Tile(1,2,8),
            Tile(5,6,3),
        ]
        
        while any(board.open_positions()):
            tile = tiles.pop()
            position = AI.get_best_position(board, tile)
            board.place_tile(tile, position)
            # board.draw()
        
        self.assertGreater(board.score(), 130)

class TestEstimatedScore(unittest.TestCase):

    def _test_estimated_score(self, board: Board, tolerance:float = 0.1, debug=True):
        
        estimated_score_level_1 = AI.estimated_score(board)
        
        scores_for_tiles = {}
        for tile in board.remaining_tiles():
            scores_for_positions = {}
            for position in board.open_positions():
                new_board = copy(board)
                new_board.place_tile(tile, position)
                scores_for_positions[position] = AI.estimated_score(new_board)
            scores_for_tiles[tile] = max(scores_for_positions.values())
        
        estimated_score_level_2 = mean(scores_for_tiles.values())
        if debug: 
            print(f'{round(estimated_score_level_1,2)} | {[round(score,2) for score in scores_for_tiles.values()]} -> {round(estimated_score_level_2,2)}')
        
        self.assertAlmostEqual(1, estimated_score_level_2 / estimated_score_level_1, delta=tolerance,
                               msg=f'{round(estimated_score_level_1, 2)} != {round(estimated_score_level_2, 2)}')

    def test_1(self):
        self._test_estimated_score(half_board(1))

    def test_2(self):
        self._test_estimated_score(half_board(2))
        
    def test_3(self):
        self._test_estimated_score(half_board(3))

    def test_4(self):
        self._test_estimated_score(half_board(4))
        
    def test_5(self):
        self._test_estimated_score(half_board(5))

    def test_6(self):
        self._test_estimated_score(half_board(6))

    def test_7(self):
        self._test_estimated_score(almost_full_board(1))
        
    def test_8(self):
        self._test_estimated_score(almost_full_board(2))
        
    def test_9(self):
        self._test_estimated_score(almost_full_board(3))
        
        
if __name__ == '__main__':
    unittest.main()
