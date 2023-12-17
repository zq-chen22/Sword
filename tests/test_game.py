# the main game
import sys

sys.path.append('E:\game\Sword\src')

from champion import Champion
from place import Place
from affect import Affect
from skill import Skill
from state import State
from state_util import *
from affect_util import *
import util
from hunguang_zong import HunGuang
from game_ground import GameGround

if __name__ == "__main__":
    print("This part of game is to manipulate a solder to beat another solder")
    place1 = Place()
    place1.setName("east stone")
    place2 = Place()
    place2.setName("west stone")
    util.bondingPlaces((place1, place2))
    solder1 = HunGuang()
    solder2 = HunGuang()
    solder1.setName("DB.Lofen")
    solder2.setName("DB.Lemon")
    solder1.setPolicy("random")
    solder2.setPolicy("random")
    # solder1.setPolicy("input")
    # solder2.setPolicy("input")
    # solder1.setPolicy("token", token = "QQ W QQ QQ")
    # solder2.setPolicy("token", token = "S W Q ")
    place1.setChampion(solder1)
    place1.setChampion(solder2)
    game = GameGround()
    game.insertPlace(place1)
    game.insertPlace(place2)
    for i in range(1000):
        game.runTurn()
        if solder1.isSurvive() and not solder2.isSurvive():
            print(f"{solder1.__str__()} wins.")
        elif not solder1.isSurvive() and solder2.isSurvive():
            print(f"{solder2.__str__()} wins.")
        elif not solder1.isSurvive() and not solder2.isSurvive():
            print("It's a draw.")
        else:
            continue
        print(solder1.token)
        print(solder2.token)
        break


        #     print(i, file = file)
        #     print(place1.affects, file = file)
        #     print(place2.affects, file = file)