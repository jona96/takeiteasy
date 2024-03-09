import random


def all_items_equal(l:list) -> bool:
    assert isinstance(l, list)
    return len(set(l)) == 1

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

    @staticmethod
    def max_row(column: str) -> int:
        assert column in ['A','B','C','D','E']
        if column in ['A', 'E']: return 3
        if column in ['B', 'D']: return 4
        if column in ['C']: return 5

    def place_tile(self, tile: Tile, position: str):
        assert len(position) == 2
        column = position[0]
        row = position[1]
        assert row.isnumeric()
        row = int(row)
        column = column.upper()
        assert column in ['A', 'B', 'C', 'D', 'E']
        assert row in range(1, Board.max_row(column) + 1)
        
        index = f'{column}{row}'
        assert index not in self.tiles.keys()
        
        self.tiles[index] = tile
        
        self.draw()

    def draw(self):

        def position_in_layout(index: str, nx: int) -> int:
            assert nx in ['n1', 'n2', 'n3']
            
            column = index[0]
            row = int(index[1])
            
            characters_per_line = 69
            lines_per_row = 4
            
            column_offset = {
                'A' : 571,
                'B' : 442,
                'C' : 313,
                'D' : 460,
                'E' : 607,
            }
            
            n_offset = {
                'n1' : 0,
                'n2' : 67,
                'n3' : 71
            }
            
            return column_offset[column] + n_offset[nx] + (row - 1) * characters_per_line * lines_per_row
        def replace_character(text: str, index: int, new_character: str) -> str:
            return text[:index] + str(new_character) + text[index + 1:]
        
        board_string = self.LAYOUT
        for index, tile in self.tiles.items():
            board_string = replace_character(board_string, position_in_layout(index, 'n1'), tile.n1)
            board_string = replace_character(board_string, position_in_layout(index, 'n2'), tile.n2)
            board_string = replace_character(board_string, position_in_layout(index, 'n3'), tile.n3)
        print(board_string)
        print(f'score: {self.score()}')

    def score(self) -> int:
        def column_score(column) -> int:
            n1 = []
            for row in range(1, Board.max_row(column) + 1):
                index = f'{column}{row}'
                if index not in self.tiles.keys(): # no tile set
                    n1.append(0)
                else:
                    n1.append(self.tiles[index].n1)
            
            if all_items_equal(n1):
                return sum(n1)
            else:
                return 0
        
        
        return sum([column_score(column) for column in ['A', 'B', 'C', 'D', 'E']])

if __name__ == '__main__':
    tiles = Tiles()

    board = Board()
    board.draw()

    for _ in range(19):
        tile = tiles.pick_tile()
        board.place_tile(tile, input(f'where to place {tile}? '))
