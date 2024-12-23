
import zong 
from hunguangSkill import *
from settings import *
import util
import pygame
import numpy as np
import random

class HunGuang(zong.JianZong):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.maxHealth = 5
        self.title = "HunGuangZong"
        self.ctitle = "浑光宗"

    def getSkills(self):
        self.getSkill(HunGuangAttack())
        self.getSkill(HunGuangStudy())
        self.getSkill(HunGuangMove())
        self.getSkill(HunGuangGetSword())
        self.getSkill(HunGuangQ1())
        self.getSkill(HunGuangQ2())
        self.getSkill(HunGuangW())
        self.getSkill(HunGuangE())
        self.getSkill(HunGuangR1())
        self.getSkill(HunGuangR2())
        self.getSkill(HunGuangShunQian())
        self.getSkill(skill.GiveUp())

    def refresh(self):
        self.endurance = self.maxEndurance
        for skill in self.skills:
            skill.refresh()

    def setPosition(self, position):
        if self.hasSword:
            self.swordPosition = position
        return super().setPosition(position)
        
    def beforeTurn(self, **kwarg):
        self.isMovable = True
        return super().beforeTurn(**kwarg)
    
    def realDamagePasitiveActivateFunc(self):
        if "realDamagePasitive" not in map(lambda state: state.name, self.states + self.nextTurnStates):
            self.getState(HunGuangRealDamagePassitive())
    
    def freeQPasitiveActivateFunc(self):
        self.getState(HunGuangFreeQPassitive())

    def narration(self):
        nar = super().narration()
        nar += f". Now he has {self.peepSkill('Q-2').layer} stack(s) of Q"
        return nar

    def showStates(self, pos):
        WIN = pygame.display.get_surface()
        font1 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 35)
        font2 = pygame.font.Font(os.path.join(PATH, "fonts", "毛笔书法字体(启功体)繁启体.TTF"), 25)
        state_pos = pos
        state_title = font1.render("体力", True, BLACK)
        if self.showPosition == "Left":
            WIN.blit(state_title, state_pos) 
        if self.showPosition == "Right":
            WIN.blit(state_title, np.array((WIDTH - state_title.get_width(), 0)) - np.array((1, -1)) * state_pos) 
        state_subtitle = font2.render(f"×{self.endurance}", True, BLACK)
        if self.showPosition == "Left":
            WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
        if self.showPosition == "Right":
            WIN.blit(state_subtitle, np.array((WIDTH - state_subtitle.get_width(), 0)) - np.array((1, -1)) * np.array((state_pos[0] - 20, state_pos[1] + state_title.get_height() - 20)))
        state_pos = (state_pos[0], state_pos[1] + state_title.get_height())
        state_title = font1.render("浑光", True, BLACK)
        if self.showPosition == "Left":
            WIN.blit(state_title, state_pos) 
        if self.showPosition == "Right":
            WIN.blit(state_title, np.array((WIDTH - state_title.get_width(), 0)) - np.array((1, -1)) * state_pos)
        state_subtitle = font2.render(f"×{self.peepSkill('Q-2').layer}", True, BLACK)
        if self.showPosition == "Left":
            WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
        if self.showPosition == "Right":
            WIN.blit(state_subtitle, np.array((WIDTH - state_subtitle.get_width(), 0)) - np.array((1, -1)) * np.array((state_pos[0] - 20, state_pos[1] + state_title.get_height() - 20)))
        state_pos = (state_pos[0], state_pos[1] + state_title.get_height())
        if self.hasSword:
            state_title = font1.render("持剑", True, BLACK)
            if self.showPosition == "Left":
                WIN.blit(state_title, state_pos) 
            if self.showPosition == "Right":
                WIN.blit(state_title, np.array((WIDTH - state_title.get_width(), 0)) - np.array((1, -1)) * state_pos)
            # state_subtitle = font2.render(f"×{self.endurance}", True, BLACK)
            # WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
            state_pos = (state_pos[0], state_pos[1] + state_title.get_height())
        else:
            state_title = font1.render("无剑", True, BLACK)
            if self.showPosition == "Left":
                WIN.blit(state_title, state_pos) 
            if self.showPosition == "Right":
                WIN.blit(state_title, np.array((WIDTH - state_title.get_width(), 0)) - np.array((1, -1)) * state_pos)
            state_subtitle = font2.render(f" {self.swordPosition.cname}", True, BLACK)
            if self.showPosition == "Left":
                WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
            if self.showPosition == "Right":
                WIN.blit(state_subtitle, np.array((WIDTH - state_subtitle.get_width(), 0)) - np.array((1, -1)) * np.array((state_pos[0] - 20
                                                                                                                           , state_pos[1] + state_title.get_height() - 20)))
            state_pos = (state_pos[0], state_pos[1] + state_title.get_height())
        super().showStates(state_pos)
            # for state in self.states:
            #     if state.visiable:
            #         state_title = font1.render(state.cname, True, BLACK)
            #         WIN.blit(state_title, state_pos) 
            #         if state.getCsubname() is not None:
            #             state_subtitle = font2.render(state.getCsubname(), True, BLACK)
            #             WIN.blit(state_subtitle, (state_pos[0] + state_title.get_width() - 15, state_pos[1] + state_title.get_height() - 20))
            #         state_pos = (state_pos[0], state_pos[1] + state_title.get_height())
    
    def chooseSkillSoloAI(self):
        # Q start
        # W/move/set a new Q
        castableSkillsButtons = [skill.button for skill in self.castableSkills()]
        castableSkillsNames = [skill.name for skill in self.castableSkills()]
        button = None
        if "R-2" in castableSkillsNames and button is None:
            if random.uniform(0., 1.) < 0.5 + 0.4 * (self.peepState("onSky").duration == 0):
                button = "R"
        if "E" in castableSkillsButtons and button is None:
            if random.uniform(0., 1.) < (0.1 + \
                0.3 * (self.position.index == self.enemy.positionLastFrame.index) * \
                    (self.positionLastFrame.index == self.enemy.positionLastFrame.index)) / (self.endurance ** 2):
                button = "E"
        if "Q-1" in castableSkillsNames and button is None:
            if random.uniform(0., 1.) < 1.0 - 0.3 * (self.position.index == self.enemy.positionLastFrame.index):
                button = "Q"
        elif "Q-2" in castableSkillsNames and button is None:
            if random.uniform(0., 1.) < 0.25 + 0.5 * (self.position.index == self.enemy.positionLastFrame.index) - 0.25 * (self.positionLastFrame.index == self.enemy.positionLastFrame.index):
                button = "Q"
            elif self.peepState("hoistSword").duration == 0 and not self.isMovable:
                button = "Q"
        if button is None:
            weight = {}
            if self.isMovable:
                if "W" in castableSkillsButtons and "Q-2" in castableSkillsNames: weight["W"] = 1
                if "M" in castableSkillsButtons and self.position.index != self.enemy.positionLastFrame.index: weight["M"] = 2
                if "S" in castableSkillsButtons and self.peepSkill("Q-2").layer == 1 and (self.maxEndurance - self.endurance) > 0: 
                    weight["S"] = self.maxEndurance - self.endurance
                if "S" in castableSkillsButtons and self.endurance == 0: weight["S"] = 3
                if "R-1" in castableSkillsNames: 
                    weight["R"] = (2 * self.peepSkill("Q-2").layer - 1)/(self.endurance + 1) ** 2
                    if self.position.index == self.enemy.positionLastFrame.index: weight["R"] *= 2
            if len(weight) > 0:
                sum = 0.
                for key in weight:
                    sum += weight[key]
                pointer = sum * random.uniform(0., 1.)
                summer = 0.
                for key in weight:
                    if summer <= pointer < summer + weight[key]: 
                        button = key
                        break
                    summer += weight[key]
        if button is None: button = "."
        for skill in self.castableSkills():
            if button.isalpha():
                if button in (skill.button.upper(), skill.button.lower()):
                    self.token += skill.button
                    self.tokenIndex += 1
                    return skill
            elif button == skill.button:
                self.token += button
                self.tokenIndex += 1
                return skill
    