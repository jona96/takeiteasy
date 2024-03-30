
from tiles import Tile
from board import Board, BoardPosition, all_items_equal
from statistics import mean
from functools import lru_cache as cache
from time import time
import random


class ScoreNode:
    def __init__(self, board:Board = None, parent = None):
        self._board = board
        self.parent = parent
        self.own_score = None
    
    def __str__(self, level=0):
        ret = '  ' * level + repr(self) + '\n'
        sorted = True if isinstance(self, ScoreNodeNewRandomTile) else False
        for child in self.sorted_children if sorted else self.children:
            if child.hasScore():
                ret += child.__str__(level+1)
        return ret

    @property
    def children(self):
        if not hasattr(self, '_children'):
            self._children:list[ScoreNode] = []
            self._expand_children()
        return self._children

    @property
    def sorted_children(self):
        return sorted(self.children, key=lambda child:child.score() or 0, reverse=True)

    def hasScore(self) -> bool:
        return self.score() is not None
    
class ScoreNodeNewRandomTile(ScoreNode):
    
    def __init__(self, new_tile:Tile, board: Board = None, parent = None):
        super().__init__(board, parent)
        self.new_tile = new_tile
        
    def __repr__(self):
        if self.score():
            return f'{self.new_tile}: {round(self.score(), 1)}'
        else:
            '----'
    
    def _expand_children(self):
        if any(self.children): return
        for position in self.board.open_positions():
            new_child = ScoreNodeWhereToPut(position, parent=self)
            self.children.append(new_child)
            
    @property
    def board(self):
        return self.parent.board if self.parent else self._board
        
    def score(self) -> float:
        children_scores = [child.score() for child in self.children if child.score()]
        if any(children_scores):
            return max(children_scores)
        else:
            return None
    
    def best_position(self, tile:Tile = None) -> BoardPosition | None:
        try:
            best_child = self.sorted_children[0]
        except ValueError:
            return None
        return best_child.board.position_of_tile(tile)
        
    def calc_score_of_children(self, eval_function, end_time:float = None):
        for child in self.children:
            if end_time and time() > end_time: 
                return
            if not child.hasScore():
                child.own_score = eval_function(child.board)

class ScoreNodeWhereToPut(ScoreNode):
        
    def __init__(self, position, board: Board = None, parent = None):
        super().__init__(board, parent)
        self.tile_position = position
        
    def __repr__(self):
        if self.own_score is not None:
            repr = f'{self.tile_position}: {(round(self.own_score, 1))}'
            if any(self.children):
                repr += f' ({round(self.score(), 1)})'
        else:
            repr = '----'
        return repr
    
    def _expand_children(self):
        if any(self.children): return
        for tile in self.board.remaining_tiles():
            new_child = ScoreNodeNewRandomTile(tile, parent=self)
            self.children.append(new_child)
    
    @property
    def board(self):
        if self.parent and self.parent.board:
            board_copy:Board = self.parent.board.__copy__()
            board_copy.place_tile(self.parent.new_tile, self.tile_position)
            return board_copy
        else:
            return self._board
        
    def score(self) -> float:
        if not self.own_score:
            return None
        children_scores = [child.score() for child in self.children if child.score()]
        if not any(children_scores):
            return self.own_score
        else:
            return mean(children_scores)
    

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
    
    @cache
    @staticmethod
    def get_best_position(board: Board, tile: Tile, timeout:int = 1) -> BoardPosition:
        end_time = time() + timeout
        
        # strategy:
        # - calc every position where to put the tile
        # - for the best x positions get every possible next tile
        # - calc every position where to put the next tile
        # - ...
                
        base_board = ScoreNodeNewRandomTile(tile, board)
        base_board.calc_score_of_children(AI.estimated_score, end_time)
        print(base_board)
        
        for position in base_board.sorted_children[:3]:
            for new_tile in position.children:
                new_tile.calc_score_of_children(AI.estimated_score)
                if time() > end_time: break
            print(base_board)
            if time() > end_time: break
        
        
        
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
    