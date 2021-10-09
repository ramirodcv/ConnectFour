from utils.color import *


# contain characteristics for a single player
class Player:
    def __init__(self, symbol="-", txtColor=TxtColor.WHITE, guiColor=GuiColor.WHITE):
        self.symbol = symbol
        self.txtColor = txtColor.value
        self.guiColor = guiColor.value

    # set characteristics for this player
    def set(self, symbol=None, txtColor=None, guiColor=None):
        if symbol:
            self.symbol = symbol
        if txtColor:
            self.txtColor = txtColor.value
        if guiColor:
            self.guiColor = guiColor.value

    # return the text str of this character
    def __str__(self):
        return self.txtColor + self.symbol


# contain all players in this enum
class Player(Enum):
    P1 = Player(symbol="1", txtColor=TxtColor.RED, guiColor=GuiColor.RED)
    P2 = Player(symbol="2", txtColor=TxtColor.BLUE, guiColor=GuiColor.BLUE)
    EMPTY = Player()  # have an empty player to replace null (makes handling __str__() easier for games)

    # get the next player (use after every turn)
    def next(self):
        if self == Player.P1:
            return Player.P2
        if self == Player.P2:
            return Player.P1
        # default
        return Player.EMPTY

    # set this players characteristics
    def set(self, symbol=None, txtColor=None, guiColor=None):
        self.value.set(symbol=symbol, txtColor=txtColor, guiColor=guiColor)

    # accessors for this player
    def getSymbol(self):
        return self.value.symbol

    def getTxtColor(self):
        return self.value.txtColor

    def getGuiColor(self):
        return self.value.guiColor

    def __str__(self):
        return str(self.value) + Player.EMPTY.value.txtColor

    def __bool__(self):
        return self != Player.EMPTY
