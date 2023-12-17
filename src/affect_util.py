from affect import Affect
import state_util

class SplashHurt(Affect):
    def __init__(self, damage, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.damage = damage

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets

    def settle(self):
        super().settle()
        for champion in self.getTargets():
            hurt = state_util.Hurt(self.damage)
            champion.getState(hurt)
            self.property.states.append(hurt)
    
class RealSplashHurt(Affect):
    def __init__(self, damage, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.damage = damage

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets

    def settle(self):
        super().settle()
        [champion.getState(state_util.RealHurt(self.damage)) for champion in self.getTargets()]  

class SplashDizziness(Affect):
    def __init__(self, duration, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.duration = duration

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets

    def settle(self):
        super().settle()
        for champion in self.getTargets():
            duration = self.duration
            if champion.hasState("Invincible"):
                continue
            champion.getState(state_util.Dizziness(duration))

class SplashImmobility(Affect):
    def __init__(self, duration, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.duration = duration

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets

    def settle(self):
        super().settle()
        for champion in self.getTargets():
            duration = self.duration
            if champion.hasState("Invincible"):
                continue
            champion.getState(state_util.Immobility(duration))

