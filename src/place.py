import pygame
from settings import *

class Place:

    placeId = 0

    def __init__(self):
        Place.placeId += 1
        self.champions = []
        self.neighbors = []
        self.affects = []
        self.name = f"place{Place.placeId}"
        self.index = Place.placeId
        self.nextTurnAffects = []
        self.screenPos = None
        self.cname = f"地点{Place.placeId}"
        self.window = None
        self.placeImg = None
        self.showTitle = None
    
    def setName(self, name):
        self.name = name

    def setIndex(self, index):
        self.index = index

    def setChampion(self, champion):
        self.champions.append(champion)
        if champion.position:
            champion.position.removeChampion(champion)
        champion.setPosition(self)

    def removeChampion(self, champion):
        self.champions.remove(champion)

    def settle(self, priority = 4000):
        for affect in self.affects:
            # self.affects.remove(affect)
            if affect.priority <= priority:
                affect.settle()

    def newAffects(self):
        self.affects = self.nextTurnAffects
        self.nextTurnAffects = []

    def narration(self):
        narration = f"{self.index}.{self.name} with champions {[champion.name for champion in self.champions]}."
        return narration

    def showAt(self, pos = None):
        pass

    def __str__(self):
        return f"{self.index}.{self.name}"
    
    def placeImgInit(self):
        pass

    def showTargetAt(self, pos, champion, button):
        WIN = pygame.display.get_surface()
        lines = []
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
        charFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
        if champion.color == "Red":
            color = MAROON
            buttonColor = SALMON
        if champion.color == "Blue":
            color = MIDNIGHTBLUE
            buttonColor = SHALLOWBLUE
        char = charFont.render(str(button),True, buttonColor)
        WIN.blit(char, (pos[0]-10, pos[1]-40))
        for l in range(int((len(self.showTitle)+3)/4)):
            for i in range(4):
                if l * 4 + i + 1 > len(self.showTitle):
                    break
                char = font.render(self.showTitle[l*4 + i],True, color)
                if i == 0:
                    lines.append((char, (pos[0] + 50 * l, pos[1])))
                else:
                    lines.append((char, (lines[-1][1][0], lines[-1][0].get_height() + lines[-1][1][1])))
        for i in lines:
            WIN.blit(i[0], i[1])


