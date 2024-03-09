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

    def __init__(self):
        pass

    def place_tile(self, tile: Tile):
        pass

    def draw(self):
        print("""
    *******************************************************
    *                      _______                        *
    *                     /       \                       *
    *             _______/    1    \_______               *
    *            /       \  3   2  /       \              *
    *    _______/    1    \_______/    1    \_______      *
    *   /       \  3   2  /       \  3   2  /       \     *
    *  /    1    \_______/    1    \_______/    1    \    *
    *  \  3   2  /       \  3   2  /       \  3   2  /    *
    *   \_______/    1    \_______/    1    \_______/     *
    *   /       \  3   2  /       \  3   2  /       \     *
    *  /    1    \_______/    1    \_______/    1    \    *
    *  \  3   2  /       \  3   2  /       \  3   2  /    *
    *   \_______/    1    \_______/    1    \_______/     *
    *   /       \  3   2  /       \  3   2  /       \     *
    *  /    1    \_______/    1    \_______/    1    \    *
    *  \  3   2  /       \  3   2  /       \  3   2  /    *
    *   \_______/    1    \_______/    1    \_______/     *
    *           \  3   2  /       \  3   2  /             *
    *            \_______/    1    \_______/              *
    *                    \  3   2  /                      *
    *                     \_______/                       *
    *                                                     *
    *******************************************************
""")



if __name__ == '__main__':
    tiles = Tiles()

    board = Board()
    
    board.place_tile(tiles.pick_tile())
    board.place_tile(tiles.pick_tile())
    board.place_tile(tiles.pick_tile())
    board.place_tile(tiles.pick_tile())

    board.draw()
