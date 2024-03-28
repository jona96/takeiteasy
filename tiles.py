from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Tile:
    n1: int
    n2: int
    n3: int

    def __repr__(self) -> str:
        return f'({self.n1},{self.n2},{self.n3})'
    
class Tiles:

    ALL_TILES = [
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
        self._left_tiles = Tiles.ALL_TILES

    def pick_tile(self):
        if not any(self._left_tiles):
            return None
        index_of_tile = int(random.random() * len(self._left_tiles))
        return self._left_tiles.pop(index_of_tile)
