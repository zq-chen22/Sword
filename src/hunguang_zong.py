
import zong 
from hunguangSkill import *

class HunGuang(zong.JianZong):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.maxHealth = 5
        self.title = "HunGuangZong"

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
        nar += f". Now he has {self.skills[5].layer} stack(s) of Q"
        return nar


    