from miniMax.optimizers import *


# prioritize moves that are adjacent to a the last few moves
class AdjMoves(MoveSelector):
    # memory is the number of moves made to remember
    def __init__(self, game, memory=1):
        super(AdjMoves, self).__init__(game)
        if memory <= 0:
            memory = 1
        self.memory = memory
        self.storage = list()

    def next(self, move=None, score=None, optimizing=False):
        # make next adjMoves instance
        output = AdjMoves(self.game, memory=self.memory)

        # restore all moves that are still within the memory range
        if self.full():
            start = 1
        else:
            start = 0
        for old in range(start, len(self.storage)):
            output.storage.append(self.storage[old])

        # append the new moves
        if move in self.game:
            adj = self.game.adj(move)
            adj.append(move)
            output.storage.append(adj)

        output.__movesToSuper()

        # if there are no adjacent moves, add all available moves
        output.__addAll()

        return output

    # update super with all stored moves
    def __movesToSuper(self):
        for step in self.storage:
            for move in step:
                super(AdjMoves, self).update(move)

    # add all available moves (use if there are no adjacent moves)
    def __addAll(self):
        if len(self.storage) == 0:
            print("adding all")
            for move in self.game.allMoves():
                super().update(move)

    # returns true if storage is holding up to the specified memory amoung
    def full(self):
        return len(self.moves) - 1 >= self.memory
