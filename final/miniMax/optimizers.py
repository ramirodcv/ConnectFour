from gameSrc.game import Game


# next function parameters:
# move: that was made
# score: the score of the given move (may be useful for prioritization)
# optimizing: set to True if and only if MiniMax is using the next function

# Stores a set of moves to check during MiniMax optimization
class MoveSelector:
    def __init__(self, game: Game):
        self.game = game
        self.moves = set()

    # subclasses call this to add moves to the selector set
    def update(self, move):
        if self.game.validMove(move):
            self.moves.add(move)

    # increment this selector
    # subclasses implement this to prioritize new moves after a move was made
    def next(self, move=None, score=None, optimizing=False):
        pass

    # get an iterator containing moves to check
    def __iter__(self):
        return self.moves.__iter__()

    # get the number of moves in this selector to check
    def __len__(self):
        return len(self.moves)


# controls how many recursive calls are made during MiniMax optimization
class DepthController:
    # return true if and only if recursive calls should continue
    def __bool__(self):
        pass

    # subclasses implement this to update self after a move has been made
    def next(self, move=None, score=None, optimizing=False):
        pass
