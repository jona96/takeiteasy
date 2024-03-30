
from copy import copy
from tiles import Tile
from board import Board, BoardPosition, all_items_equal
from statistics import mean
from functools import lru_cache as cache
from time import time
import random
import cProfile as profile

class ContinueException(Exception): pass
class BreakException(Exception): pass

class ScoreNode:
    def __init__(self, board:Board = None, parent = None):
        self._board = board
        self.parent = parent
        self._score = None
    
    def __str__(self, level=0):
        ret = '  ' * level + repr(self) + '\n'
        sorted = True if isinstance(self, ScoreNodeNewRandomTile) else False
        for child in self.sorted_children() if sorted else self.children:
            if child.hasScore():
                ret += child.__str__(level+1)
        return ret

    @property
    def children(self):
        if not hasattr(self, '_children'):
            self._children:set[ScoreNode] = set()
            self._expand_children()
        return self._children

    def sorted_children(self):
        return sorted(list(self.children), key=lambda child:child.score(default=0), reverse=True)

    def hasScore(self) -> bool:
        return self.score() is not None
    
    def score(self, default=None) -> float:
        return self._score or default
    
    def set_score(self, score: float):
        self._score = score
        if self.parent:
            self.parent.update_score()
    
class ScoreNodeNewRandomTile(ScoreNode):
    
    def __init__(self, new_tile:Tile, board: Board = None, parent = None):
        super().__init__(board, parent)
        self.new_tile = new_tile
        
    def __repr__(self):
        return f'{self.new_tile}: {round(self.score(), 1) if self.hasScore() else "----"}'
    
    def _expand_children(self):
        if any(self.children): return
        for position in self.board.open_positions():
            new_child = ScoreNodeWhereToPut(position, parent=self)
            self.children.add(new_child)
            
    @property
    def board(self):
        return self.parent.board if self.parent else self._board
        
    def update_score(self):
        # children_scores = {child.score() for child in self.children if child.hasScore()}
        # self.set_score(max(children_scores))
        
        try:
            self.set_score(max([child.score() for child in self.children]))
        except TypeError:   # not every child has a score
            pass
        
    def best_position(self, tile:Tile = None) -> BoardPosition | None:
        try:
            best_child = self.sorted_children()[0]
        except ValueError:
            return None
        return best_child.board.position_of_tile(tile)
        
    def number_of_parents(self) -> int:
        if not self.parent or not self.parent.parent: return 0
        else: return self.parent.parent.number_of_parents() + 1
    
    def calc_one_child(self, eval_function) -> bool:
        children_without_score = {child for child in self.children if not child.hasScore()}
        if any(children_without_score):
            selected_child = children_without_score.pop()
            # print(f'{"_" * self.number_of_parents()}calc {self.new_tile} at {selected_child.tile_position}')
            selected_child.set_score(eval_function(selected_child.board))
            return True
        else:
            return False
            

class ScoreNodeWhereToPut(ScoreNode):
        
    def __init__(self, position, board: Board = None, parent = None):
        super().__init__(board, parent)
        self.tile_position = position
        
    def __repr__(self):
        return f'{self.tile_position}: {round(self.score(), 1) if self.hasScore() else "----"}'
    
    def _expand_children(self):
        if any(self.children): return
        for tile in self.board.remaining_tiles():
            new_child = ScoreNodeNewRandomTile(tile, parent=self)
            self.children.add(new_child)
    
    @property
    def board(self):
        if self.parent and self.parent.board:
            board_copy:Board = copy(self.parent.board)
            board_copy.place_tile(self.parent.new_tile, self.tile_position)
            return board_copy
        else:
            return self._board
        
    def update_score(self):
        try:
            self.set_score(mean([child.score() for child in self.children]))
        except TypeError:   # not every child has a score
            pass
        

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
        
        new_tile_board = base_board
        while time() < end_time:
            
            # print(base_board)
            
            if calc_one(base_board, 1, AI.estimated_score): pass
            elif calc_one(base_board, 2, AI.estimated_score): pass
            elif calc_one(base_board, 3, AI.estimated_score): pass
            else: break
            
        # print(base_board)
        
        return base_board.best_position(tile)
        
def calc_one(board: ScoreNodeNewRandomTile, level: int, function) -> bool:
    if level == 0:
        return False
    elif level == 1:
        if board.calc_one_child(function): return True
        return False
    elif level >= 2:
        for position in board.sorted_children()[:3]:
            for new_tile_board in position.children:
                if calc_one(new_tile_board, level - 1, function): return True
        return False


if __name__ == '__main__':
    from game import Game
    from time import sleep
    
    game = Game()
    game.start()
    
    for _ in range(19):
        # position = AI.get_best_position(game.board, game.get_tile())
        profile.run('position = AI.get_best_position(game.board, game.get_tile())', sort='tottime')
        print(f'place Tile {game.get_tile()} at {position}')
        game.place_tile(position)
    