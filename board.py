from dataclasses import dataclass
from tiles import Tile, Tiles


def all_items_equal(l:list) -> bool:
    assert isinstance(l, list)
    return len(set(l)) == 1

@dataclass(frozen=True)
class BoardPosition:
    column: str
    row: int
    
    def __post_init__(self):
        assert isinstance(self.column, str)
        assert self.column == self.column.upper()
        assert isinstance(self.row, int)

    def __repr__(self) -> str:
        return f'{self.column}{self.row}'

    @classmethod
    def from_string(cls, position: str):
        return cls(position[0].upper(), int(position[1]))

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

    SCORE_GROUPS = {
        'n1' : [
            [ BoardPosition('A', 1), BoardPosition('A', 2), BoardPosition('A', 3) ],
            [ BoardPosition('B', 1), BoardPosition('B', 2), BoardPosition('B', 3), BoardPosition('B', 4) ],
            [ BoardPosition('C', 1), BoardPosition('C', 2), BoardPosition('C', 3), BoardPosition('C', 4), BoardPosition('C', 5) ],
            [ BoardPosition('D', 1), BoardPosition('D', 2), BoardPosition('D', 3), BoardPosition('D', 4) ],
            [ BoardPosition('E', 1), BoardPosition('E', 2), BoardPosition('E', 3) ],
        ],
        'n2' : [
            [ BoardPosition('A', 1), BoardPosition('B', 1), BoardPosition('C', 1) ],
            [ BoardPosition('A', 2), BoardPosition('B', 2), BoardPosition('C', 2), BoardPosition('D', 1) ],
            [ BoardPosition('A', 3), BoardPosition('B', 3), BoardPosition('C', 3), BoardPosition('D', 2), BoardPosition('E', 1) ],
            [                        BoardPosition('B', 4), BoardPosition('C', 4), BoardPosition('D', 3), BoardPosition('E', 2) ],
            [                                               BoardPosition('C', 5), BoardPosition('D', 4), BoardPosition('E', 3) ],
        ],
        'n3' : [
            [                                               BoardPosition('C', 1), BoardPosition('D', 1), BoardPosition('E', 1) ],
            [                        BoardPosition('B', 1), BoardPosition('C', 2), BoardPosition('D', 2), BoardPosition('E', 2) ],
            [ BoardPosition('A', 1), BoardPosition('B', 2), BoardPosition('C', 3), BoardPosition('D', 3), BoardPosition('E', 3) ],
            [ BoardPosition('A', 2), BoardPosition('B', 3), BoardPosition('C', 4), BoardPosition('D', 4) ],
            [ BoardPosition('A', 3), BoardPosition('B', 4), BoardPosition('C', 5) ],
        ],
    }

    def __init__(self):
        self._tiles = {}  # layout BoardPosition('A', 1) : Tile(1, 2, 3)

    def place_tile(self, tile: Tile, position: BoardPosition):
        assert position in self.open_positions()
        
        self._tiles[position] = tile

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
        print(f'max score: {self.max_score()}')

    def score(self) -> int:
        score = 0

        for nx in ['n1', 'n2', 'n3']:
            for group in self.SCORE_GROUPS[nx]:
                number_list = []
                for board_position in group:
                    tile = self.tiles().get(board_position, Tile(0, 0, 0)) # 0-Tile if no tile is set
                    number = getattr(tile, nx)
                    number_list.append(number)
                score += sum(number_list) if all_items_equal(number_list) else 0

        return score

    def max_score(self) -> int:
        score = 0

        max_numbers = {
            'n1' : 9,
            'n2' : 7,
            'n3' : 8,
        }

        for nx in ['n1', 'n2', 'n3']:
            for group in self.SCORE_GROUPS[nx]:
                number_list = []
                for board_position in group:
                    if board_position in self.tiles().keys():
                        tile = self.tiles()[board_position]
                        number = getattr(tile, nx)
                        number_list.append(number)
                if not any(number_list):   # no tile set, assume max value 
                    score += max_numbers[nx] * len(group)
                elif all_items_equal(number_list):  # so far all number the same
                    score += number_list[0] * len(group)
                else:       # different tiles -> no way to safe the row
                    score += 0

        return score
       
    def tiles(self) -> dict[BoardPosition, Tile]:
        return self._tiles

    def position_of_tile(self, tile:Tile) -> BoardPosition | None:
        if tile not in self._tiles.values():
            return None
        else:
            return [key for key, value in self._tiles.items() if value == tile][0]

    def remaining_tiles(self) -> list[Tile]:
        return [tile for tile in Tiles.ALL_TILES if tile not in self.tiles().values()]
    
    def open_positions(self) -> list[BoardPosition]:
        return [pos for pos in self.ALL_POSITIONS if pos not in self.tiles().keys()]