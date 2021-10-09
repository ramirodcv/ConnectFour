from tkinter import *
from miniMax.miniMax import *
from miniMax.depthController.maxSteps import *
from miniMax.moveSelector.adjMoves import *
from utils.vector2D import *
from time import *


# makes a board canvas (gameplay is handled internally and makes use of event binding)
class Connect4Canvas(Canvas):
    # display and gameplay constants
    __ENTRY_PROP = 0.75  # how much of the column/row space the circles take up (must be less than 1)
    __CPU_MOVE_TIME = 0.75
    __PLAYER_MOVE_TIME = 0.1

    # best move search parameters
    __MAX_STEPS = 4
    __MEMORY = 4

    def __init__(self, master, game, useCpu, maxDim, labelFunc, cnf=None):
        # calculate entry size, so this board is contained within the maxDim constraint
        self.entrySize = min(maxDim.x / game.dim().x, maxDim.y / game.dim().y)
        super(Connect4Canvas, self).__init__(
            master,
            width=game.dim().x * self.entrySize,
            height=game.dim().y * self.entrySize,
            cnf=cnf,
        )

        # game logic variables
        self.game = game
        self.player = Player.P1
        self.winner = Player.EMPTY

        # cpu variables
        self.useCpu = useCpu
        self.dc = None
        self.ms = None
        if useCpu:
            self.dc = MaxSteps(maxSteps=Connect4Canvas.__MAX_STEPS)
            self.ms = AdjMoves(game=game, memory=Connect4Canvas.__MEMORY)

        # handle display
        self.__colorAllEntries()
        self.labelFunc = labelFunc

        # bind mouse click handler
        self.bind("<Button 1>", self.click)

    # click event (use move)
    def click(self, event):
        # break if not user move or game is over
        if not self.__isPlayerTurn() or not self.game:
            return

        # calculate the move
        move = int(event.x / self.entrySize)
        # correct for rounding errors (not exact to the pixel everytime)
        if move == self.game.dim().x:
            move -= 1
        # make the move
        self.__makeMove(move, delay=Connect4Canvas.__PLAYER_MOVE_TIME)

    # returns true if it is a player's turn (not CPU)
    def __isPlayerTurn(self):
        return not self.useCpu or self.player == Player.P1

    # CPU finds optimal move and executes it
    def __cpuTurn(self):
        start = time()
        # get minimax optimal move
        move = MiniMax.bestMove(
            self.game,
            self.player,
            depthController=self.dc,
            moveSelector=self.ms,
        )
        # calculate time left in CPU turn
        delay = Connect4Canvas.__CPU_MOVE_TIME - (time() - start)
        if delay <= 0:
            delay = None
        # make move and delay by the time left in the CPU's turn
        self.__makeMove(move, delay=delay)

    # make the given move and disallow click events during the delay period
    # delay is in seconds
    def __makeMove(self, move, delay=None):
        # break if not a valid move
        if not self.game.validMove(move):
            return

        # unbind mouse event
        self.bind("<Button 1>", lambda x: None)
        # make move and score it
        score = self.game.move(move, self.player)
        # increment optimizer variables
        if self.useCpu:
            self.dc = self.dc.next(move=move, score=score, optimizing=False)
            self.ms = self.ms.next(move=move, score=score, optimizing=False)

        # delay for the given amount of time
        if delay and type(delay) == int:
            sleep(delay)

        # update display and handle player/winner variables
        self.winner = self.game.winner()
        self.__color(entry=self.game.getTopLocation(move), colorAll=(score == self.game.maxScore()))
        self.player = self.player.next()
        self.labelFunc(self.player, self.useCpu, self.winner, self.game)

        # have the CPU move if it is the CPU's turn
        if not self.__isPlayerTurn():
            self.__cpuTurn()

        # try to rebind click event
        # this raises an Error when destroying this widget at certain times so use try except
        try:
            self.bind("<Button 1>", self.click)
        except:
            pass

    # color the specified entries
    # colorAll: color all entries if true
    # entry: color a single specified entry
    def __color(self, entry=None, colorAll=False):
        if colorAll:
            self.__colorAllEntries()
        elif entry is not None:
            self.__colorEntry(entry)

    # color the given entry
    def __colorEntry(self, entry):
        # if not a valid entry break
        if entry not in self.game:
            return

        # get the height of this board
        height = self.game.dim().y * self.entrySize

        # define graphics location
        topLeft = entry.scale(self.entrySize)
        eToP = Vector2D(
            x=self.entrySize * (1 - Connect4Canvas.__ENTRY_PROP) / 2,
            y=self.entrySize * (1 - Connect4Canvas.__ENTRY_PROP) / 2,
        )
        p0 = topLeft + eToP
        eToP.x = self.entrySize - eToP.x
        eToP.y = self.entrySize - eToP.y
        p1 = topLeft + eToP

        # flip y values, because graphics to game indexing is reversed
        p0.y = height - p0.y
        p1.y = height - p1.y

        # get entry from game and color the entry on the board
        entry = self.game[entry]
        self.create_oval(p0.x, p0.y, p1.x, p1.y, fill=entry.getGuiColor())

    # color each entry on the board
    def __colorAllEntries(self):
        entry = Vector2D()
        # for each entry in game
        for i in range(self.game.dim().x):
            for j in range(self.game.dim().y):
                # color the entry
                self.__colorEntry(entry=entry.set(x=i, y=j))
                
