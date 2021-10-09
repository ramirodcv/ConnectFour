from utils.vector2D import *
from gameSrc.game import *
from gameSrc.player import *
from utils.color import *


# class that wraps players, so colorings can be changed if a win occurred
class Entry:
    # text coloring
    __T_WINNER = TxtColor.YELLOW.value
    __T_REG = TxtColor.WHITE.value

    # GUI coloring
    __G_WINNER = GuiColor.YELLOW.value

    def __init__(self, player):
        self.player = player
        self.__isWinner = False

    # set this entry as part of the connect 4 win (color it yellow)
    def setAsWinner(self, isWinner=True):
        self.__isWinner = isWinner

    def getGuiColor(self):
        if self.__isWinner:
            return Entry.__G_WINNER
        return self.player.getGuiColor()

    def __str__(self):
        # recolor to winner color
        if self.__isWinner:
            output = (Entry.__T_WINNER + self.player.getSymbol() + Entry.__T_REG)
        # return regular player str
        else:
            output = str(self.player)
        return output

    # self.player != Player.EMPTY
    def __bool__(self):
        return bool(self.player)


# takes on a range of valid values and a default value
class BoardCharacteristic:
    def __init__(self, least=6, most=10, default=6):
        self.least = least
        self.most = most
        self.default = default

    # if the given value is within the range of self
    def __contains__(self, item):
        if type(item) != int:
            return False
        return self.least <= item <= self.most


