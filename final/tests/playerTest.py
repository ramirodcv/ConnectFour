from assignments.final.gameSrc.player import Player
from assignments.final.utils.color import TxtColor


def main():
    Player.P1.set(symbol="x", color=TxtColor.RED)
    Player.P2.set(symbol="o", color=TxtColor.BLUE)
    Player.EMPTY.set(symbol="-", color=TxtColor.WHITE)

    print(Player.P1)
    print(Player.P2)
    print(Player.EMPTY)


main()