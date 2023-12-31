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
import numpy as np
import util
import cv2
from hunguang_zong import HunGuang

# pygame.init()  

# for font_name in pygame.font.get_fonts():
#     # if font_name == "华文仿宋":
#     print(font_name)

# exit()

class Qian(Place):
    def __init__(self):
        super().__init__()
        self.screenPos = (0.5 * WIDTH - 350, 180)
        self.setName("qian")
        self.cname = "乾"

    def placeImgInit(self):
        super().placeImgInit()
        img = cv2.imread(os.path.join(PATH, 'graphics', 'property', 'qian.png'))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img[np.linalg.norm(img[:, :, :]/255, axis = 2) ** 2 > 2.7, 3] = 0
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        # img = img[int(img.shape[0] * 0.2):int(img.shape[0] * 0.7), int(img.shape[1] * 0.2):int(img.shape[1] * 0.7)]
        # img[:, :, 3] = np.floor(np.array(img[:, :, 3]) * 0.3)
        ink = util.hex_to_bgr(INK)
        img[:, :, :3] = np.floor(255 - (1-img[:, :, :3]/255) * (255 - np.array(ink)))
        # img[:, :, :3] =  np.floor(np.array(img[:, :, :3]) * 0.6)
        qian = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGRA")
        self.placeImg = pygame.transform.scale(qian, (0.7 * qian.get_width(), 0.7 * qian.get_height()))

    def showAt(self, pos):
        pos = (pos[0]+20, pos[1])
        super().showAt()
        WIN = pygame.display.get_surface()
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 40)
        color = GRAY + "78"
        title = "乾卦第一"
        char = font.render(title, True, color)
        WIN.blit(char, (pos[0]- 10, pos[1] + 180))
        if self.placeImg is None:
            self.placeImgInit()
        WIN.blit(self.placeImg, pos)

class Kun(Place):
    def __init__(self):
        super().__init__()
        self.screenPos = (0.5 * WIDTH + 200, 190)
        self.setName("kun")
        self.cname = "坤"

    def placeImgInit(self):
        super().placeImgInit()
        img = cv2.imread(os.path.join(PATH, 'graphics', 'property', 'kun.png'))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img[np.linalg.norm(img[:, :, :]/255, axis = 2) ** 2 > 2.7, 3] = 0
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        ink = util.hex_to_rgb(INK)
        img[:, :, :3] = np.floor(255 - (1-img[:, :, :3]/255) * (255 - np.array(ink)))
        kun = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGRA")
        self.placeImg = pygame.transform.scale(kun, (0.7 * kun.get_width(), 0.7 * kun.get_height()))

    def showAt(self, pos):
        pos = (pos[0]+35, pos[1])
        super().showAt()
        WIN = pygame.display.get_surface()
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 40)
        color = GRAY + "78"
        title = "坤卦第二"
        char = font.render(title, True, color)
        WIN.blit(char, (pos[0] - 10, pos[1] + 170))
        if self.placeImg is None:
            self.placeImgInit()
        WIN.blit(self.placeImg, pos)


class Game:
    def __init__(self):
        self.window = GameWindow()
        place1 = Qian()
        place2 = Kun()
        util.bondingPlaces((place1, place2))
        solder1 = HunGuang()
        solder2 = HunGuang()
        solder1.setName("DB.Lofen")
        solder1.cname = "子虚"
        solder1.showPosition = "Left"
        solder1.color = "Red"
        solder2.setName("DB.Lemon")
        solder2.cname = "乌有"
        solder2.showPosition = "Right"
        solder2.color = "Blue"
        place1.setChampion(solder1)
        place1.setChampion(solder2)
        self.window.insertPlace(place1)
        self.window.insertPlace(place2)
        # general setup

        solder1.setPolicy("key")
        solder2.setPolicy("key")
        # sound 
        
    
    def run(self):
        while True:
            self.window.runTurn()

if __name__ == '__main__':
    game = Game()
    game.run()