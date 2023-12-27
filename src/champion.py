# The champions manipulated by people.
import random
from settings import *
import pygame
import cv2
import numpy as np
import util

class InTurnProperty:
    def __init__(self):
        self.isHit = False
        self.isHurt = False
        self.isControled = False
        self.skillAffects = []
        self.expectedDamage = 0

class Champion:

    championId = 0

    healthImg = cv2.imread(os.path.join(PATH, "graphics", "property", "dot.jpg"))
    healthImg = cv2.cvtColor(healthImg, cv2.COLOR_BGR2BGRA)
    healthImg[np.linalg.norm(healthImg[:, :, :]/255, axis = 2) ** 2 > 2.8, 3] = 0
    
    def __init__(self):
        Champion.championId += 1
        self.position = None
        self.health = None
        self.skills = []
        self.states = []
        self.name = None
        self.policy = None
        self.maxHealth = None
        self.hasUtimate = True
        self.title = "DefaultChampion"
        if self.name is None:
            self.name = f"champion{Champion.championId}"
        self.setIdAsGroup()
        self.setPolicy("random")
        self.chooseSkillFunc = self.chooseSkillRandom
        self.getSkills()
        self.token = ""
        self.tokenIndex = 0
        self.nextTurnStates = []
        self.property = InTurnProperty()
        self.propertyHistory = []
        self.state = "beforeTurn"
        self.showPosition = None
        self.ctitle = "无宗门"
        self.cname = None
        self.color = None
        self.screenPos =  None
        self.window = None
        self.healthSample = None
        self.emptyHealthSample = None
        self.figureImg = None
        # self.window = WindowProperty()

    def narration(self):
        nar = f"one {self.title} named {self.name} at {self.position.name} with health {self.health}/{self.maxHealth} and {len(self.states)} states"
        for state in self.states:
            nar += ", " + state.narration()
        return nar

    def setPosition(self, position):
        self.position = position
        self.updateScreenPos()

    def setName(self, name):
        self.name = name

    def setGroup(self, group):
        self.group = group

    def setIdAsGroup(self):
        self.group = self.championId

    def settleAllState(self, priority = 4000):
        for state in sorted(self.states, key = lambda state: state.priority):
            if state.priority <= priority:
                state.settle()

    def newStates(self):
        self.states = self.nextTurnStates
        self.nextTurnStates = []
    
    def getSkill(self, skill):
        self.skills.append(skill)
        skill.setOwner(self)

    def castSkill(self, skill):
        skill.cast()

    def canCastSkill(self, skill):
        for state in self.states:
            if not state.ownerCanCastSkill(skill):
                return False
        return skill in self.skills and skill.isCastable()

    def castableSkills(self):
        castableSkills = []
        for skill in self.skills:
            if self.canCastSkill(skill):
                castableSkills.append(skill)
        return castableSkills

    def getState(self, state):
        self.states.append(state)
        state.setOwner(self)

    def getNextTurnState(self, state):
        self.nextTurnStates.append(state)
        state.setOwner(self)

    def beforeTurn(self, **kwarg):
        self.state = "beforeTurn"
        self.propertyHistory.append(self.property)
        self.property = InTurnProperty()

    def afterTurn(self, **kwarg):
        self.state = "afterTurn"
        self.settleAllState(**kwarg)

    def __str__(self):
        return self.title + " " + self.name

    def isSurvive(self):
        if self.health > 0:
            return True
        return False 
    
    def setPolicy(self, policy, **kwarg):
        self.policy = policy
        for skill in self.skills:
            skill.switchPolicy(policy)
        if policy == "random":
            self.chooseSkillFunc = self.chooseSkillRandom
        if policy == "input":
            self.chooseSkillFunc = self.chooseSkillInput
        if policy == "token":
            self.chooseSkillFunc = self.chooseSkillToken
            self.token = kwarg['token']
        if policy == "mix":
            self.chooseSkillFunc = self.chooseSkillMix
            if 'token' in kwarg.keys():
                self.token = kwarg['token']
        if policy == "key":
            self.chooseSkillFunc = self.chooseSkillKey


    def midTurn(self, **kwarg):
        self.state = "midTurn"
        if "log" in kwarg.keys():
            kwarg["log"][-1] += f"{self.title} {self.name} chooses to take the following moves.\n"
        while self.castableSkills() != []:
            choosedSkill = self.chooseSkillFunc()
            if choosedSkill.button == ".":
                break
            self.castSkill(choosedSkill)
            if "log" in kwarg.keys():
                kwarg["log"][-1] += choosedSkill.narration()
                kwarg["log"][-1] += ","
        if "log" in kwarg.keys():
            kwarg["log"][-1] += "\n"
        if self.policy == "token":
            self.tokenIndex += 1
        else:
            self.tokenIndex += 1
            self.token += " "

    def chooseSkillRandom(self):
        skill = random.choice(self.castableSkills())
        button = skill.button
        self.token += button
        self.tokenIndex += 1
        return skill
  
    def chooseSkillInput(self): 
        print(f"Now all skills {self.name} can use are {[skill.button + '.' + skill.name for skill in self.castableSkills()]}")
        button = input("Please input the button of your target skill: ")
        for skill in self.castableSkills():
            if skill.button == button:
                self.token += button
                self.tokenIndex += 1
                return skill
        print("invalid skill.")
        return self.chooseSkillInput()

    def chooseSkillToken(self):
        button = self.token[self.tokenIndex]
        for skill in self.castableSkills():
            if skill.button == button:
                self.tokenIndex += 1
                return skill
        return None
    
    def chooseSkillMix(self):
        if self.tokenIndex < len(self.token):
            return self.chooseSkillToken()
        instruction = input("Please add some action token or input 'random' for random mode or 'input' for input mode.\n")
        if instruction == "random":
            self.chooseSkillFunc = self.chooseSkillRandom
            return self.chooseSkillFunc()
        if instruction == "input":
            self.chooseSkillFunc = self.chooseSkillInput
            return self.chooseSkillFunc()
        self.token.append(instruction)
        return self.chooseSkillToken()
    
    def chooseSkillKey(self):
        self.window.update()
        self.showSkills()
        pygame.display.update()
        instruction = ""
        while True:
            instruction = util.getPygameKey()
            if len(instruction) > 0:
                break
        button = instruction[0]
        for skill in self.castableSkills():
            if button.isalpha():
                if button in (skill.button.upper(), skill.button.lower()):
                    self.token += button
                    self.tokenIndex += 1
                    return skill
            elif button == skill.button:
                self.token += button
                self.tokenIndex += 1
                return skill
        return self.chooseSkillKey()
        
    def hasState(self, stateName):
        for state in self.states:
            if state.name == stateName:
                return True
        return False

    # window display attributes
    def showSkills(self):
        buttonDict = {}
        for skill in self.skills:
            if skill.button in buttonDict.keys():
                buttonDict[skill.button].append(skill)
            else:
                buttonDict[skill.button] = [skill]
        skillPos = [0.5 * (WIDTH - 70 * len(buttonDict.keys())) + 50 , HEIGHT - 250]
        
        pos = (skillPos[0]-70, skillPos[1])
        WIN = pygame.display.get_surface()
        lines = []
        font = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
        charFont = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 70)
        if self.color == "Red":
            color = MAROON
            buttonColor = SALMON
        if self.color == "Blue":
            color = MIDNIGHTBLUE
            buttonColor = SHALLOWBLUE
        if self.state == "beforeTurn":
            title = "初"
        elif self.state == "midTurn":
            title = "中"
        elif self.state == "afterTurn":
            title = "末"
        title = f"回合{title}"
        char = charFont.render("*",True, buttonColor)
        WIN.blit(char, (pos[0]+15, pos[1]-40))
        for l in range(int((len(title)+4)/5)):
            for i in range(5):
                if l * 4 + i + 1 > len(title):
                    break
                char = font.render(title[l*4 + i],True, color)
                if i == 0:
                    lines.append((char, (pos[0] + 50 * l, pos[1])))
                else:
                    lines.append((char, (lines[-1][1][0], lines[-1][0].get_height() + lines[-1][1][1])))
        for i in lines:
            WIN.blit(i[0], i[1])

        for i, k in enumerate(buttonDict.keys()):
            isActive = False
            for skill in buttonDict[k]:
                if skill.isCastable():
                    skill.showAt(skillPos)
                    isActive = True
                    break
            if not isActive:
                buttonDict[k][0].showAt(skillPos)
            skillPos[0] += int((len(skill.showTitle)-1)/4) * 50 + 70

    
    def showStates(self, pos):
        WIN = pygame.display.get_surface()
        font1 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 35)
        font2 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 25)
        state_pos = pos
        for state in self.states:
            if state.visiable:
                state_title = font1.render(state.cname, True, BLACK)
                if self.showPosition == "Left":
                    WIN.blit(state_title, state_pos) 
                if self.showPosition == "Right":
                    WIN.blit(state_title, np.array((WIDTH - state_title.get_width(), 0)) - np.array((1, -1)) * state_pos) 
                if state.getCsubname() is not None:
                    state_subtitle = font2.render(state.getCsubname(), True, BLACK)
                    if self.showPosition == "Left":
                        WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
                    if self.showPosition == "Right":
                        WIN.blit(state_subtitle, np.array((WIDTH - state_subtitle.get_width(), 0)) - np.array((1, -1)) * np.array((state_pos[0] - 20, state_pos[1] + state_title.get_height() - 20)))
                state_pos = (state_pos[0], state_pos[1] + state_title.get_height())

    def figureImgInit(self):
        if self.color == "Blue":
            color = util.hex_to_bgr(DEEPBLUE)
        if self.color == "Red":
            color = util.hex_to_bgr(FIREBRICK)
        img = cv2.imread(os.path.join(PATH, "graphics", "property", "cross.jpg"))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        new_img = img.copy()
        new_img[:, :, 3] = 255 * np.linalg.norm(1 - img[:, :, :]/255, axis = 2)/np.max(np.linalg.norm(1 - img[:, :, :]/255, axis = 2))
        new_img[np.linalg.norm(img[:, :, :]/255, axis = 2) ** 2 > 2.8, 3] = 0
        new_img[:, :, :3] = np.array(color)
        cross = pygame.image.frombuffer(new_img.tostring(), new_img.shape[1::-1], "BGRA")
        self.figureImg = pygame.transform.scale(cross, (120, 120 * cross.get_height() / cross.get_width()))

    def showPlace(self):
        WIN = pygame.display.get_surface()
        if self.figureImg is None:
            self.figureImgInit()
        WIN.blit(self.figureImg, self.screenPos)

    def updateScreenPos(self):
        self.screenPos = np.array(self.position.screenPos) + 100 * np.random.random((2,))

    def healthSampleInit(self):
        if self.color == "Blue":
            color = util.hex_to_bgr(DEEPBLUE)
        if self.color == "Red":
            color = util.hex_to_bgr(FIREBRICK)
        healthImg = self.healthImg.copy()
        healthImg[:, :, :3] = np.floor(255 - (1-self.healthImg[:, :, :3]/255) * (255 - np.array(color)))
        health_sample = pygame.image.frombuffer(healthImg.tostring(), healthImg.shape[1::-1], "BGRA")
        self.healthSample = pygame.transform.scale(health_sample, (40, 40 * health_sample.get_height() / health_sample.get_width()))

    def emptyHealthSampleInit(self):
        color = util.hex_to_bgr(GRAY)
        healthImg = self.healthImg.copy()
        healthImg[:, :, :3] = np.floor(255 - (1-self.healthImg[:, :, :3]/255) * (255 - np.array(color)))
        health_sample = pygame.image.frombuffer(healthImg.tostring(), healthImg.shape[1::-1], "BGRA")
        self.emptyHealthSample = pygame.transform.scale(health_sample, (40, 40 * health_sample.get_height() / health_sample.get_width()))

    def showHealth(self, pos):
        WIN = pygame.display.get_surface()
        dot_pos = pos
        for i in range(self.maxHealth):
            if i < self.health:
                if self.healthSample is None:
                    self.healthSampleInit()
                health_sample = self.healthSample
            else:
                if self.emptyHealthSample is None:
                    self.emptyHealthSampleInit()
                health_sample = self.emptyHealthSample
            if self.showPosition == "Left":
                WIN.blit(health_sample, dot_pos)
            if self.showPosition == "Right":
                WIN.blit(health_sample, np.array((WIDTH - health_sample.get_width(), 0)) - np.array((1, -1)) * dot_pos)
            dot_pos = (dot_pos[0], dot_pos[1] + health_sample.get_height() + 10)

    def showBar(self):
        WIN = pygame.display.get_surface()
        font1 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 40)
        font2 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 50)
        if self.color == "Red":
            color = MAROON
        if self.color == "Blue":
            color = MIDNIGHTBLUE
        title = font1.render(self.ctitle, True, BLACK)
        pos = np.array((50, 100))
        title_pos = pos
        name = font2.render(self.cname, True, color)
        name_pos = pos + title.get_height()
        self.showHealth((pos[0], pos[1] + 2 * title.get_height()))
        self.showStates((pos[0] + 1.5 * title.get_height(), pos[1] + 2.5 * title.get_height()))
        if self.showPosition == "Left":
            WIN.blit(title, title_pos)
            WIN.blit(name, name_pos)
        if self.showPosition == "Right":
            WIN.blit(title, np.array((WIDTH - title.get_width(), 0)) - np.array((1, -1)) * title_pos)
            WIN.blit(name, np.array((WIDTH - name.get_width(), 0)) - np.array((1, -1)) * name_pos)
               
if __name__ == "__main__":
    x = Champion()
    y = Champion()
    z = Champion()
    t = Champion()
    print(x.canCastSkill(1))
    print(x.group)
    print(y.group)
    print(z.group)
    print(t.group)
