# The zong champions.
import skill
from champion import Champion
from affect_util import SplashHurt
import random

logPath = r"C:\Users\86137\Desktop\log.txt"

class JianZongAttack(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("Auto Attack")
        self.setButton("A")

    def isCastable(self):
        if self.owner.isMovable and self.owner.hasSword and self.owner.endurance > 0 and self.allTargets() != []:
            return True
        return False

    def cast(self):
        target = self.getTarget()
        if target != self.owner.position:
            self.owner.hasSword = False
            self.owner.swordPosition = target
        SplashHurt(1, position = target, owner = self.owner)
        self.owner.isMovable = False
    
    def allTargets(self):
        return self.owner.position.neighbors

class JianZongStudy(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Study")
        self.setButton("S")

    def isCastable(self):
        if self.owner.isMovable:
            return True
        return False

    def cast(self):
        self.owner.refresh()
        self.owner.isMovable = False

class JianZongMove(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("Move")
        self.setButton("M")
        self.getTarget = self.getRandomTarget

    def allTargets(self):
        return self.owner.position.neighbors

    def isCastable(self):
        if self.owner.isMovable and self.allTargets() != [] and self.owner.endurance > 0:
            return True
        return False
    
    def cast(self):
        target = self.getTarget()
        target.setChampion(self.owner)
        if not self.owner.hasSword and self.owner.swordPosition == target:
            self.owner.hasSword = True
        self.owner.isMovable = False

class JianZong(Champion):
    def __init__(self):
        super().__init__()
        self.health = 4
        self.maxHealth = 4
        self.title = "JianZong"
        self.endurance = 3
        self.maxEndurance = 3
        self.isMovable = False
        self.hasSword = True
        self.swordPosition = self.position
        self.ctitle = "剑宗"

    def getSkills(self):
        self.getSkill(JianZongAttack())
        self.getSkill(JianZongStudy())
        self.getSkill(JianZongMove())

    def refresh(self):
        self.endurance = self.maxEndurance
        for skill in self.skills:
            skill.refresh()

    def setPosition(self, position):
        if self.hasSword:
            self.swordPosition = position
        return super().setPosition(position)
    
    def narration(self):
        nar = f"one {self.title} named {self.name} at {self.position.name} with health {self.health}/{self.maxHealth}, endurance {self.endurance}/{self.maxEndurance} and {len(self.states)} states"
        for state in self.states:
            nar += ", " + state.narration()
        nar += f". His sword is "
        if not self.hasSword:
            nar += "not "
        nar += "in hand now"
        return nar

    def beforeTurn(self, **kwarg):
        super().beforeTurn(**kwarg)
        self.isMovable = True

    def recoverEndurance(self, endurance):
        self.endurance = min(self.endurance + endurance, self.maxEndurance)