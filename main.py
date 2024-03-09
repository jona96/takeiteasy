import random


class Tile:
    def __init__(self, n1, n2, n3):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

    def __repr__(self) -> str:
        return f'({self.n1},{self.n2},{self.n3})'
    
class Tiles:

    _all_tiles = [
        Tile(1, 2, 3), Tile(1, 2, 4), Tile(1, 2, 8),
        Tile(1, 6, 3), Tile(1, 6, 4), Tile(1, 6, 8),
        Tile(1, 7, 3), Tile(1, 7, 4), Tile(1, 7, 8),
        Tile(5, 2, 3), Tile(5, 2, 4), Tile(5, 2, 8),
        Tile(5, 6, 3), Tile(5, 6, 4), Tile(5, 6, 8),
        Tile(5, 7, 3), Tile(5, 7, 4), Tile(5, 7, 8),
        Tile(9, 2, 3), Tile(9, 2, 4), Tile(9, 2, 8),
        Tile(9, 6, 3), Tile(9, 6, 4), Tile(9, 6, 8),
        Tile(9, 7, 3), Tile(9, 7, 4), Tile(9, 7, 8),
    ]

    def __init__(self):
        self.left_tiles = Tiles._all_tiles

    def pick_tile(self):
        if not any(self.left_tiles):
            return None
        index_of_tile = int(random.random() * len(self.left_tiles))
        return self.left_tiles.pop(index_of_tile)


class Board:

    LAYOUT = """
    ****************************************************************
    *                               C                              *
    *                            _______                           *
    *                      B    /       \    D                     *
    *                   _______/         \_______                  *
    *             A    /       \         /       \    E            *
    *          _______/         \_______/         \_______         *
    *         /       \         /       \         /       \        *
    *        /         \_______/         \_______/         \       *
    *        \         /       \         /       \         /       *
    *      1  \_______/         \_______/         \_______/  1     *
    *         /       \         /       \         /       \        *
    *        /         \_______/         \_______/         \       *
    *        \         /       \         /       \         /       *
    *      2  \_______/         \_______/         \_______/  2     *
    *         /       \         /       \         /       \        *
    *        /         \_______/         \_______/         \       *
    *        \         /       \         /       \         /       *
    *      3  \_______/         \_______/         \_______/  3     *
    *                 \         /       \         /                *
    *               4  \_______/         \_______/  4              *
    *                          \         /                         *
    *                        5  \_______/                          *
    *                                                              *
    ****************************************************************
"""

    def __init__(self):
        self.tiles = {}  # layout 'A1' : Tile(1, 2, 3)

    def place_tile(self, tile: Tile, position: str):
        assert len(position) == 2
        column = position[0]
        row = position[1]
        assert row.isnumeric()
        row = int(row)
        column = column.upper()
        assert column in ['A', 'B', 'C', 'D', 'E']
        if column in ['A', 'E']: assert row in [1, 2, 3]
        if column in ['B', 'D']: assert row in [1, 2, 3, 4]
        if column in ['C']: assert row in [1, 2, 3, 4, 5]
        
        index = f'{column}{row}'
        assert index not in self.tiles.keys()
        
        self.tiles[index] = tile
        
        self.draw()

    def draw(self):
        print(self.LAYOUT)
        print(self.tiles)
        print(f'score: {self.score()}')

    def score(self) -> int:
        return sum([tile.n1 + tile.n2 + tile.n3 for tile in self.tiles.values()])

if __name__ == '__main__':
    tiles = Tiles()

    board = Board()
    board.draw()

    for _ in range(19):
        tile = tiles.pick_tile()
        board.place_tile(tile, input(f'where to place {tile}? '))
