from gameSrc.connect4Game import *
from miniMax.miniMax import *
from miniMax.depthController.maxSteps import *
from miniMax.moveSelector.adjMoves import *


def getNumeric(prompt):
    res = input(prompt)
    if res.isnumeric():
        return int(res)
    return None


def getMove(game, player):
    move = getNumeric(str(player) + " move: ")
    while not game.validMove(move):
        print("Invalid Move.")
        move = getNumeric(str(player) + " move: ")
    return move


moves = (1, 4, 4, 6, 2, 3, 2)


def main():
    game = Connect4Game(width=7, height=6, inARow=4)
    player = Player.P1

    dc = MaxSteps(maxSteps=4)
    ms = AllMoves(game=game)

    while game:
        if player == Player.P1:
            move = getMove(game, player)
        elif player == Player.P2:
            move = MiniMax.bestMove(game, player, dc, moveSelector=ms, debug=False)
            print("CPU made move: " + str(move))

        print(game)
        print()
        player = player.next()

        ms = ms.next(move=move)
        dc = dc.next(move=move)


main()
