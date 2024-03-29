
from tiles import Tile, Tiles
from board import Board, BoardPosition, all_items_equal
from copy import deepcopy
from statistics import mean
from functools import lru_cache as cache
from time import time
import random


class ScoreTree:
    def __init__(self, position:Board, score:float = None):
        self.children:list[ScoreTree] = []
        self.board = position
        self.own_score = score
    
    def __str__(self, level=0):
        ret = '  ' * level + repr(self) + '\n'
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        if self.own_score is not None:
            return str(round(self.own_score, 1))
        else:
            return '----'
    
    def hasScore(self) -> bool:
        return self.score() is not None
    
    def score(self) -> float:
        if not any(self.children):
            return self.own_score
        else:
            children_scores = [child.score() or 0 for child in self.children]
            return mean(children_scores)
        
    def best_child(self, tile:Tile = None):
        matching_children = [child for child in self.children if tile is None or tile in child.board.tiles().values()]
        if not any(matching_children):
            return None
        return max(matching_children, key=lambda child:child.score() or 0)
        
    def best_position(self, tile:Tile = None) -> BoardPosition | None:
        return self.best_child().board.position_of_tile(tile)
        
    def expand_children(self, new_tile:Tile):
        if any(self.children): return
        for position in self.board.open_positions():
            new_board = deepcopy(self.board)
            new_board.place_tile(new_tile, position)
            new_child = ScoreTree(new_board)
            self.children.append(new_child)
    
    def calc_score_of_children(self, eval_function):
        for child in self.children:
            if not child.hasScore():
                child.own_score = eval_function(child.board)
        

class AI:
    
    @cache
    @staticmethod
    def estimated_score(board: Board) -> float:
        if board.open_positions() == 0:
            return board.score()
        
        """estimate propability of completion for a started score group
        by looking at the remaining tiles with the matching numbers"""
        
        score = 0
        for nx in ['n1', 'n2', 'n3']:
            for group in Board.SCORE_GROUPS[nx]:
                number_list = []
                for board_position in group:
                    if board_position in board.tiles().keys():
                        tile = board.tiles()[board_position]
                        number = getattr(tile, nx)
                        number_list.append(number)
                if not any(number_list):
                    # no tile set, assume average value of 5 with average propability of 50%
                    score += 5 * len(group) * 0.2
                elif all_items_equal(number_list):
                    # so far all number the same
                    number = number_list[0]
                    missing_tiles = len(group) - len(number_list)
                    remaining_tiles_with_number = [tile for tile in board.remaining_tiles() if getattr(tile, nx) == number]
                    propability_factor = (len(remaining_tiles_with_number) / len(board.remaining_tiles())) ** missing_tiles
                    score += number * len(group) * propability_factor
                else:
                    # different tiles -> no way to safe the row
                    score += 0

        return score
        return board.max_score() # TODO: better implementation
        return random.random() * 307 # TODO: implement
    
    @cache
    @staticmethod
    def get_best_position(board: Board, tile: Tile, depth: int = 2, width: int = 3) -> BoardPosition:
        return AI.get_best_position_tree(board, tile)
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
                for next_tile in simul_board.remaining_tiles():
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
    
    @cache
    @staticmethod
    def get_best_position_tree(board: Board, tile: Tile, timeout:int = 0.1) -> BoardPosition:
        end_time = time() + timeout
        base_board = ScoreTree(board)
        base_board.expand_children(tile)
        base_board.calc_score_of_children(AI.estimated_score)
        print(base_board)
        
        while not time() > end_time:
            # find deepest best child
            best_scoring_child = base_board.best_child()
            while any(best_scoring_child.children):
                best_scoring_child = best_scoring_child.best_child()
            
            # calc scores for that
            for new_tile in best_scoring_child.board.remaining_tiles():
                best_scoring_child.expand_children(new_tile)
                best_scoring_child.calc_score_of_children(AI.estimated_score)
            
            print(base_board)
            
        return base_board.best_position(tile)
        
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
    