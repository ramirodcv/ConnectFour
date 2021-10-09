# color helper class
from enum import Enum


# store gui and text colors in a class
class TxtColor(Enum):
    RED = "\u001b[31;1m"
    BLUE = "\u001b[34;1m"
    YELLOW = "\u001b[33m"
    WHITE = "\u001b[0m"


class GuiColor(Enum):
    RED = "red"
    BLUE = "blue"
    YELLOW = "yellow"
    WHITE = "white"
    BLACK = "black"
    LIGHT_BLUE = "#A7FCFF"
    LIGHT_GREY = "#C4D4D5"
    GREY = "#687378"
