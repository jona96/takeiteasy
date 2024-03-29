
from tiles import Tile, Tiles
from board import Board, BoardPosition, all_items_equal
from copy import deepcopy
from statistics import mean
from functools import lru_cache as cache
from time import time
import random


class ScoreNode:
    def __init__(self, position:Board, score:float = None):
        self.board = position
        self.own_score = score
    
    def __str__(self, level=0):
        ret = '  ' * level + repr(self) + '\n'
        for child in self.children:
            if child.hasScore():
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        if self.own_score is not None:
            repr = str(round(self.own_score, 1))
            if any(self.children):
                repr += f' ({round(self.score(), 1)})'
        else:
            repr = '----'
        return repr
    
    @property
    def children(self):
        if not hasattr(self, '_children'):
            self._children:list[ScoreNode] = []
            self._expand_children()
        return self._children

    def hasScore(self) -> bool:
        return self.score() is not None
    
    def hasScoreForFullDepth(self) -> bool:
        if len(self.children) == 1: # last child == last tile is is placed
            return self.children[0].hasScore()
        else:
            for child in self.children:
                if not child.hasScoreForFullDepth():
                    return False
            return True
        
    def calc_score_of_children(self, eval_function):
        for child in self.children:
            if not child.hasScore():
                child.own_score = eval_function(child.board)
        
class ScoreNodeWhereToPut(ScoreNode):
    
    def __init__(self, position: Board, new_tile:Tile, score: float = None):
        super().__init__(position, score)
        self.new_tile = new_tile
        
    def score(self) -> float:
        if not self.own_score:
            return None
        children_scores = [child.score() for child in self.children if child.score()]
        if not any(children_scores):
            return self.own_score
        else:
            return max(children_scores)
        
    def _expand_children(self):
        if any(self.children): return
        for position in self.board.open_positions():
            new_board = deepcopy(self.board)
            new_board.place_tile(self.new_tile, position)
            new_child = ScoreNodeNewRandomTile(new_board)
            self.children.append(new_child)
    
    def best_child(self, tile:Tile = None):
        matching_children = [child for child in self.children if tile is None or tile in child.board.tiles().values()]
        if not any(matching_children):
            return None
        return max(matching_children, key=lambda child:child.score() or 0)
        
    def best_position(self, tile:Tile = None) -> BoardPosition | None:
        return self.best_child().board.position_of_tile(tile)
        
class ScoreNodeNewRandomTile(ScoreNode):
    
    def score(self) -> float:
        if not self.own_score:
            return None
        children_scores = [child.score() for child in self.children if child.score()]
        if not any(children_scores):
            return self.own_score
        else:
            return mean(children_scores)
        
    def _expand_children(self):
        if any(self.children): return
        for tile in self.board.remaining_tiles():
            new_board = deepcopy(self.board)
            new_child = ScoreNodeWhereToPut(new_board, tile)
            self.children.append(new_child)
    

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
    def get_best_position(board: Board, tile: Tile, timeout:int = 0.1) -> BoardPosition:
        end_time = time() + timeout
        base_board = ScoreNodeWhereToPut(board, tile)
        base_board.own_score = AI.estimated_score(base_board.board)
        base_board.calc_score_of_children(AI.estimated_score)
        print(base_board)
        
        # while not time() > end_time:
        #     # find deepest best child that has not been fully solved
            
        #     # matching_children = [child for child in self.children if tile is None or tile in child.board.tiles().values()]
        #     # if not any(matching_children):
        #     #     return None
        #     # return max(matching_children, key=lambda child:child.score() or 0)
            
        #     best_scoring_child = base_board.best_child()
        #     while any([child.score() for child in best_scoring_child.children]):
        #         best_scoring_child = best_scoring_child.best_child()
            
        #     # calc scores for that
        #     best_scoring_child.calc_score_of_children(AI.estimated_score)
            
        #     print(base_board)
            # sleep(1)
            
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
    