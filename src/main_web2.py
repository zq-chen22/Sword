from settings import *
from game_webset import GameWebset
from state_util import *
from affect_util import *
import util
from hunguang_zong import HunGuang
from place_util import *
import copy

# pygame.init()  

# for font_name in pygame.font.get_fonts():
#     # if font_name == "华文仿宋":
#     print(font_name)

# exit()

class GameWeb:
    def __init__(self):
        self.window = GameWebset()
        place1 = Qian()
        place2 = Kun()
        util.bondingPlaces((place1, place2))
        solder1 = HunGuang()
        solder2 = HunGuang()
        solder2.setName("DB.Lofen")
        solder2.cname = "子虚"
        solder2.showPosition = "Left"
        solder1.webID = 1
        solder2.color = "Red"
        solder1.setName("DB.Lemon")
        solder1.cname = "乌有"
        solder1.showPosition = "Right"
        solder1.color = "Blue"
        place1.setChampion(solder1)
        place2.setChampion(solder2)
        self.window.insertPlace(place1)
        self.window.insertPlace(place2)
        solder1.setPolicy("key")
        solder2.setPolicy("token", token = "")
        
    
    def run(self):
        while True:
            self.window.runTurn()

if __name__ == '__main__':
    game = GameWeb()
    game.run()