from tkinter import *
from gui.playDisplay import *
from gameSrc.connect4Game import *


rootSize = Vector2D(1000, 700)
maxBoardSize = Vector2D(600, 600)

def main():
    root = Tk()
    root.title("Play Display Test")
    root.geometry(str(rootSize.x) + "x" + str(rootSize.y))
    root.resizable(False, False)
    root.grid()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    game = Connect4Game(width=7, height=6, inARow=4)

    play = PlayDisplay(root, game, False, maxBoardSize)
    play.grid(row=0, column=0, sticky=(N, E, S, W))

    play.mainloop()


main()
