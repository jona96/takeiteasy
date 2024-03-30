from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Tile:
    n1: int
    n2: int
    n3: int

    def __post_init__(self):
        assert self.n1 in [0, 1, 5, 9]
        assert self.n2 in [0, 2, 6, 7]
        assert self.n3 in [0, 3, 4, 8]

    def __repr__(self) -> str:
        return f'({self.n1},{self.n2},{self.n3})'
    
class Tiles:

    ALL_TILES = {
        Tile(1, 2, 3), Tile(1, 2, 4), Tile(1, 2, 8),
        Tile(1, 6, 3), Tile(1, 6, 4), Tile(1, 6, 8),
        Tile(1, 7, 3), Tile(1, 7, 4), Tile(1, 7, 8),
        Tile(5, 2, 3), Tile(5, 2, 4), Tile(5, 2, 8),
        Tile(5, 6, 3), Tile(5, 6, 4), Tile(5, 6, 8),
        Tile(5, 7, 3), Tile(5, 7, 4), Tile(5, 7, 8),
        Tile(9, 2, 3), Tile(9, 2, 4), Tile(9, 2, 8),
        Tile(9, 6, 3), Tile(9, 6, 4), Tile(9, 6, 8),
        Tile(9, 7, 3), Tile(9, 7, 4), Tile(9, 7, 8),
    }

    def __init__(self, already_set_tiles: set[Tile] = set()):
        self._left_tiles = Tiles.ALL_TILES - already_set_tiles

    def pick_tile(self):
        if not any(self._left_tiles):
            return None
        tile = random.sample(list(self._left_tiles), 1)[0]
        self._left_tiles.remove(tile)
        return tile


if __name__ == '__main__':
    tiles = Tiles()
    while any(tiles._left_tiles):
        print(tiles.pick_tile())