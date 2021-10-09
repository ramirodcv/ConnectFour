from gameSrc.connect4Game import *
from miniMax.moveSelector.adjMoves import *


def main():
    game = Connect4Game()
    ms = AdjMoves(game, memory=3)

    ms = ms.next(move=3)
    ms = ms.next(move=0)
    ms = ms.next(move=6)

    print(ms)


main()