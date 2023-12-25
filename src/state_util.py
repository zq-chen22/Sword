from state import State

class Hurt(State):
    def __init__(self, damage, *args):
        super().__init__(*args)
        self.damage = damage
        self.name = "Hurt"
        self.priority = 1000
        self.cname = "受伤"
        self.csubname = f"×{self.damage}"

    def deal(self):
        damage = self.damage
        self.owner.property.expectedDamage += damage
        self.property.damage = damage
        for state in self.owner.states:
            if state.name == "Invincible":
                damage = 0
            if state.name == "Sheild":
                if damage > state.damage:
                    damage -= state.damage
                    state.save(state.damage)
                else:
                    state.save(damage)
                    damage = 0
        self.owner.property.isHit = True
        if damage > 0:
            self.owner.property.isHurt = True
        self.owner.health -= damage
        
    
    def narration(self):
        return f"{self.damage}-{self.name}" 
    
class RealHurt(State):
    def __init__(self, damage, *args):
        super().__init__(*args)
        self.damage = damage
        self.name = "RealHurt"
        self.priority = 1000
        self.cname = "真伤"
        self.csubname = f"×{self.damage}"

    def deal(self):
        damage = self.damage
        self.owner.property.expectedDamage += damage
        self.property.damage = damage
        for state in self.owner.states:
            if state.name == "Invincible":
                damage = 0
        self.owner.property.isHit = True
        if damage > 0:
            self.owner.property.isHurt = True
        self.owner.health -= damage
    
    def narration(self):
        return f"{self.damage}-{self.name}"


class Heal(State):
    def __init__(self, damage, *args):
        super().__init__(*args)
        self.damage = damage
        self.name = "Heal"
        self.priority = 2000
        self.cname = "治疗"
        self.csubname = f"×{self.damage}"

    def deal(self):
        self.owner.health = min(self.damage + self.owner.health, self.owner.maxHealth)
    
    def narration(self):
        return f"{self.damage}-{self.name}"

class Sheild(State):
    def __init__(self, damage, duration, *args):
        super().__init__(*args)
        self.damage = damage
        self.name = "Sheild"
        self.priority = 2000
        self.duration = duration
        self.cname = "护盾"

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)

    def narration(self):
        return f"{self.damage}-{self.name}"
    
    def getCsubname(self):
        return f"{self.damage}×{self.duration+1}"

    def save(self, damage):
        self.damage -= damage

class Invincible(State):
    def __init__(self, duration, *args):
        super().__init__(*args)
        self.name = "Invincible"
        self.priority = 3000
        self.duration = duration
        self.cname = "无敌"

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)

    def narration(self):
        return f"{self.duration}-{self.name}"

    def getCsubname(self):
        return f"×{self.duration+1}"
    
class Unselectable(State):
    def __init__(self, duration, *args):
        super().__init__(*args)
        self.name = "Unselectable"
        self.priority = 3000
        self.duration = duration
        self.cname = "无影"

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)

    def narration(self):
        return f"{self.duration}-{self.name}"

    def getCsubname(self):
        return f"×{self.duration+1}"

class Dizziness(State):
    def __init__(self, duration, *args):
        super().__init__(*args)
        self.name = "Dizziness"
        self.priority = 3000
        self.duration = duration
        self.cname = "眩晕"

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)

    def ownerCanCastSkill(self, skill):
        if super().ownerCanCastSkill(skill) and skill.hasLabels("anyState"):
            return True
        return False

    def narration(self):
        return f"{self.duration}-{self.name}"

    def getCsubname(self):
        return f"×{self.duration+1}"
    
class Immobility(State):
    def __init__(self, duration, *args):
        super().__init__(*args)
        self.name = "Immobility"
        self.priority = 3000
        self.duration = duration
        self.cname = "定身"

    def deal(self):
        if self.duration == 0:
            return
        self.duration -= 1 
        self.owner.nextTurnStates.append(self)

    def ownerCanCastSkill(self, skill):
        if super().ownerCanCastSkill(skill) and not skill.hasLabels("move"):
            return True
        return False

    def narration(self):
        return f"{self.duration}-{self.name}"
    
    def getCsubname(self):
        return f"×{self.duration+1}"