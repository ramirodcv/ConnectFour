# Ram's Connect 4
This project required more code than I initially thought.
This README will first outline the basic structure of this project
and then second describe future work that could be done.
Run mainConsole.py for the final product.

# gameSrc folder
This folder contains all logic for managing a game. I specifically designed my code
to be adaptable to any 2 player game. For example, I could pretty easily create tic-tac-toe
and use the move optimizer on it. It also contains code specific to Connect 4.

#### connect4Game.py
This contains Connect4Game, a subclass of Game. This class implements all Game functions
with the logic of the classic connect 4 game (and adds some more board sizing options).

#### game.py
This contains a class with all functions that need to be implemented to use move optimizers on a game.
It describes the basic functionality of all 2 player games.

#### player.py
This contains the Player class that extends Enum. it contains all characteristics for 2 players (and an empty player).
This class is meant to simplify displaying different players in a game.
Player's symbols and colors are contained within this class

# gui folder
This folder contains all code for the game gui (except for what is in mainGui.py).
It defines a frame widget that contains the Connect 4 game.

#### mainDisplay.py
The MainDisplay class extends tkinter.Frame. It defines a game frame that configures and manages
a Connect4Canvas. Place this frame in a Tk object and start its mainloop to play.

#### connect4Canvas.py
This contains Connect4Canvas, which extends tkinter.Canvas.
It colors the board that is displayed, uses click events to determine a player's moves,
and manages a Connect4Game object while the game display is visible.

# miniMax folder
All move optimization is contained within this folder. Files either define the recursive
optimization process or determine how the recursion process occurs (how many steps to take
and which moves to prioritize).

#### optimizers.py
This file defines the outline for a DepthController and a MoveSelector.
DepthControllers define how many recursive calls are made during move optimization.
MoveSelectors define which moves to search during the recursive process.
Both optimizers used during gameplay will be described below.

#### maxSteps.py (DepthController)
This file contains a class that maximizes the number of recursive calls made.
Each recursive call is explored by the same number of steps (move 1 and move 2 would
be searched an equal amount if these moves are taken).

#### adjMoves.py (MoveSelector)
This folder contains the AdjMoves class that prioritizes moves adjacent to recently made moves
(it will remember up to a specified number of moves: memory=...).
If no adjacent moves are available, all available moves will be prioritized.

#### miniMax.py
###### see: https://github.com/Cledersonbc/tic-tac-toe-minimax
This contains the MiniMax class containing only static methods. bestMoves() takes a Game, a Player, a MoveSelector, and
a DepthController and recursively determines what move the player should take.
It scores gameStates after recursion is stopped and selects the best move given those state evaluations.
Note that DepthController and the Game ending define when recursion stops.
Only moves defined by the MoveSelector will be taken.

# tests
This folder contains test for various classes. not everything is updated. I would ignore this folder.

# utils
This folder contains classes useful for this project that do not relate to any other folder.

#### color.py
This folder contains console and gui colorings

#### vector2D.py
This contains the Vector2D class that has the functionality of any common 2D vector.

## mainConsole.py
Run this folder to play connect 4 on the text console.

## mainGui.py
Run this folder to play connect 4 on a GUI display (this is what is outlined in the project proposal).

# Future Work
#### GUI
When the program runs the long optimization process, the window is unresponsive, because the event handler
is executed by the mainloop. I would eventually like to handle the CPU's move on a separate Thread.

#### Optimization
I would like more to create more dynamic MoveSelectors and DepthControllers. I would like to prioritize
moves that can result in wins or loses. I would also like to search certain recursive calls more deeply if they
have more realistic game states.

#### Games
I would like to create more Game subclasses. I am specifically interested in creating a checkers game.

