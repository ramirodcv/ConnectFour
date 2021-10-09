from gameSrc.connect4Game import *
from gameSrc.player import *
from miniMax.depthController.maxSteps import *
from miniMax.moveSelector.adjMoves import *
from miniMax.miniMax import *


def main():
    moves = (0, 1, 1)
    player = Player.P1

    game = Connect4Game(width=4, height=4, inARow=3)

    dc = MaxSteps(8)
    ms = AdjMoves(game, memory=6)

    for move in moves:
        score = game.move(move, player)
        ms = ms.next(move, score)
        dc = dc.next(move, score)
        player = player.next()

    move = MiniMax.bestMove(game, Player.P2, depthController=dc, moveSelector=ms, debug=False)
    print(move)


main()