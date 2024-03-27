from dataclasses import dataclass
from tiles import Tile


def all_items_equal(l:list) -> bool:
    assert isinstance(l, list)
    return len(set(l)) == 1

@dataclass(frozen=True)
class BoardPosition:
    column: str
    row: int
    
    def __repr__(self) -> str:
        return f'{self.column}{self.row}'

    @classmethod
    def from_string(cls, position: str):
        return cls(position[0], int(position[1]))

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

    ALL_POSITIONS = [
        BoardPosition('A', 1),
        BoardPosition('A', 2),
        BoardPosition('A', 3),
        BoardPosition('B', 1),
        BoardPosition('B', 2),
        BoardPosition('B', 3),
        BoardPosition('B', 4),
        BoardPosition('C', 1),
        BoardPosition('C', 2),
        BoardPosition('C', 3),
        BoardPosition('C', 4),
        BoardPosition('C', 5),
        BoardPosition('D', 1),
        BoardPosition('D', 2),
        BoardPosition('D', 3),
        BoardPosition('D', 4),
        BoardPosition('E', 1),
        BoardPosition('E', 2),
        BoardPosition('E', 3),
    ]

    def __init__(self):
        self._tiles = {}  # layout BoardPosition('A', 1) : Tile(1, 2, 3)
        self._tiles_old = {}  # layout 'A1' : Tile(1, 2, 3)

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

    def place_tile(self, tile: Tile, position: BoardPosition):
        assert position in Board.ALL_POSITIONS
        assert position not in self._tiles.keys()
        
        self._tiles[position] = tile
        
        self.draw()

    def draw(self):

        def position_in_layout(board_position: BoardPosition, nx: int) -> int:
            assert nx in ['n1', 'n2', 'n3']
            
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
            
            return column_offset[board_position.column] + n_offset[nx] + (board_position.row - 1) * characters_per_line * lines_per_row
        def replace_character(text: str, index: int, new_character: str) -> str:
            return text[:index] + str(new_character) + text[index + 1:]
        
        board_string = self.LAYOUT
        for board_position, tile in self._tiles.items():
            board_string = replace_character(board_string, position_in_layout(board_position, 'n1'), tile.n1)
            board_string = replace_character(board_string, position_in_layout(board_position, 'n2'), tile.n2)
            board_string = replace_character(board_string, position_in_layout(board_position, 'n3'), tile.n3)
        print(board_string)
        print(f'score: {self.score()}')

    def draw_old(self):

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
        for index, tile in self._tiles_old.items():
            board_string = replace_character(board_string, position_in_layout(index, 'n1'), tile.n1)
            board_string = replace_character(board_string, position_in_layout(index, 'n2'), tile.n2)
            board_string = replace_character(board_string, position_in_layout(index, 'n3'), tile.n3)
        print(board_string)
        print(f'score: {self.score_old()}')

    def score(self) -> int:
        def column_score(column) -> int:
            n1 = []
            for row in Board.all_rows(column):
                board_position = BoardPosition(column, row)
                n1.append(self._tiles.get(board_position, Tile(0, 0, 0)).n1) # 0-tile is default
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
            for board_position in [BoardPosition.from_string(s) for s in indices_for_row_from_left[row]]:
                n2.append(self._tiles.get(board_position, Tile(0, 0, 0)).n2) # 0-tile is default
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
            for board_position in [BoardPosition.from_string(s) for s in indices_for_row_from_left[row]]:
                n3.append(self._tiles.get(board_position, Tile(0, 0, 0)).n3) # 0-tile is default
            return sum(n3) if all_items_equal(n3) else 0
        
        score = 0
        for column in Board.all_columns():
            score += column_score(column)
        for row in [1, 2, 3, 4, 5]:
            score += row_from_left_score(row)
            score += row_from_right_score(row)
        return score

    def score_old(self) -> int:
        def column_score(column) -> int:
            n1 = []
            for row in Board.all_rows(column):
                index = f'{column}{row}'
                n1.append(self._tiles_old.get(index, Tile(0, 0, 0)).n1) # 0-tile is default
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
                n2.append(self._tiles_old.get(index, Tile(0, 0, 0)).n2) # 0-tile is default
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
                n3.append(self._tiles_old.get(index, Tile(0, 0, 0)).n3) # 0-tile is default
            return sum(n3) if all_items_equal(n3) else 0
        
        score = 0
        for column in Board.all_columns():
            score += column_score(column)
        for row in [1, 2, 3, 4, 5]:
            score += row_from_left_score(row)
            score += row_from_right_score(row)
        return score

    def tiles(self) -> dict[str, Tile]:
        return self._tiles
