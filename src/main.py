import pygame, sys
from settings import *
from game_window import GameWindow
from champion import Champion
from place import Place
from affect import Affect
from skill import Skill
from state import State
from state_util import *
from affect_util import *
import util
from hunguang_zong import HunGuang

# pygame.init()  

# for font_name in pygame.font.get_fonts():
#     # if font_name == "华文仿宋":
#     print(font_name)

# exit()

class Game:
    def __init__(self):
        self.window = GameWindow()
        place1 = Place()
        place1.setName("east stone")
        place2 = Place()
        place2.setName("west stone")
        util.bondingPlaces((place1, place2))
        solder1 = HunGuang()
        solder2 = HunGuang()
        solder1.setName("DB.Lofen")
        solder2.setName("DB.Lemon")
        place1.setChampion(solder1)
        place1.setChampion(solder2)
        self.window.insertPlace(place1)
        self.window.insertPlace(place2)
        # general setup

        solder1.setPolicy("random")
        solder2.setPolicy("random")
        # sound 
        
    
    def run(self):
        while True:
            self.window.runTurn()

if __name__ == '__main__':
    game = Game()
    game.run()