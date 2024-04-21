
from copy import copy
import sys
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
        # TODO: list -> sets
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
                    # calculate propability for each possible number with remaining tiles
                    calibration_factor = 0.9 # for effects like when a tile is needed in multiple places
                    for number in range(1, 10):
                        remaining_tiles_with_number = [tile for tile in board.remaining_tiles() if getattr(tile, nx) == number]
                        propability = 1.0
                        for i in range(len(group)):
                            if i > len(remaining_tiles_with_number):
                                # not enough tiles with number to complete full group
                                propability = 0
                                continue
                            assert i < len(board.remaining_tiles()), f'should be catched by above check i={i} remaining_tiles={len(board.remaining_tiles())}'
                            propability *= (len(remaining_tiles_with_number) - i) / (len(board.remaining_tiles()) - i) # tiles with num / all tiles
                        score += number * len(group) * propability * calibration_factor
                elif all_items_equal(number_list):
                    # so far all number the same
                    calibration_factor = 0.9 # for effects like when a tile is needed in multiple places
                    number = number_list[0]
                    missing_tiles = len(group) - len(number_list)
                    remaining_tiles_with_number = [tile for tile in board.remaining_tiles() if getattr(tile, nx) == number]
                    propability = 1.0
                    for i in range(missing_tiles):
                        propability *= (len(remaining_tiles_with_number) - i) / (len(board.remaining_tiles()) - i) # tiles with num / all tiles
                    score += number * len(group) * propability * calibration_factor
                else:
                    # different tiles -> no way to safe the row
                    score += 0

        return score
    
    @staticmethod
    def calc_one(board: ScoreNodeNewRandomTile, level: int, function) -> bool:
        if level == 0:
            return False # no need to calc root
        elif level == 1:
            return board.calc_one_child(function)
        elif level >= 2:
            if not any(board.children): raise BreakException() # finished
            best_children = board.sorted_children()
            max_score = best_children[0].score()
            best_children = [child for child in best_children if child.score() > (max_score * 0.9)]
            if len(best_children) == 1 and len(board.board.open_positions()) > 7: raise BreakException() # result is pretty clear already
            random.shuffle(best_children)
            for position in best_children:
                for new_tile_board in position.children:
                    if AI.calc_one(new_tile_board, level - 1, function): return True
            return False

    @cache
    @staticmethod
    def get_best_position(board: Board, tile: Tile, timeout:int = 1, debug=False) -> BoardPosition:
        
        end_time = time() + timeout
        base_board = ScoreNodeNewRandomTile(tile, board)
        while time() < end_time:
            # if debug: print(base_board)
            try:
                level = 1
                while not AI.calc_one(base_board, level, AI.estimated_score):
                    level += 1
            except BreakException:
                break
            except KeyboardInterrupt:
                break
            
            if debug:
                sys.stdout.write('\r' + '  '.join([f'{child.board.position_of_tile(base_board.new_tile)} ({round(child.score(0), 2)})' for child in base_board.sorted_children()[:5]]))
                sys.stdout.flush()
            
        if debug: 
            print('')
            print('')
            print(base_board)
        return base_board.best_position(tile)
        

if __name__ == '__main__':
    from game import Game
    from time import sleep
    
    game = Game()
    game.start()
    
    for _ in range(19):
        position = AI.get_best_position(game.board, game.get_tile(), debug=True, timeout=5)
        # profile.run('position = AI.get_best_position(game.board, game.get_tile())', sort='tottime')
        print(f'place Tile {game.get_tile()} at {position}')
        game.place_tile(position)
    