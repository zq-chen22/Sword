import affect_util
import affect
import state_util
import state

class HunGuangRealDamagePassitive(state.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.priority = 3000
        self.name = "realDamagePasitive"

    def deal(self):
        self.owner.nextTurnStates.append(self)
    
    def narration(self):
        return self.name 

class HunGuangFreeQPassitive(state.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.priority = 3000
        self.name = "freeQPasitive"

    def deal(self):
        self.owner.nextTurnStates.append(self)
    
    def narration(self):
        return self.name 

class HunGuangHoistSword(state.State):
    def __init__(self, owner, *args):
        super().__init__(*args)
        self.priority = 3000
        self.name = "hoistSword"
        self.duration = 2
        self.sheild = state_util.Sheild(1, 2)
        owner.getState(self.sheild)

    def remove(self):
        super().remove()
        self.sheild.duration = 0

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)
    
    def ownerCanCastSkill(self, skill):
        if skill.name in ("Auto Attack", "Q-1"):
            return False
        return True

    def narration(self):
        return self.name
    
class HunGuangHeChen(state.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.priority = 3000
        self.name = "heChen"

    def deal(self):
        for skillAffect in self.owner.property.skillAffects:
            damage = 0
            for affect in skillAffect["affects"]:
                damage += affect.property.getDamage()
            if damage > 0:
                self.owner.maxHealth += 1
                self.owner.getState(state_util.Heal(damage))
                if "endurance" in skillAffect["skill"].kwargs.keys():
                    self.owner.recoverEndurance(1 + skillAffect["skill"].kwargs["endurance"])
                else:
                    self.owner.recoverEndurance(1)
                return
        if not self.owner.property.isHurt:
            self.owner.nextTurnStates.append(self)
    
    def narration(self):
        return self.name
    
class HunGuangSweepSword(state.State):
    def __init__(self, endurance, *args):
        super().__init__(*args)
        self.priority = 1500
        self.name = "sweepSword"
        self.endurance = endurance

    def deal(self):
        if self.owner.property.expectedDamage > 0:
            affect_util.SplashHurt(damage = self.owner.property.expectedDamage, position = self.owner.position, owner = self.owner, ownerSkill = self.owner.skills[7])
            self.owner.recoverEndurance(self.endurance)

    def narration(self):
        return self.name
    
class HunGuangOnSky(state.State):
    def __init__(self, owner,  poisoners, *args):
        super().__init__(*args)
        self.priority = 3000
        self.name = "onSky"
        self.poisoners = poisoners
        self.duration = 2
        self.invincible = state_util.Invincible(duration = 2)
        owner.getState(self.invincible)

    def remove(self):
        super().remove()
        self.invincible.remove()

    def deal(self):
        for poisoner in self.poisoners:
            if poisoner.position == self.owner.position:
                poisoner.getNextTurnState(state_util.Immobility(0))
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)
    
    def ownerCanCastSkill(self, skill):
        if skill.name not in ("R-2", "End"):
            return False
        return True

    def narration(self):
        return self.name