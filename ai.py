
from tiles import Tile, Tiles
from board import Board, BoardPosition
import random

class AI:
    
    def _random_pick(self, board: Board, tile: Tile) -> BoardPosition:
        position = random.choice(board.ALL_POSITIONS)
        if position in board.tiles().keys():
            return self.run(board, tile)
        else:
            return position
        
    def run(self, board: Board, tile: Tile) -> BoardPosition:
        return self._random_pick(board, tile)

if __name__ == '__main__':
    from game import Game
    from time import sleep
    
    game = Game()
    game.start()
    
    ai = AI()
    
    for _ in range(19):
        position = ai.run(game.board, game.get_tile())
        print(f'place Tile {game.get_tile()} at {position}')
        game.place_tile(position)
        sleep(1)
    