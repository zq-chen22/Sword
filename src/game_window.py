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
		self.skillList = None
		pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
		pygame.display.set_caption('华山论剑2.5.2')

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

	def skillListInit(self):
		self.skillList = {champion: [] for champion in self.champions}

	def midTurn(self):
		for champion in self.champions:
			champion.midTurn(log = self.motionLog, skillList = self.skillList)

	def beforeTurn(self):
		super().beforeTurn()
		self.skillListInit()

	def runTurn(self):
		self.turn += 1
		self.beforeTurn()
		self.midTurn()
		self.afterTurn()
		if self.checkWin():
			exit()

	def update(self):
		self.reArrangeShowPosition()
		WIN = pygame.display.get_surface()
		WIN.fill(WATER_COLOR)
		WIN.blit(self.BG, (0, 0))
		WIN.blit(self.taichi, (0.5 * (WIDTH - self.taichi.get_width()), 100))
		line = self.titleFont.render("华山论剑第{}回".format(cn2an.an2cn(self.turn, "up")), True, BLACK)
		WIN.blit(line, (0.5 * WIDTH - 0.5 * line.get_width() - 50, 20 ))
		patch = self.smallFont.render("版本号 2 - 5 - 2", True, BLACK)
		WIN.blit(patch, (min(0.5 * WIDTH + 0.45 * line.get_width() -50, WIDTH - 200 - patch.get_width()) , line.get_rect().y + line.get_height() + 5))
		for place in self.places:
			place.showAt(place.screenPos)
		for champion in self.champions:
			champion.showBar()
			champion.showPlace()

	def freshScreen(self):
		frame_id = 0
		while True:
			frame_id += 1
			self.update()
			for champion in self.champions:
				champion.reportSkills(self.skillList[champion])
				champion.playSkillAtFrame(self.skillList[champion], frame_id)
			self.showScreen()
			pygame.display.update()
			if util.getPygameKey() != '':
				break
			pygame.time.Clock().tick(FPS)

	def reportLog(self):
		self.freshScreen()
		for champion in self.champions:
			champion.reportSkills(self.skillList[champion])

	def showScreen(self):
		WIN = pygame.display.get_surface()
		sideFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 35)
		font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
		charFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
		if self.gameover:
			line = font.render("决斗结束 按任意键退出……",True, BLACK)
		if not self.gameover:
			line = font.render("回合结束 按任意键继续……",True, BLACK)
		WIN.blit(line, (0.5 * WIDTH - 0.5 * line.get_width(), HEIGHT - 50 - line.get_height()))

	def checkWin(self):
		if (self.champions[0].isSurvive() and self.champions[1].isSurvive()):
			return False
		WIN = pygame.display.get_surface()
		gigaFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 100)
		color = BLACK
		if self.champions[0].isSurvive() and not self.champions[1].isSurvive():
			if self.champions[0].color == "Blue": color = DEEPBLUE
			if self.champions[0].color == "Red": color = FIREBRICK
			line = gigaFont.render("胜利",True, color)
		if self.champions[1].isSurvive() and not self.champions[0].isSurvive():
			if self.champions[1].color == "Blue": color = DEEPBLUE
			if self.champions[1].color == "Red": color = FIREBRICK
			line = gigaFont.render("失败",True, color)
		if not self.champions[1].isSurvive() and not self.champions[0].isSurvive():
			color = BLACK
			line = gigaFont.render("平局",True, color)
		WIN.blit(line, (0.5 * WIDTH - 0.5 * line.get_width(), 180))
		self.gameover = True
		return True

	def reArrangeShowPosition(self):
		showPositions = ["Left", "Right", ]
		for ind, champion in enumerate(sorted(self.champions, key = lambda champion: champion.screenPos[0])):
			champion.showPosition = showPositions[ind]
