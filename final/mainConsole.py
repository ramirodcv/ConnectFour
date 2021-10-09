from gameSrc.connect4Game import *
from miniMax.moveSelector.adjMoves import *
from miniMax.miniMax import *

MAX_STEPS = 4
MEMORY = 4


# get input with the given type meeting the given condition
def getInput(prompt, condition=lambda: True, returnType=None):
    valid = False   # true once output meets condition
    while not valid:
        try:
            # get input
            res = input(prompt + ": ").strip().lower()
            # cast input
            if returnType:
                res = returnType(res)

            # check condition
            if not condition(res):
                print("invalid input.")
            else:
                valid = True
        except:
            pass
    return res


# get how many players are playing
def getPlayerCount():
    print("Enter how many players are participating")
    res = int(getInput(
        "How many players are there (1 or 2)",
        condition=lambda x: 1 <= x <= 2,
        returnType=int
    ))
    print()
    return res


# get board characteristics
def getBoardCharacteristics():
    print("Select board characteristics.")
    temp = Connect4Game.getWidthRange()
    width = int(getInput(
        "board width (" + str(temp.least) + "-" + str(temp.most) + ")",
        condition=lambda x: temp.least <= x <= temp.most,
        returnType=int
    ))
    temp = Connect4Game.getHeightRange()
    height = int(getInput(
        "board height (" + str(temp.least) + "-" + str(temp.most) + ")",
        condition=lambda x: temp.least <= x <= temp.most,
        returnType=int
    ))
    temp = Connect4Game.getRowLengthRange()
    rowLength = int(getInput(
        "winning row length (" + str(temp.least) + "-" + str(temp.most) + ")",
        condition=lambda x: temp.least <= x <= temp.most,
        returnType=int
    ))
    print()
    return width, height, rowLength


# display game results
def displayResults(game):
    if not game.winner():
        print("No one won. Stalemate.")
    else:
        print("Congrats " + str(game.winner()) + ", you won!!!")
    print()


def main():
    # while playing connect 4
    playing = True
    while playing:
        # get options
        useCpu = getPlayerCount() == 1
        width, height, rowLength = getBoardCharacteristics()

        # make game
        game = Connect4Game(width=width, height=height, inARow=rowLength)
        player = Player.P1

        # handle cpu variables
        dc = None
        ms = None
        if useCpu:
            dc = MaxSteps(maxSteps=MAX_STEPS)
            ms = AdjMoves(game=game, memory=MEMORY)

        # play the game
        while game:
            # get cpu move if its the CPU's turn
            if player == Player.P2 and useCpu:
                move = MiniMax.bestMove(game, player, depthController=dc, moveSelector=ms)
                print(str(player) + " move: " + str(move))
            # get user's move
            else:
                move = int(getInput(
                    str(player) + " move (0-" + str(game.dim().x - 1) + ")",
                    condition=lambda x: 0 <= x < game.dim().x,
                    returnType=int
                ))

            # make the move and display the new board
            score = game.move(move, player)
            print(game)
            print()

            # increment player and optimizers
            player = player.next()
            if useCpu:
                dc = dc.next(move=move, score=score)
                ms = ms.next(move=move, score=score)

        # handle game end
        displayResults(game)
        playing = getInput("Would you like to continue player? (y/n)", condition=lambda x: x == "y" or x == "n") == "y"
        print()

    print("Thanks for playing.")


main()
