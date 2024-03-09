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
    *                        5  \_______/  5                       *
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

    @staticmethod
    def all_rows(column: str) -> list[int]:
        return range(1, Board.max_row(column) + 1)

    @staticmethod
    def all_columns() -> list[str]:
        return ['A', 'B', 'C', 'D', 'E']

    def place_tile(self, tile: Tile, position: str):
        assert len(position) == 2
        column = position[0]
        row = position[1]
        assert row.isnumeric()
        row = int(row)
        column = column.upper()
        assert column in Board.all_columns()
        assert row in Board.all_rows(column)
        
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
            for row in Board.all_rows(column):
                index = f'{column}{row}'
                n1.append(self.tiles.get(index, Tile(0, 0, 0)).n1) # 0-tile is default
            return sum(n1) if all_items_equal(n1) else 0

        def row_from_left_score(row) -> int:
            indices_for_row_from_left = {
                1: ['A1', 'B1', 'C1'],
                2: ['A2', 'B2', 'C2', 'D1'],
                3: ['A3', 'B3', 'C3', 'D2', 'E1'],
                4: [      'B4', 'C4', 'D3', 'E2'],
                5: [            'C5', 'D4', 'E3'],
            }
            n2 = []
            for index in indices_for_row_from_left[row]:
                n2.append(self.tiles.get(index, Tile(0, 0, 0)).n2) # 0-tile is default
            return sum(n2) if all_items_equal(n2) else 0
        

        def row_from_right_score(row) -> int:
            indices_for_row_from_left = {
                1: [            'C1', 'D1', 'E1'],
                2: [      'B1', 'C2', 'D2', 'E2'],
                3: ['A1', 'B2', 'C3', 'D3', 'E3'],
                4: ['A2', 'B3', 'C4', 'D4'],
                5: ['A3', 'B4', 'C5'],
            }
            n3 = []
            for index in indices_for_row_from_left[row]:
                n3.append(self.tiles.get(index, Tile(0, 0, 0)).n3) # 0-tile is default
            return sum(n3) if all_items_equal(n3) else 0
        
        score = 0
        for column in Board.all_columns():
            score += column_score(column)
        for row in [1, 2, 3, 4, 5]:
            score += row_from_left_score(row)
            score += row_from_right_score(row)
        return score

    def tiles(self) -> dict[str, Tile]:
        return self.tiles

class GameNotRunningException(Exception):
    pass
class GameCannotPlaceTileException(Exception):
    pass

class Game:
    
    def __init__(self) -> None:
        self.tiles = Tiles()
        self.board = Board()
        self.started = False
        self._finished = False
        self.current_tile = None

    def start(self):
        self.started = True
        self.current_tile = self.tiles.pick_tile()
        print(self.board.draw())

    def get_tile(self) -> Tile:
        if not self.started:
            raise GameNotRunningException()
        return self.current_tile
    
    def place_tile(self, position: str):
        if self.finished(): return
        try:
            self.board.place_tile(self.current_tile, position)
        except Exception as e: raise GameCannotPlaceTileException(e)
        
        self.current_tile = self.tiles.pick_tile()
        
        if len(self.board.tiles()) == 19:
            self._finished = True

    def finished(self) -> bool:
        return self._finished

if __name__ == '__main__':

    game = Game()
    game.start()
    while not game.finished():
        print(f'The current tile is: {game.get_tile()}')
        position = input('position for current Tile (e.g. C3): ')
        try:
            game.place_tile(position)
        except:
            print(f'Could not place the tile on {position}. Try again.')
    
        
