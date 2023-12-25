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
        self.screenPos = (0.5 * WIDTH - 330, 180)
        self.setName("qian")
        self.cname = "乾"

    def showAt(self, pos):
        super().showAt()
        WIN = pygame.display.get_surface()
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 40)
        lines = []
        color = GRAY + "78"
        title = "乾卦第一"
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
        qian = pygame.transform.scale(qian, (0.7 * qian.get_width(), 0.7 * qian.get_height()))
        char = font.render(title, True, color)
        WIN.blit(char, (pos[0]- 10, pos[1] + 180))
        WIN.blit(qian, pos)

class Kun(Place):
    def __init__(self):
        super().__init__()
        self.screenPos = (0.5 * WIDTH + 235, 190)
        self.setName("kun")
        self.cname = "坤"

    def showAt(self, pos):
        super().showAt()
        WIN = pygame.display.get_surface()
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 40)
        lines = []
        color = GRAY + "78"
        title = "坤卦第二"
        img = cv2.imread(os.path.join(PATH, 'graphics', 'property', 'kun.png'))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img[np.linalg.norm(img[:, :, :]/255, axis = 2) ** 2 > 2.7, 3] = 0
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # img = img[int(img.shape[0] * 0.2):int(img.shape[0] * 0.7), int(img.shape[1] * 0.2):int(img.shape[1] * 0.7)]
        # img[:, :, 3] = np.floor(np.array(img[:, :, 3]) * 0.3)
        ink = util.hex_to_rgb(INK)
        img[:, :, :3] = np.floor(255 - (1-img[:, :, :3]/255) * (255 - np.array(ink)))
        # img[:, :, :3] =  np.floor(np.array(img[:, :, :3]) * 0.6)
        qian = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGRA")
        qian = pygame.transform.scale(qian, (0.7 * qian.get_width(), 0.7 * qian.get_height()))
        char = font.render(title, True, color)
        WIN.blit(char, (pos[0] - 10, pos[1] + 170))
        WIN.blit(qian, pos)


class Game:
    def __init__(self):
        self.window = GameWindow()
        place1 = Qian()
        place2 = Kun()
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