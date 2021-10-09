from gameSrc.game import *
from miniMax.depthController.maxSteps import *
from miniMax.moveSelector.allMoves import *
import random


# class with all static variables that runs recursive minimax optimization on a game
# https://github.com/Cledersonbc/tic-tac-toe-minimax
class MiniMax:
    # get the best move in the current game state using the specified search optimizers
    @staticmethod
    def bestMove(game: Game, player: Player, depthController=None, moveSelector=None, debug=False):
        # invalid player, break
        if not player:
            return None
        # if the given depthController is invalid, default to maxSteps
        if depthController is None or not issubclass(type(depthController), DepthController):
            depthController = MaxSteps(game.maxScore())
        # if the given moveSelector is invalid default to AllMoves
        if moveSelector is None or not issubclass(type(moveSelector), MoveSelector):
            moveSelector = AllMoves(game)
        # run recursive functions and get the best move (index 0)
        return MiniMax.__helper(game, player, depthController, moveSelector, debug)[0]

    @staticmethod
    def __helper(game, player, dc, ms, debug):
        # print board if debugging
        if debug:
            print(game)
            print()

        # base case: game is over or no more searches should be made
        if not game or not dc or len(ms) == 0:
            # return the score for the current game state
            return None, game.scoreState()

        # create bestScore and make it initialize it to the worst score, so it will be replaced after a comparisons
        bestScore = StateScore()
        bestScore[player] = -game.maxScore()
        bestScore[player.next()] = game.maxScore()
        bestMoves = list()

        for move in ms:
            # store the first move (just in case there is only 1 move to check)
            if len(bestMoves) == 0:
                bestMoves.append(move)

            # make the move and score it
            score = game.move(move, player, undoable=True)
            if score is not None:
                # if the move was valid and did not result in a win
                if score < game.maxScore():
                    # get recursive score and increment player and optimizers
                    recScore = MiniMax.__helper(
                        game,
                        player.next(),
                        dc.next(move=move, score=score, optimizing=True),
                        ms.next(move=move, score=score, optimizing=True),
                        debug
                    )[1]
                    # undo the move
                    game.undoMove(move)

                    # add to the most optimal moves list
                    if bestScore == recScore:
                        bestMoves.append(move)

                    # store the most optimal move in bestMove and its score in bestScore
                    elif recScore == StateScore.mostOptimal(player, recScore, bestScore, game.maxScore()):
                        bestMoves.clear()
                        bestMoves.append(move)
                        bestScore = recScore

                # if the move was valid and resulted in a win, return it (it is most optimal)
                else:
                    game.undoMove(move)
                    bestScore[player] = game.maxScore()
                    bestScore[player.next()] = 0
                    return move, bestScore

        # choose a move from the most optimal move list
        return random.choice(bestMoves), bestScore
