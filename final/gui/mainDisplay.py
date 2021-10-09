from gui.connect4Canvas import *
from gameSrc.connect4Game import *
from utils.color import *


class MainDisplay(Frame):
    # cnf for frames that manage widget layout
    __CNF = {
        "bg": GuiColor.LIGHT_GREY.value,
        "border": 0
    }
    # cnf for configuration frames (show up as panels in config display)
    __CONFIG_FRAME_CNF = {
        "bg": GuiColor.WHITE.value,
        "highlightbackground": GuiColor.BLACK.value,
        "highlightthickness": 5
    }
    # cnf for configuration sliders
    __SLIDER_CNF = {
        "length": 250,
        "orient": HORIZONTAL,
        "bg": GuiColor.WHITE.value,
        "highlightbackground": GuiColor.WHITE.value,
        "troughcolor": GuiColor.GREY.value,
        "width": 20
    }
    # cnf for Connect 4 board
    __BOARD_CNF = {
        "bg": GuiColor.GREY.value,
        "bd": 2,
        "highlightbackground": GuiColor.BLACK.value
    }

    # default fonts
    __HEADER_FONT = "Arial 40 bold"
    __OPTIONS_FONT = "Arial 20"

    def __init__(self, root, maxBoardSize):
        super(MainDisplay, self).__init__(root, cnf=MainDisplay.__CNF)
        # configure self grid
        self.grid(sticky=(N, S, E, W))
        self.grid_columnconfigure(0, weight=1),
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        ############################################
        # make gameplay display (start hidden)
        self.connect4Canvas = None
        self.maxBoardSize = maxBoardSize
        # make frame to contain Connect4canvas and gameLabel
        self.gameDisplay = Frame(self, cnf=MainDisplay.__CNF)
        self.gameDisplay.grid(row=1, column=0, columnspan=2, sticky=(N, E, S, W))
        self.gameDisplay.grid_rowconfigure(0, weight=1)
        self.gameDisplay.grid_rowconfigure(1, weight=3)
        self.gameDisplay.grid_columnconfigure(0, weight=1)
        # create game label
        self.gameLabel = Label(self.gameDisplay, text="", font=MainDisplay.__HEADER_FONT, cnf=MainDisplay.__CNF)
        self.gameLabel.grid(row=0, column=0, sticky=(N, E, S, W))
        self.gameDisplay.grid_remove()

        # make exit button and hide it (used with game display)
        self.exitButton = Button(self, text="EXIT", font="Arial 16", command=self.exitButton)
        self.exitButton.grid(row=0, column=1, sticky=E, padx=(5, 5), pady=(5, 5))
        self.exitButton.grid_remove()
        # make row length label and hide it (used in game display)
        self.rowLengthLabel = Label(self, text="", font="Arial 16 underline", cnf=MainDisplay.__CNF)
        self.rowLengthLabel.grid(row=0, column=0, sticky=E, padx=(5, 5), pady=(5, 5))
        self.rowLengthLabel.grid_remove()

        ##########################################################
        # make configuration display (used to select game characteristics)
        self.configDisplay = Frame(self, cnf=MainDisplay.__CNF)
        self.configDisplay.grid(row=1, column=0, columnspan=2, pady=(20, 0), sticky=(N, E, S, W))
        self.configDisplay.grid()
        self.configDisplay.grid_rowconfigure(0, weight=1)
        self.configDisplay.grid_rowconfigure(1, weight=1)
        self.configDisplay.grid_rowconfigure(2, weight=1)
        self.configDisplay.grid_columnconfigure(0, weight=1)
        self.configDisplay.grid_columnconfigure(1, weight=3)

        # make config header label
        self.label = Label(
            self.configDisplay,
            cnf=MainDisplay.__CNF,
            text="Welcome to Connect4",
            font=MainDisplay.__HEADER_FONT
        )
        self.label.grid(row=0, column=0, columnspan=2, sticky=(N, E, S, W))

        # make the left configuration frame (player options)
        tempFrame = Frame(self.configDisplay, cnf=MainDisplay.__CONFIG_FRAME_CNF)
        tempFrame.grid(row=1, column=0, padx=(40, 20), pady=(10, 10), sticky=(N, E, S, W))
        tempFrame.grid_rowconfigure(0, weight=1)
        tempFrame.grid_rowconfigure(1, weight=1)
        tempFrame.grid_columnconfigure(0, weight=1)
        # pvp option
        self.playerConfig = StringVar(value="pvp")
        self.pvp = Radiobutton(
            tempFrame,
            text="Player vs. Player",
            variable=self.playerConfig,
            value="pvp",
            font=MainDisplay.__OPTIONS_FONT,
            bg=GuiColor.WHITE.value,
        )
        self.pvp.grid(row=0, column=0, pady=(20, 0))
        # pvc option
        self.pvc = Radiobutton(
            tempFrame,
            text="Player vs. Computer",
            variable=self.playerConfig,
            value="pvc",
            font=MainDisplay.__OPTIONS_FONT,
            bg=GuiColor.WHITE.value,
        )
        self.pvc.grid(row=1, column=0, pady=(0, 20))

        # make the left configuration frame (game characteristics)
        tempFrame = Frame(self.configDisplay, cnf=MainDisplay.__CONFIG_FRAME_CNF)
        tempFrame.grid(row=1, column=1, padx=(20, 40), pady=(10, 10), sticky=(N, E, S, W))
        tempFrame.grid_rowconfigure(0, weight=1)
        tempFrame.grid_rowconfigure(1, weight=1)
        tempFrame.grid_rowconfigure(2, weight=1)
        tempFrame.grid_columnconfigure(0, weight=1)
        tempFrame.grid_columnconfigure(1, weight=1)
        # add labels for each characteristics
        # width
        tempLabel = Label(
            tempFrame,
            text="width:",
            font=MainDisplay.__OPTIONS_FONT,
            bg=GuiColor.WHITE.value
        )
        tempLabel.grid(row=0, column=0)
        # height
        tempLabel = Label(
            tempFrame,
            text="height:",
            font=MainDisplay.__OPTIONS_FONT,
            bg=GuiColor.WHITE.value
        )
        tempLabel.grid(row=1, column=0)
        # row length
        tempLabel = Label(
            tempFrame,
            text="win length:",
            font=MainDisplay.__OPTIONS_FONT,
            bg=GuiColor.WHITE.value
        )
        tempLabel.grid(row=2, column=0)
        # add a slider for each characteristic
        tempRange = Connect4Game.getWidthRange()
        # width
        self.widthVar = IntVar(value=tempRange.default)
        scale = Scale(
            tempFrame,
            from_=tempRange.least,
            to=tempRange.most,
            variable=self.widthVar,
            cnf=MainDisplay.__SLIDER_CNF
        )
        scale.grid(row=0, column=1)
        # height
        tempRange = Connect4Game.getHeightRange()
        self.heightVar = IntVar(value=tempRange.default)
        scale = Scale(
            tempFrame,
            from_=tempRange.least,
            to=tempRange.most,
            variable=self.heightVar,
            cnf=MainDisplay.__SLIDER_CNF
        )
        scale.grid(row=1, column=1)
        # row length
        tempRange = Connect4Game.getRowLengthRange()
        self.rowLengthVar = IntVar(value=tempRange.default)
        scale = Scale(
            tempFrame,
            from_=tempRange.least,
            to=tempRange.most,
            variable=self.rowLengthVar,
            cnf=MainDisplay.__SLIDER_CNF
        )
        scale.grid(row=2, column=1)

        # make the start game button
        self.playButton = Button(self.configDisplay, text="START GAME", font="Arial 40", command=self.startGame)
        self.playButton.grid(row=2, column=0, columnspan=2)

    # exit button event handler
    def exitButton(self):
        # if not in play state break
        if self.connect4Canvas is None:
            return
        # hide game display widgets and destroy the Connect4Canvas
        self.gameDisplay.grid_remove()
        self.connect4Canvas.destroy()
        self.connect4Canvas = None
        self.exitButton.grid_remove()
        self.rowLengthLabel.grid_remove()

        # show the configuration display
        self.configDisplay.grid()

    # when start game is pressed
    def startGame(self):
        # show exit button and rowLengthLabel
        self.exitButton.grid()
        self.exitButton.config(state=ACTIVE)
        self.rowLengthLabel.grid()
        self.rowLengthLabel.config(text=("Get " + str(self.rowLengthVar.get()) + " in-a-row to win."))

        # hide the configuration display
        self.configDisplay.grid_remove()

        # make a new Connect4Canvas with the specified characteristics and show game display widgets
        self.connect4Canvas = Connect4Canvas(
            self.gameDisplay,
            Connect4Game(width=self.widthVar.get(), height=self.heightVar.get(), inARow=self.rowLengthVar.get()),
            self.playerConfig.get() == "pvc",
            self.maxBoardSize,
            self.setGameLabel,
            cnf=MainDisplay.__BOARD_CNF
        )
        self.connect4Canvas.grid(row=1, column=0, pady=(0, 20))
        self.setGameLabel(Player.P1, self.playerConfig.get() == "pvc", Player.EMPTY, True)
        self.gameDisplay.grid()

    # sets the game label to inform the user who's turn it is
    def setGameLabel(self, player, useCpu, winner, game):
        # stalemate
        if not winner and not game:
            self.gameLabel.config(text="Draw. There is no winner.")

        # win occurred
        elif winner == Player.P1 and not useCpu:
            self.gameLabel.config(text="Congratulations Red, you won!!!")
        elif winner == Player.P1 and useCpu:
            self.gameLabel.config(text="Congratulations, you won!!!")
        elif winner == Player.P2 and not useCpu:
            self.gameLabel.config(text="Congratulations Blue, you won!!!")
        elif winner == Player.P2 and useCpu:
            self.gameLabel.config(text="You lose. Press exit to play again.")

        # win did not occur
        elif player == Player.P1 and not useCpu:
            self.gameLabel.config(text="Red please make your move.")
        elif player == Player.P1 and useCpu:
            self.gameLabel.config(text="Please make a move.")
        elif player == Player.P2 and not useCpu:
            self.gameLabel.config(text="Blue please make your move.")
        else:  # player == Player.P2 and useCpu
            self.gameLabel.config(text="CPU turn.")
        # force update on the label
        self.update()
