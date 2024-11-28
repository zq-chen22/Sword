import pygame
from settings import *
from place import Place
from state_util import *
from affect_util import *
import numpy as np
import util
import cv2

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
        self.showTitle = "乾卦第一"

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
        char = font.render(self.showTitle, True, color)
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
        self.showTitle = "坤卦第二"

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
        char = font.render(self.showTitle, True, color)
        WIN.blit(char, (pos[0] - 10, pos[1] + 170))
        if self.placeImg is None:
            self.placeImgInit()
        WIN.blit(self.placeImg, pos)