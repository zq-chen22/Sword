from game_ground import GameGround
from settings import *
import pygame
import util 
import cn2an

class GameWindow(GameGround):
	def __init__(self):
		super().__init__()
		pygame.init()
		self.window = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
		pygame.display.set_caption('Sword')

		self.clock = pygame.time.Clock()
		self.titleFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
		self.font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
		self.smallFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 32)

		self.BG = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'graphics', 'background', 'notebook.jpg')), (WIDTH, HEIGHT))

		main_sound = pygame.mixer.Sound('audio/十面埋伏.mp3')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)

	def runTurn(self):
		self.turn += 1
		self.beforeTurn()
		self.update()
		self.showScreen()
		self.midTurn()
		self.afterTurn()

	def update(self):
		self.window.fill(WATER_COLOR)
		self.window.blit(self.BG, (0, 0))
		line = self.titleFont.render("华山论剑第{}回".format(cn2an.an2cn(self.turn, "up")), True, pygame.Color(0, 0, 0, a = 0.7))
		self.window.blit(line, (0.5 * WIDTH - 0.5 * line.get_width() - 50, 20 ))
		patch = self.smallFont.render("版本号 2 - 5 - 2", True, pygame.Color(0, 0, 0, a = 0.7))
		self.window.blit(patch, (0.5 * WIDTH + 0.45 * line.get_width() -50 , line.get_rect().y + line.get_height() + 5))
		# for i in range(int(len(self.narration())/40)):
		# 	line = self.font.render(self.narration()[40 * i: min(40 * i + 40, len(self.narration()) - 1)], True, pygame.Color(0, 0, 0, a = 0.7))
		# 	self.window.blit(line, (50, 50 * ( i + 3 )))
		self.champions[0].showSkills()

	def reportLog(self):
		pass

	def showScreen(self):
		pygame.display.update()
		for i in range(5 * FPS):
			if util.getPygameKey() != '':
				break
			self.clock.tick(FPS)





		