from copy import deepcopy
from statistics import mean
from ai import AI
from board import Board
from tiles import Tile, Tiles


tile_set_1 = [
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
    
tile_set_2 = [
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

tile_set_3 = [
    Tile(1,6,4),
    Tile(5,7,8),
    Tile(9,7,3),
    Tile(9,6,4),
    Tile(5,7,4),
    Tile(5,6,8),
    Tile(9,7,4),
    Tile(1,7,3),
    Tile(9,6,8),
    Tile(5,7,3),
    Tile(9,2,8),
    Tile(1,7,4),
    Tile(9,7,8),
    Tile(1,6,3),
    Tile(1,2,3),
    Tile(9,2,4),
    Tile(9,6,3),
    Tile(5,6,3),
    Tile(1,7,8),
    Tile(1,2,4),
    Tile(5,2,4),
    Tile(1,6,8),
    Tile(9,2,3),
    Tile(5,6,4),
    Tile(1,2,8),
    Tile(5,2,8),
    Tile(5,2,3),
]

tile_set_4 = [
    Tile(9,6,8),
    Tile(5,6,3),
    Tile(9,7,4),
    Tile(1,7,3),
    Tile(5,7,4),
    Tile(9,7,3),
    Tile(5,2,8),
    Tile(5,7,3),
    Tile(5,2,4),
    Tile(9,2,3),
    Tile(9,2,4),
    Tile(1,6,8),
    Tile(1,6,3),
    Tile(5,2,3),
    Tile(9,6,4),
    Tile(9,6,3),
    Tile(1,2,3),
    Tile(1,2,4),
    Tile(9,2,8),
    Tile(5,7,8),
    Tile(1,2,8),
    Tile(1,6,4),
    Tile(1,7,4),
    Tile(5,6,8),
    Tile(1,7,8),
    Tile(9,7,8),
    Tile(5,6,4),
]

def get_game_score(tile_set: list[Tile] = None, timeout:float = 1) -> int:
    board = Board()
    if tile_set:
        tiles = deepcopy(tile_set)
    else:
        t = Tiles()
        tiles = []
        while any(t._left_tiles):
            tiles.append(t.pick_tile())
    
    while any(board.open_positions()):
        tile = tiles.pop()
        position = AI.get_best_position_tree(board, tile, timeout)
        board.place_tile(tile, position)
        # board.draw()
    
    return board.score()

scores = {}

def run_test(description, tile_set, timeout, retries=10):
    key = f'{description} ({timeout}s)'
    print(key + ' ', end='', flush=True)
    scores[key] = []
    for _ in range(retries):
        scores[key].append(get_game_score(tile_set, timeout=timeout))
        print('.', end='', flush=True)
    print('')

def print_results():
    print('')
    print('*** Results ***')
    for key, values in scores.items():
        print(f'{key:25}: {mean(values)} {values}')




try:
    run_test('random tiles', None, 0.1, 10)
    run_test('random tiles', None, 1, 5)
    run_test('tile set 1', tile_set_1, 0.1, 10)
    run_test('tile set 1', tile_set_1, 1, 5)
    run_test('tile set 1', tile_set_1, 3, 2)
    run_test('tile set 2', tile_set_2, 0.1, 10)
    run_test('tile set 2', tile_set_2, 1, 5)
    run_test('tile set 3', tile_set_3, 0.1, 10)
    run_test('tile set 4', tile_set_4, 0.1, 10)
except:
    pass
print_results()