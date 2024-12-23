import skill
# import random
from hunguangState import *
import affect
import affect_util
from hunguangAffect import *
import random

class HunGuangAttack(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("Auto Attack")
        self.setButton("A")
        self.addLabels("hurt")
        self.showTitle = "剑击"
        
    def isCastable(self):
        if super().isCastable() and self.owner.isMovable and self.owner.hasSword and self.owner.endurance > 0 and self.allTargets() != []:
            return True
        return False

    def cast(self):
        super().cast()
        target = self.getTarget()
        hurt = 1
        withPasitive = False
        if target != self.owner.position:
            self.owner.hasSword = False
            self.owner.swordPosition = target
        for state in self.owner.states:
            if state.name == "realDamagePasitive":
                withPasitive = True
                self.owner.states.remove(state)
        if withPasitive:
            if target == self.owner.position:
                self.addAffect(affect_util.RealSplashHurt(hurt, position = target, owner = self.owner))
            else:
                self.addAffect(affect_util.RealSplashHurt(hurt, position = target, owner = self.owner, hitActivatedFunctions = [self.owner.freeQPasitiveActivateFunc]))
        else:
            self.addAffect(affect_util.SplashHurt(hurt, position = target, owner = self.owner))
        self.owner.isMovable = False
    
    def getSoloAITarget(self):
        if self.owner.enemy.positionLastFrame not in self.allTargets(): return self.getRandomTarget()
        target = self.owner.enemy.positionLastFrame
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target

    def allTargets(self):
        return self.owner.position.neighbors

class HunGuangGetSword(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Get Sword")
        self.setButton("A")
        self.showTitle = "召剑"

    def isCastable(self):
        if super().isCastable() and self.owner.isMovable and not self.owner.hasSword:
            return True
        return False

    def cast(self):
        super().cast()
        self.owner.swordPosition = self.owner.position
        for state in self.owner.states:
            if state.name == "freeQPasitive":
                self.owner.states.remove(state)
        self.owner.hasSword = True
        self.owner.isMovable = False

class HunGuangStudy(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Study")
        self.setButton("S")
        self.showTitle = "冥想"

    def isCastable(self):
        if super().isCastable() and self.owner.isMovable:
            return True
        return False

    def cast(self):
        super().cast()
        self.owner.refresh()
        self.owner.isMovable = False

class HunGuangMove(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("Move")
        self.setButton("M")
        self.addLabels("move")
        self.getTarget = self.getRandomTarget
        self.showTitle = "驰越"

    def allTargets(self):
        return self.owner.position.neighbors

    def isCastable(self):
        if super().isCastable() and self.owner.isMovable and self.allTargets() != [] and (self.owner.endurance > 0 or self.owner.hasState("hoistSword")):
            return True
        return False
    
    def getSoloAITarget(self):
        if self.owner.enemy.positionLastFrame not in self.allTargets(): return self.getRandomTarget()
        target = self.owner.enemy.positionLastFrame
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target
    
    def cast(self):
        super().cast()
        target = self.getTarget()
        target.setChampion(self.owner)
        if not self.owner.hasSword and self.owner.swordPosition == target:
            for state in self.owner.states:
                if state.name == "freeQPasitive":
                    self.owner.getState(HunGuangHoistSword(owner = self.owner))
                    self.owner.states.remove(state)
            self.owner.hasSword = True
        self.owner.isMovable = False

class HunGuangQ1(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Q-1")
        self.setButton("Q")
        self.addLabels("spell")
        self.showTitle = "浑光起"

    def isCastable(self):
        if super().isCastable() and self.owner.hasSword and self.owner.endurance > 0 and self.owner.isMovable and not self.owner.hasState("hoistSword"):
            return True
        return False
    
    def cast(self):
        super().cast()
        self.owner.endurance -= 1
        self.owner.getState(HunGuangHoistSword(owner = self.owner))
        self.owner.isMovable = False

class HunGuangQ2(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("Q-2")
        self.setButton("Q")
        self.addLabels("hurt" ,"spell")
        self.layer = 1
        self.showTitle = "浑光坠"

    def isCastable(self):
        if super().isCastable() and self.owner.hasSword and self.owner.hasState("hoistSword"):
            return True
        return False
    
    def addLayer(self):
        self.layer += 1

    def refresh(self):
        self.layer = 1

    def cast(self):
        super().cast(endurance = 1)
        hurt = self.layer
        for state in self.owner.states:
            if state.name == "hoistSword":
                state.remove()
        self.addAffect(affect_util.SplashHurt(hurt, position = self.owner.position, owner = self.owner, ownerSkill = self))
        self.addAffect(HunGuangRealDamagePasitiveFeedback(position = self.owner.position, owner = self.owner, ownerSkill = self))
        self.addAffect(HunGuangAddQLayerFeedback(position = self.owner.position, owner = self.owner, ownerSkill = self))

class HunGuangW(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("W")
        self.setButton("W")
        self.addLabels("spell")
        self.showTitle = "和尘术"

    def isCastable(self):
        if super().isCastable() and self.owner.hasSword and self.owner.endurance > 0 and self.owner.isMovable and not self.owner.hasState("heChen"):
            return True
        return False
    
    def cast(self):
        super().cast(endurance = 1)
        self.owner.endurance -= 1
        self.owner.getState(HunGuangHeChen())
        self.owner.isMovable = False

class HunGuangE(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("E")
        self.setButton("E")
        self.addLabels("hurt", "spell")
        self.canUse = True
        self.showTitle = "横扫千军"

    def isCastable(self):
        if super().isCastable() and self.owner.hasSword and self.owner.endurance > 0 and self.owner.isMovable and self.canUse:
            return True
        return False
    
    def cast(self):
        super().cast(endurance = self.owner.endurance)
        self.owner.getState(HunGuangSweepSword(endurance = self.owner.endurance))
        self.owner.getState(state_util.Invincible(duration = 0))
        self.addAffect(HunGuangRealDamagePasitiveFeedback(position = self.owner.position, owner = self.owner, ownerSkill = self))
        self.owner.endurance = 0
        self.owner.isMovable = False
        self.canUse = False

    def refresh(self):
        self.canUse = True

class HunGuangR1(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("R-1")
        self.setButton("R")
        self.addLabels("spell", "move")
        self.getTarget = self.getRandomTarget
        self.showTitle = "神兵无影"

    def isCastable(self):
        if super().isCastable() and self.owner.hasSword and self.owner.isMovable and self.owner.hasUtimate and not self.owner.hasState("hoistSword") and self.allTargets() != []:
            return True
        return False
    
    def cast(self):
        super().cast()
        destination = self.getTarget()
        hunGuangForceMove = HunGuangForceMove(destination = destination, position =self.owner.position)
        self.addAffect(hunGuangForceMove)
        self.owner.endurance = self.owner.maxEndurance
        self.owner.getState(HunGuangOnSky(owner= self.owner, poisoners = hunGuangForceMove.getTargets()))
        destination.setChampion(self.owner)
        self.owner.isMovable = False
        self.owner.hasUtimate = False

    def allTargets(self):
        return self.owner.position.neighbors

    def getSoloAITarget(self):
        other_targets = []
        for skillAffect in self.owner.property.skillAffects:
            if 'hurt' in skillAffect["skill"].skill.labels:
                target = self.owner.position
                self.owner.token += str(target.index)
                self.owner.tokenIndex += 1
                return target
        for target in self.allTargets():
            if target.index != self.owner.position.index: other_targets.append(target)
        if len(other_targets) == 0: return self.getRandomTarget()
        target = random.choice(other_targets)
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target

class HunGuangR2(skill.Skill):
    def __init__(self):
        super().__init__()
        self.setName("R-2")
        self.setButton("R")
        self.addLabels("spell")
        self.showTitle = "神兵天降"

    def isCastable(self):
        if super().isCastable() and self.owner.hasState("onSky"):
            for state in self.owner.states:
                if state.name == "onSky":
                    if state.duration == 2:
                        return False
            return True
        return False
    
    def cast(self):
        super().cast()
        hurt = round(0.3 * (self.owner.maxHealth - self.owner.health))
        for state in self.owner.states:
            if state.name == "onSky":
                state.remove()
        self.addAffect(affect_util.SplashHurt(damage = hurt, position = self.owner.position, owner = self.owner, ownerSkill = self))
        self.addAffect(HunGuangRealDamagePasitiveFeedback(position = self.owner.position, owner = self.owner, ownerSkill = self))
        self.addAffect(affect_util.SplashDizziness(duration = 1, position = self.owner.position, owner = self.owner, ownerSkill = self))

    def allTargets(self):
        return self.owner.position.neighbors
    
class HunGuangShunQian(skill.TargetSkill):
    def __init__(self):
        super().__init__()
        self.setName("F")
        self.setButton("F")
        self.addLabels("faBao", "move")
        self.getTarget = self.getRandomTarget
        self.showTitle = "瞬迁"

    def allTargets(self):
        return self.owner.position.neighbors

    def isCastable(self):
        if super().isCastable() and self.owner.faBao > 0:
            return True
        return False
    
    def cast(self):
        super().cast()
        target = self.getTarget()
        target.setChampion(self.owner)
        if not self.owner.hasSword and self.owner.swordPosition == target:
            for state in self.owner.states:
                if state.name == "freeQPasitive":
                    self.owner.getState(HunGuangHoistSword(owner = self.owner))
                    self.owner.states.remove(state)
            self.owner.hasSword = True
        self.owner.faBao -= 1

    def getSoloAITarget(self):
        if self.owner.enemy.positionLastFrame not in self.allTargets(): return self.getRandomTarget()
        target = self.owner.enemy.positionLastFrame
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target