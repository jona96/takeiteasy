from board import Board, BoardPosition
from tiles import Tile, Tiles

class GameNotRunningException(Exception): pass
class GameCannotPlaceTileException(Exception): pass

class Game:
    
    def __init__(self) -> None:
        self.tiles = Tiles()
        self.board = Board()
        self.started = False
        self._finished = False
        self.current_tile = None

    def start(self):
        self.started = True
        self.current_tile = self.tiles.pick_tile()
        print(self.board.draw())

    def get_tile(self) -> Tile:
        if not self.started:
            raise GameNotRunningException()
        return self.current_tile
    
    def place_tile(self, position: BoardPosition):
        if self.finished(): return
        try:
            self.board.place_tile(self.current_tile, position)
        except Exception as e: raise GameCannotPlaceTileException(e)
        
        self.current_tile = self.tiles.pick_tile()
        
        if len(self.board.tiles()) == 19:
            self._finished = True
    
    def finished(self) -> bool:
        return self._finished
