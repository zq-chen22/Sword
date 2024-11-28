import random
import pygame
from settings import *
import util
import numpy as np

class SkillShoot:
    def __init__(self, skill, **kwargs):
        self.skill = skill
        self.kwargs = kwargs

class Skill:
    def __init__(self):
        self.owner = None
        self.name = "default skill"
        self.button = None
        self.labels = []
        self.targets = []
        self.showTitle = "测试技能"

    def addLabels(self, *arg):
        for label in arg:
            self.labels.append(label)

    def hasLabels(self, label):
        if label in self.labels:
            return True
        return False

    def setName(self, newName):
        self.name = newName

    def setButton(self, newButton):
        self.button = newButton

    def setOwner(self, newOwner):
        self.owner = newOwner
    
    def cast(self, **kwarg):
        self.owner.property.skillAffects.append({"skill": SkillShoot(self, **kwarg), "affects": []})

    def isCastable(self):
        return self.isCastableOverStates()

    def isCastableOverStates(self):
        for state in self.owner.states:
            if not state.ownerCanCastSkill(self):
                return False
        return True
    
    def addAffect(self, affect):
        self.owner.property.skillAffects[-1]["affects"].append(affect)
        affect.setOwner(self.owner)
        affect.setOwnerSkill(self)

    def narration(self):
        return self.name
    
    def refresh(self):
        pass

    def switchPolicy(self, policy):
        pass

    def showAt(self, pos, **kwarg):
        WIN = pygame.display.get_surface()
        lines = []
        sideFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 35)
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
        charFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
        if self.isCastable():
            if self.owner.color == "Red":
                color = MAROON
                buttonColor = SALMON
            if self.owner.color == "Blue":
                color = MIDNIGHTBLUE
                buttonColor = SHALLOWBLUE
        else:
            color = IRON
            buttonColor = GRAY
        char = charFont.render(self.button,True, buttonColor)
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
        if "targets" in kwarg.keys():
            if len(kwarg["targets"]) != 0:
                side = sideFont.render(kwarg["targets"][0].cname, True, color)
                WIN.blit(side, (lines[-1][1][0] + lines[-1][0].get_width()-10, lines[-1][1][1] + lines[-1][0].get_height()-10))

    def showReportAt(self, pos, **kwarg):
        WIN = pygame.display.get_surface()
        lines = []
        sideFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 35)
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
        charFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
        if self.owner.color == "Red":
            color = MAROON
            buttonColor = SALMON
        if self.owner.color == "Blue":
            color = MIDNIGHTBLUE
            buttonColor = SHALLOWBLUE
        char = charFont.render(self.button,True, buttonColor)
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
        if "targets" in kwarg.keys():
            if len(kwarg["targets"]) != 0:
                side = sideFont.render(kwarg["targets"][0].cname, True, color)
                WIN.blit(side, (lines[-1][1][0] + lines[-1][0].get_width()-20, lines[-1][1][1] + lines[-1][0].get_height()-20))

class TargetSkill(Skill):
    def __init__(self):
        super().__init__()
        
        self.name = "target skill"
        self.getTarget = self.getRandomTarget
        self.addLabels("target")
    
    def allTargets(self):
        return None
    
    def getRandomTarget(self):
        target = random.choice(self.allTargets())
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target
    
    def getInputTarget(self):
        print(f"Now all possible targets of {self.owner.name}'s {self.name} are {[target.__str__() for target in self.allTargets()]}")
        index = int(input("Please input the index of your target place: "))
        for target in self.allTargets():
            if target.index == index:
                self.owner.token += str(index)
                self.owner.tokenIndex += 1
                self.targets.append(target)
                return target
        print("That's not a valid index.")
        return self.getInputTarget()

    def getTokenTarget(self):
        index = int(self.owner.token[self.owner.tokenIndex])
        self.owner.tokenIndex += 1
        for target in self.allTargets():
            if target.index == index:
                self.targets.append(target)
                return target
    
    def getMixTarget(self):
        if self.tokenIndex < len(self.token):
            return self.getTokenTarget()
        instruction = input("Please add some action token or input 'random' for random mode or 'input' for input mode.\n")
        if instruction == "random":
            self.getTarget = self.getRandomTarget
            return self.getTarget()
        if instruction == "input":
            self.getTarget = self.getInputTarget
            return self.getTarget()
        self.owner.token.append(instruction)
        return self.getTokenTarget()
    
    def showTargets(self):
        skillPos = np.array([0.5 * (WIDTH - 70 * len(self.allTargets())) + 50 , HEIGHT - 250])
        self.showAt(skillPos - np.array([int((len(self.showTitle)-1)/4) * 50 + 100, 0]))
        for button, target in enumerate(self.allTargets()):
            target.showTargetAt(skillPos, self.owner, button + 1)
            skillPos[0] += int((len(target.cname)-1)/4) * 50 + 70

    def getKeyTarget(self):
        self.owner.window.update()
        self.showTargets()
        pygame.display.update()

        instruction = ""
        while True:
            instruction = util.getPygameKey()
            if len(instruction) > 0:
                break
        button = instruction[0]
        for b, target in enumerate(self.allTargets()):
            if button == str(b + 1):
                self.owner.token += button
                self.owner.tokenIndex += 1
                self.targets.append(target)
                return target
        return self.getKeyTarget()

    def switchPolicy(self, policy):
        if policy == "random":
            self.getTarget = self.getRandomTarget
        if policy == "input":
            self.getTarget = self.getInputTarget
        if policy == "token":
            self.getTarget = self.getTokenTarget
        if policy == "mix":
            self.getTarget = self.getMixTarget
        if policy == "key":
            self.getTarget = self.getKeyTarget
        if policy == "soloAI":
            self.getTarget = self.getSoloAITarget

    def getSoloAITarget(self):
        pass

    def narration(self):
        nar = self.name
        for target in self.targets:
            nar += "-(" + target.name + ")"
        self.targets = []
        return nar

class GiveUp(Skill):
    def __init__(self):
        super().__init__()
        self.setName("End")
        self.addLabels("anyState")
        self.setButton(".")
        self.showTitle = "终结回合"