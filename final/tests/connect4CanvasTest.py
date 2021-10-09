from gui.connect4Canvas import *
from gameSrc.connect4Game import *


moves = (0, 1, 0, 1, 0, 1, 0)
rootSize = Vector2D(1000, 700)


def main():
    root = Tk()
    root.title("Connect4 Canvas Test")
    root.geometry(str(rootSize.x) + "x" + str(rootSize.y))
    root.resizable(False, False)
    root.grid()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    game = Connect4Game(width=7, height=6, inARow=4)

    board = Connect4Canvas(root, game, True, Vector2D(600, 600), cnf={"bg": GuiColor.LIGHT_GREY.value, "border": 0})
    board.grid(row=0, column=0)

    board.mainloop()


main()
