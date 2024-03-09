import random

class Tiles:

    _all_tiles = [
        (1, 2, 3), (1, 2, 4), (1, 2, 8),
        (1, 6, 3), (1, 6, 4), (1, 6, 8),
        (1, 7, 3), (1, 7, 4), (1, 7, 8),
        (5, 2, 3), (5, 2, 4), (5, 2, 8),
        (5, 6, 3), (5, 6, 4), (5, 6, 8),
        (5, 7, 3), (5, 7, 4), (5, 7, 8),
        (9, 2, 3), (9, 2, 4), (9, 2, 8),
        (9, 6, 3), (9, 6, 4), (9, 6, 8),
        (9, 7, 3), (9, 7, 4), (9, 7, 8),
    ]

    def __init__(self):
        self.left_tiles = Tiles._all_tiles

    def pick_tile(self):
        if not any(self.left_tiles):
            return None
        index_of_tile = int(random.random() * len(self.left_tiles))
        return self.left_tiles.pop(index_of_tile)


if __name__ == '__main__':
    game = Tiles()

    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())
    print(game.pick_tile())