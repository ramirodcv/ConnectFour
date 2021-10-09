from gameSrc.player import *


# class to score a game state
# scores should be positive
# the highest score should equal game.maxScore()
# a more desired state should have a high score for the specified player
class StateScore:
    # returns the more optimal state of two states relative to the given player
    @staticmethod
    def mostOptimal(player: Player, score1, score2, maxScore):
        # invalid input return None
        if not player or type(score1) != StateScore or type(score2) != StateScore:
            return None

        # return score1 if Player.P1 won in score1 or lost in score2
        if score1[player] == maxScore or score2[player.next()] == maxScore:
            return score1

        # return score2 if Player.P1 won in score2 or lost in score1
        if score2[player] == maxScore or score1[player.next()] == maxScore:
            return score2

        # return the highest difference in scores
        if score1.dif(player) > score2.dif(player):
            return score1

        # return a random score (they are valued equally)
        return score2

    def __init__(self):
        self.p1Score = 0
        self.p2Score = 0

    # return true if and only if this score has equal values to another score
    def __eq__(self, other):
        if type(other) != StateScore:
            return False
        return (self.p1Score == other.p1Score) and (self.p2Score == other.p2Score)

    # get the score for the specified player
    def __getitem__(self, item: Player):
        if item == Player.EMPTY:
            return 0
        if item == Player.P1:
            return self.p1Score
        # item == Player.P2
        return self.p2Score

    # set the score for the specified player player
    def __setitem__(self, key, value):
        if key == Player.P1:
            self.p1Score = value
        if key == Player.P2:
            self.p2Score = value

    # return the difference is scores relative to a player
    # should be positive if the specified player is in a more optimal position
    def dif(self, player):
        if not player:
            return 0
        return self[player] - self[player.next()]

    def __str__(self):
        return "(p1Score=" + str(self.p1Score) + ", p2Score=" + str(self.p2Score) + ")"


class Game:
    ###############
    # define helper functions in the section they are used or the helper function section
    # make helpers private (unless overridden function)

    ###############
    # game characteristics

    # return the max score that can be returned from move
    def maxScore(self):
        pass

    def dim(self):
        pass

    ##############
    # game validity

    # returns true if a move can be made (board not full and no winner)
    def __bool__(self):
        return not self.full() and not self.winner()

    # return true if there are no more available moves (usually board not full)
    def full(self):
        pass

    # returns the winner of this game (Player.EMTPY for no winner)
    def winner(self):
        pass

    ############
    # move validity and move lists for optimizers

    # if the given item (move) is in this game
    def __contains__(self, item):
        pass

    # returns true if the given move can be made
    def validMove(self, move):
        pass

    # get all moves adjacent to the given move
    def adj(self, location):
        pass

    # return all possible moves
    def allMoves(self):
        pass

    ############
    # movement and scoring

    # returns None if no move was made
    # returns a score if the move was made (equal to maxScore if win occurred)
    def move(self, move, player, undoable=False):
        pass

    # undo a move
    # the move being reverted must be made with undoable=True for correct behavior
    def undoMove(self, move):
        pass

    # score the current game state
    def scoreState(self):
        pass

    def scoreMove(self, move, player, undoable):
        pass

    ############
    # display to console

    # for game printing to console
    def __str__(self):
        pass

    ###########
    # helper functions used in multiple sections
