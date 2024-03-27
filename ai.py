
from tiles import Tile, Tiles
from board import Board
import random

class AI:
    
    def run(self, board: Board, tile: Tile) -> str:
        column = random.choice(board.all_columns())
        row = random.choice(board.all_rows(column))
        position = f'{column}{row}'
        if position in board.tiles().keys():
            return self.run(board, tile)
        else:
            return position
    

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
    