class Connect4Game(Game):
    # directions to for counting streaks (negate for other 4 directions)
    __CHECK_DIR = (Vector2D(0, 1), Vector2D(1, 1), Vector2D(1, 0), Vector2D(1, -1))

    # empty entry to handle all unused spots
    __EMPTY_ENTRY = Entry(Player.EMPTY)

    # board characteristics for width, height, and in a row
    __HEIGHT = BoardCharacteristic(least=6, most=9, default=6)
    __WIDTH = BoardCharacteristic(least=6, most=9, default=7)
    __IN_A_ROW = BoardCharacteristic(least=3, most=6, default=4)

    # returns if the board characteristics would be valid
    @staticmethod
    def valid(width=__WIDTH.default, height=__HEIGHT.default, inARow=__IN_A_ROW.default):
        return width in Connect4Game.__WIDTH and height in Connect4Game.__HEIGHT and inARow in Connect4Game.__IN_A_ROW

    # gets __EMPTY_ENTRY
    @staticmethod
    def emptyEntry():
        return Entry(Player.EMPTY)

    # get board characteristic requirements
    @staticmethod
    def getWidthRange():
        return Connect4Game.__WIDTH

    @staticmethod
    def getHeightRange():
        return Connect4Game.__HEIGHT

    @staticmethod
    def getRowLengthRange():
        return Connect4Game.__IN_A_ROW

    def __init__(self, width=__WIDTH.default, height=__HEIGHT.default, inARow=__IN_A_ROW.default):
        # if invalid connect4 board characteristics
        if not Connect4Game.valid(width=width, height=height, inARow=inARow):
            raise ValueError("Invalid connect4 characteristics.")

        # board characteristics
        self.__dim = Vector2D(width, height)
        self.__inARow = inARow

        # game state variables
        self.__moveMade = 0
        self.__winner = None
        self.__board = list()
        for i in range(self.__dim.x):
            self.__board.append(list())

        # change Player symbols
        Player.P1.set(symbol="x")
        Player.P2.set(symbol="o")

    ###############
    # game characteristics

    # return the max score that can be returned from move
    def maxScore(self):
        return self.__inARow

    # get the dimensions of this board
    def dim(self):
        return Vector2D(self.__dim.x, self.__dim.y)

    ##############
    # game validity

    # return true there are no more available moves (usually board not full)
    def full(self):
        return self.__moveMade >= (self.__dim.x * self.__dim.y)

    # returns the winner of this game (Player.EMTPY for no winner)
    def winner(self):
        return self.__winner

    ############
    # move validity and move lists for optimizers

    # if the given item (move) is in this game
    def __contains__(self, item):
        # column is on the board
        if type(item) == int:
            return 0 <= item < self.__dim.x
        # location is on the board
        if type(item) == Vector2D:
            return 0 <= item.x < self.__dim.x and 0 <= item.y < self.__dim.y
        # not a valid item
        return False

    # returns true if the given move can be made
    def validMove(self, move):
        # not a valid move
        if move not in self or type(move) != int:
            return False
        # return true if column is not full
        return len(self.__board[move]) < self.__dim.y

    # get all moves adjacent to the given move
    def adj(self, location):
        if location not in self or type(location) != int:
            return None
        output = list()
        if (location - 1) in self:
            output.append(location - 1)
        if (location + 1) in self:
            output.append(location + 1)
        return output

    # return all possible moves
    def allMoves(self):
        return range(self.__dim.x)

    ############
    # movement and scoring

    # returns None if no move was made
    # returns a score if the move was made (equal to maxScore if win occurred)
    def move(self, move, player: Player, undoable=False):
        # if not a valid move
        if not self.validMove(move) or not Player:
            return None
        # make the move
        self.__board[move].append(Entry(player))
        self.__moveMade += 1
        return self.scoreMove(self.getTopLocation(move), player, undoable)

    # undo a move
    # the move being reverted must be made with undoable=True for correct behavior
    def undoMove(self, move):
        # if not a valid move
        if move not in self or type(move) != int:
            return False
        # if move was not made
        if len(self.__board[move]) <= 0:
            return False
        # remove move
        self.__moveMade -= 1
        self.__board[move].pop()
        return True

    # score the current game state
    def scoreState(self):
        score = StateScore()
        # get the highest score for both players from all the top(active) positions in the board
        for i in range(self.__dim.x):
            top = self.getTopLocation(i)
            entry = self[top]
            if top and entry:
                score[entry.player] = max(self.__scoreLocation(top, entry.player), score[entry.player])
        return score

    # score the given move (and handle winning if not undoable)
    def scoreMove(self, move, player, undoable):
        bestScore = 0
        # for each direction to check
        for direction in self.__CHECK_DIR:
            # score the direction
            bestScore = max(self.__countStreak(player, move, direction, undoable), bestScore)
            if bestScore == self.maxScore():
                return bestScore
        return bestScore

    # count how many moves a player has made in a streak
    # streak is a line in on the board (horizontal, vertical, or diagonal)
    def __countStreak(self, player, location, direction, undoable):
        # needed pieces in a row to win
        needed = self.__inARow - 1
        # count the pieces in a row in one direction
        needed -= self.__countDirection(player, location, direction, needed)
        # calculate row start (for coloring winning locations)
        rowStart = location + direction.scale(self.__inARow - 1 - needed)
        # count the pieces in a row in the anti-parallel direction
        needed -= self.__countDirection(player, location, direction.scale(-1), needed)
        # if player won and win should be handled
        if needed <= 0 and not undoable:
            self.__winner = player
            self.__colorWinner(rowStart, direction.scale(-1))
        return self.maxScore() - needed

    # count how many pieces there are in a row starting at a location in a specified direction
    # specified location is not a part of the count (assumed player already moved there)
    def __countDirection(self, player, location, direction, neededCount):
        inARow = 0
        temp = location + direction  # the next location to compare to
        while self[temp].player == player and inARow < neededCount:
            inARow += 1
            temp += direction
        return inARow

    # color the winning streak
    def __colorWinner(self, location, direction):
        for i in range(self.__inARow):
            self[location + direction.scale(i)].setAsWinner()

    # score a location
    # score is 0 if the streak made with the given location cannot form winning streak
    # that is (in the classic 4 in a row): xooox -> the three o's cannot forma  winning streak
    # if the streak can form a winning streak, return the streaks length
    def __scoreLocation(self, location, player):
        # get the best streak in each win direction
        bestScore = 0
        for dir in Connect4Game.__CHECK_DIR:
            bestScore = max(self.__scoreStreak(location, dir, player), bestScore)
        return bestScore

    # score a given streak at the specified location in the given direction
    def __scoreStreak(self, location, direction, player):
        # streak size (assume player already moved at the given location)
        streakSize = 1
        maxStreak = 1
        # get the row size and max row size in one direction (max row size is less than game.maxScore())
        temp1, temp2 = self.__scoreDirection(location, direction, player)
        streakSize += temp1
        maxStreak += temp2
        # get the row size and max row size in the anti-parallel direction
        temp1, temp2 = self.__scoreDirection(location, direction.scale(-1), player)
        streakSize += temp1
        maxStreak += temp2
        # if this streak cannot be a winning streak return 0, else return the streak's size
        if maxStreak < self.__inARow:
            streakSize = 0
        return streakSize

    # get the a row's size and maxSize in a given direction
    def __scoreDirection(self, location, direction, player):
        streakSize = 0
        maxStreak = 0
        temp = location + direction  # next location to compare to
        streak = True
        # while board edge or opponent has not been hit and we checked up to self.maxScore()
        while self[temp].player != player.next() and temp in self and maxStreak < self.__inARow:
            if self[temp].player == player and streak:
                streakSize += 1
            else:
                streak = False
            maxStreak += 1
            temp += direction

        return streakSize, maxStreak

    ############
    # display to console

    # for game printing to console
    def __str__(self):
        output = ""
        loc = Vector2D()

        for j in range(self.__dim.y - 1, -1, -1):
            for i in range(self.__dim.x):
                # store the string value of the given Entry
                output += str(self[loc.set(x=i, y=j)]) + " "
            # move to new line after row is added
            if j != 0:
                output += "\n"
        return output

    ###########
    # helper functions used in multiple sections

    # int: get the top Entry in a column
    # Vector2D: get the Entry at the given location
    def __getitem__(self, item):
        res = Connect4Game.__EMPTY_ENTRY
        # invalid location
        if item not in self:
            pass
        # if type int and the top location is valid, return the entry at that top location
        elif type(item) == int:
            top = self.getTopLocation(item)
            if top:
                res = self.__board[top.x][top.y]
        # if Vector2D and the given location is valid, return the corresponding Entry
        elif type(item) == Vector2D:
            if item.y < len(self.__board[item.x]):
                res = self.__board[item.x][item.y]
        return res

    # get the location of the top move in a column
    # None for no moves in column
    def getTopLocation(self, col: int):
        # invalid column
        if col not in self:
            return None
        # move not made on the given column
        if len(self.__board[col]) <= 0:
            return None
        return Vector2D(col, len(self.__board[col]) - 1)
