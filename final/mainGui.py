from gui.mainDisplay import *

# window size
ROOT_SIZE = Vector2D(1000, 700)
# maximum board size (board will always be less than or equal to this size)
MAX_BOARD_SIZE = Vector2D(600, 500)


def rootGeometry():
    return str(ROOT_SIZE.x) + "x" + str(ROOT_SIZE.y)


def main():
    root = Tk()

    # configure root display
    root.title("Connect 4")
    root.geometry(rootGeometry())
    root.resizable(False, False)

    # handle root grid
    root.grid()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # make main display and center it within root
    mainDisplay = MainDisplay(root, MAX_BOARD_SIZE)
    mainDisplay.grid(row=0, column=0, sticky=(N, E, S, W))

    # start the mainDisplay mainloop()
    mainDisplay.mainloop()


main()
