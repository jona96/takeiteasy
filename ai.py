
from tiles import Tile, Tiles
from board import Board, BoardPosition
from copy import deepcopy
from statistics import mean
from functools import lru_cache as cache
import random

class AI:
    
    @cache
    @staticmethod
    def estimated_score(board: Board) -> float:
        if board.open_positions() == 0:
            return board.score()
        return board.max_score() # TODO: better implementation
        return random.random() * 307 # TODO: implement
    
    @staticmethod
    def get_best_position(board: Board, tile: Tile, depth: int = 2, width: int = 3) -> BoardPosition:
        scores = []
        # depth 1
        for position in board.open_positions():
            simul_board = deepcopy(board)
            simul_board.place_tile(tile, position)
            scores += [{'pos':position, 'score': AI.estimated_score(simul_board)}]
        scores.sort(key=lambda x:x['score'], reverse=True) # sort with high scores first
        scores = scores[:width]  # keep only most promising results for further analysis
        
        # depth 2
        if depth > 0 and len(board.open_positions()) > 1:
            for score in scores:
                simul_board = deepcopy(board)
                simul_board.place_tile(tile, score['pos'])
                scores_for_possible_next_tiles = []
                for next_tile in simul_board.left_tiles():
                    best_pos_for_next_tile = AI.get_best_position(simul_board, next_tile, depth-1)
                    next_simul_board = deepcopy(simul_board)
                    next_simul_board.place_tile(next_tile, best_pos_for_next_tile)
                    scores_for_possible_next_tiles += [{'tile':next_tile, 'score':AI.estimated_score(next_simul_board)}]
                new_score = mean([score['score'] for score in scores_for_possible_next_tiles])
                scores = [s for s in scores if s['pos'] != score['pos']] # delete old evaluation
                scores += [{'pos':score['pos'], 'score':new_score}] # add new evaluation
            scores.sort(key=lambda x:x['score'], reverse=True) # sort with high scores first
        
        highest_score = max(scores, key=lambda x:x['score'])
        return highest_score['pos']
    
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
    