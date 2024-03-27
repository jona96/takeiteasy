from game import Game
from board import BoardPosition

if __name__ == '__main__':

    game = Game()
    game.start()
    while not game.finished():
        print(f'The current tile is: {game.get_tile()}')
        position = input('position for current Tile (e.g. C3): ')
        board_position = BoardPosition.from_string(position)
        try:
            game.place_tile(board_position)
        except:
            print(f'Could not place the tile on {position}. Try again.')
    
        
