from game import Game

if __name__ == '__main__':

    game = Game()
    game.start()
    while not game.finished():
        print(f'The current tile is: {game.get_tile()}')
        position = input('position for current Tile (e.g. C3): ')
        try:
            game.place_tile(position)
        except:
            print(f'Could not place the tile on {position}. Try again.')
    
        
