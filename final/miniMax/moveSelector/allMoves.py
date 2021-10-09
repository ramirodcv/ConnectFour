from miniMax.optimizers import *


# prioritize all valid moves in the given game
class AllMoves(MoveSelector):
    def __init__(self, game):
        super(AllMoves, self).__init__(game)
        for move in game.allMoves():
            super(AllMoves, self).update(move)

    def next(self, move=None, score=None, optimizing=False):
        return AllMoves(self.game)
