
from tiles import Tile, Tiles
from board import Board, BoardPosition
from copy import deepcopy
from statistics import mean
from functools import lru_cache as cache
import random

class AI:
    
    def _random_pick(self, board: Board, tile: Tile) -> BoardPosition:
        position = random.choice(board.ALL_POSITIONS)
        if position in board.tiles().keys():
            return self.get_best_position(board, tile)
        else:
            return position
    
    @cache
    @staticmethod
    def estimated_score(board: Board) -> float:
        if len(board.tiles()) == 19:
            return board.score()
        else:
            # try every left tile
            scores = []
            for tile in board.left_tiles():
                for position in board.open_positions():
                    board_copy = deepcopy(board)
                    board_copy.place_tile(tile, position)
                    scores.append(AI.estimated_score(board_copy))
            return mean(scores)

    def _try_everything(self, board: Board, tile: Tile) -> BoardPosition:
        score_positions = {} # estimated score : BoardPosition
        for position in board.open_positions():
            board_copy = deepcopy(board)
            board_copy.place_tile(tile, position)
            score_positions[AI.estimated_score(board_copy)] = position
        print(score_positions)
        max_score = max(score_positions.keys())
        best_position = score_positions[max_score]
        return best_position

    def get_best_position(self, board: Board, tile: Tile) -> BoardPosition:
        if len(board.open_positions()) <= 4:
            return self._try_everything(board, tile)
        else:
            return self._random_pick(board, tile)

if __name__ == '__main__':
    from game import Game
    from time import sleep
    
    game = Game()
    game.start()
    
    ai = AI()
    
    for _ in range(19):
        position = ai.get_best_position(game.board, game.get_tile())
        print(f'place Tile {game.get_tile()} at {position}')
        game.place_tile(position)
        sleep(0.3)
    