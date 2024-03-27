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

    def place_tile(self, tile: Tile, position: BoardPosition):
        assert position in Board.ALL_POSITIONS
        assert position not in self._tiles.keys()
        
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

    def score(self) -> int:
        score_groups = {
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
                [                        BoardPosition('D', 4), BoardPosition('C', 4), BoardPosition('D', 3), BoardPosition('E', 2) ],
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

        score = 0

        for nx in ['n1', 'n2', 'n3']:
            for group in score_groups[nx]:
                number_list = []
                for board_position in group:
                    tile = self.tiles().get(board_position, Tile(0, 0, 0)) # 0-Tile if no tile is set
                    number = getattr(tile, nx)
                    number_list.append(number)
                score += sum(number_list) if all_items_equal(number_list) else 0

        return score
                
    def tiles(self) -> dict[str, Tile]:
        return self._tiles
