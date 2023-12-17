import skill
import champion
from affect_util import SplashHurt
import random

class Attack(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Auto Attack")
        self.setButton("A")

    def isCastable(self):
        if self.owner.isMovable:
            return True
        return False

    def cast(self):
        self.owner.isMovable = False
        SplashHurt(1, position = self.owner.position, owner = self.owner)

class Study(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Study")
        self.setButton("S")

    def isCastable(self):
        if self.owner.isMovable:
            return True
        return False

    def cast(self):
        self.owner.isMovable = False

class Move(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("Move")
        self.setButton("M")
        self.getTarget = self.getRandomTarget

    def allTargets(self):
        return self.owner.position.neighbors

    def isCastable(self):
        if self.owner.isMovable and self.allTargets() != []:
            return True
        return False

    def cast(self):
        self.getTarget().setChampion(self.owner)
        self.owner.isMovable = False

class Solder(champion.Champion):
    def __init__(self):
        super().__init__()
        self.health = 4
        self.maxHealth = 4
        self.title = "Solder"
        self.getSkills()
        self.isMovable = True

    def getSkills(self):
        self.getSkill(Attack())
        self.getSkill(Study())
        self.getSkill(Move())

    def beforeTurn(self, **kwarg):
        self.isMovable = True
        return super().beforeTurn(**kwarg)

