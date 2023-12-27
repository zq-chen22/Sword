from game_ground import GameGround
from settings import *
import pygame
import util 
import cn2an
import cv2
import numpy as np

class GameWindow(GameGround):
	def __init__(self):
		super().__init__()
		pygame.init()
		self.window = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
		pygame.display.set_caption('华山论剑2.5.2')

		self.clock = pygame.time.Clock()
		self.titleFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
		self.font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
		self.smallFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 32)

		self.BG = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'graphics', 'background', 'notebook.jpg')), (WIDTH, HEIGHT))
		img = cv2.imread(os.path.join(PATH, "graphics", "property", "taichi.jpg"))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
		# print(np.linalg.norm(img[:, :, :]/255, axis = 2) > 0.9)
		img[np.linalg.norm(img[:, :, :]/255, axis = 2) ** 2 > 2.8, 3] = 0
		img = img[int(img.shape[0] * 0.2):int(img.shape[0] * 0.7), int(img.shape[1] * 0.2):int(img.shape[1] * 0.7)]
		img[:, :, 3] = np.floor(np.array(img[:, :, 3]) * 0.2) 
		self.taichi = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "BGRA")
		self.taichi = pygame.transform.scale(self.taichi, (self.taichi.get_width() * 1.5, self.taichi.get_height() * 1.5))
		main_sound = pygame.mixer.Sound(os.path.join(PATH, 'audio/十面埋伏.mp3'))
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)

	def runTurn(self):
		self.turn += 1
		self.beforeTurn()
		self.midTurn()
		self.afterTurn()

	def update(self):
		self.window.fill(WATER_COLOR)
		self.window.blit(self.BG, (0, 0))
		self.window.blit(self.taichi, (0.5 * (WIDTH - self.taichi.get_width()), 100))
		line = self.titleFont.render("华山论剑第{}回".format(cn2an.an2cn(self.turn, "up")), True, pygame.Color(0, 0, 0, a = 0.7))
		self.window.blit(line, (0.5 * WIDTH - 0.5 * line.get_width() - 50, 20 ))
		patch = self.smallFont.render("版本号 2 - 5 - 2", True, pygame.Color(0, 0, 0, a = 0.7))
		self.window.blit(patch, (min(0.5 * WIDTH + 0.45 * line.get_width() -50, WIDTH - 200 - patch.get_width()) , line.get_rect().y + line.get_height() + 5))
		for place in self.places:
			place.showAt(place.screenPos)
		for champion in self.champions:
			champion.showBar()
			champion.showPlace()

	def reportLog(self):
		pass

	def showScreen(self):
		pygame.display.update()
		for i in range(5 * FPS):
			if util.getPygameKey() != '':
				break
			self.clock.tick(FPS)	