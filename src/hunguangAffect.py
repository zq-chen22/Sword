import affect
import affect_util

class HunGuangRealDamagePasitiveFeedback(affect.Affect):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.setName("HunGuangRealDamagePasitiveFeedback")

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets
    
    def settle(self):
        super().settle()
        if len(self.getTargets()) > 0:
            self.owner.realDamagePasitiveActivateFunc()

class HunGuangAddQLayerFeedback(affect.Affect):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.setName("HunGuangAddQLayerPasitiveFeedback")

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets
    
    def settle(self):
        super().settle()
        if len(self.getTargets()) > 0:
            for skill in self.owner.skills:
                if skill.name == "Q-2":
                    skill.addLayer()

class HunGuangForceMove(affect.Affect):
    def __init__(self, destination, **kwarg):
        super().__init__(**kwarg)
        self.setName("HunGuangAddQLayerPasitiveFeedback")
        self.destination = destination
        self.priority = 500

    def getTargets(self):
        targets = []
        for champion in self.position.champions:
            if champion.group != self.owner.group and not champion.hasState("Unselectable"):
                targets.append(champion)
        return targets
    
    def settle(self):
        super().settle()
        for champion in self.getTargets():
            self.destination.setChampion(champion) 