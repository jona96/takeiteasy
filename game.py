from board import Board, BoardPosition
from tiles import Tile, Tiles

class GameNotRunningException(Exception): pass
class GameCannotPlaceTileException(Exception): pass

class Game:
    
    def __init__(self, board:Board = None) -> None:
        if board:
            self.board = board
            self.tiles = Tiles(list(board.tiles().values()))
        else:
            self.board = Board()
            self.tiles = Tiles()
        self.started = False
        self._finished = False
        self.current_tile = None

    def start(self):
        self.started = True
        self.current_tile = self.tiles.pick_tile()
        self.board.draw()

    def get_tile(self) -> Tile:
        if not self.started:
            raise GameNotRunningException()
        return self.current_tile
    
    def place_tile(self, position: BoardPosition):
        if self.finished(): return
        try:
            self.board.place_tile(self.current_tile, position)
            self.board.draw()
        except Exception as e: raise GameCannotPlaceTileException(e)
        
        self.current_tile = self.tiles.pick_tile()
        
        if len(self.board.tiles()) == 19:
            self._finished = True
    
    def finished(self) -> bool:
        return self._finished


if __name__ == '__main__':
    
    board = Board()
    game = Game(board)
    game.start()
    
    while not game.finished():
        print(f'The current tile is: {game.get_tile()}')
        position = input('position for current Tile (e.g. C3): ')
        try:
            game.place_tile(BoardPosition.from_string(position))
        except:
            print(f'Could not place the tile on {position}. Try again.')
        