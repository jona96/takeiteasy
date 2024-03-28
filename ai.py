
from tiles import Tile, Tiles
from board import Board, BoardPosition
from copy import deepcopy
from statistics import mean
from functools import lru_cache as cache
import random

class AI:
    
    @cache
    @staticmethod
    def estimated_score(board: Board, depth:int = 2) -> float:
        if depth == 0:
            return board.max_score()
        elif not any(board.open_positions()):
            return board.score()
        else:
            # try every left tile
            tile_scores = []
            for tile in board.left_tiles():
                score_positions = []
                for position in board.open_positions():
                    board_copy = deepcopy(board)
                    board_copy.place_tile(tile, position)
                    score_positions.append({'position' : position, 'score' : board_copy.max_score()})
                score_positions.sort(key=lambda x:x['score'], reverse=True)
                positions_with_best_max_scores = [score_pos['position'] for score_pos in score_positions][:3]
                # print(f'positions_with_best_max_scores={positions_with_best_max_scores}')
                
                score_positions = []
                for position in positions_with_best_max_scores:
                    board_copy = deepcopy(board)
                    board_copy.place_tile(tile, position)
                    score_positions.append({'position' : position, 'score' : AI.estimated_score(board_copy, depth - 1)})
                score_positions.sort(key=lambda x:x['score'], reverse=True)
                tile_scores.append(score_positions[0]['score'])
            return mean(tile_scores)

    @staticmethod
    def get_best_position(board: Board, tile: Tile) -> BoardPosition:
        score_positions = []
        for position in board.open_positions():
            board_copy = deepcopy(board)
            board_copy.place_tile(tile, position)
            score_positions.append({'position' : position, 'score' : AI.estimated_score(board_copy, 2)})
        # print(score_positions)
        score_positions.sort(key=lambda x:x['score'], reverse=True)
        best_position = score_positions[0]['position']
        return best_position

if __name__ == '__main__':
    from game import Game
    from time import sleep
    
    game = Game()
    game.start()
    
    for _ in range(19):
        position = AI.get_best_position(game.board, game.get_tile())
        print(f'place Tile {game.get_tile()} at {position}')
        game.place_tile(position)
        sleep(0.3)
    