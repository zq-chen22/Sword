import random

class SkillShoot():
    def __init__(self, skill, **kwargs):
        self.skill = skill
        self.kwargs = kwargs

class Skill:
    def __init__(self):
        self.owner = None
        self.name = "default skill"
        self.button = None
        self.labels = []

    def addLabels(self, *arg):
        for label in arg:
            self.labels.append(label)

    def hasLabels(self, label):
        if label in self.labels:
            return True
        return False

    def setName(self, newName):
        self.name = newName

    def setButton(self, newButton):
        self.button = newButton

    def setOwner(self, newOwner):
        self.owner = newOwner
    
    def cast(self, **kwarg):
        self.owner.property.skillAffects.append({"skill": SkillShoot(self, **kwarg), "affects": []})

    def isCastable(self):
        return self.isCastableOverStates()

    def isCastableOverStates(self):
        for state in self.owner.states:
            if not state.ownerCanCastSkill(self):
                return False
        return True
    
    def addAffect(self, affect):
        self.owner.property.skillAffects[-1]["affects"].append(affect)
        affect.setOwner(self.owner)
        affect.setOwnerSkill(self)

    def narration(self):
        return self.name
    
    def refresh(self):
        pass

    def switchPolicy(self, policy):
        pass

class TargetSkill(Skill):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.name = "target skill"
        self.getTarget = self.getRandomTarget
        self.addLabels("target")
    
    def allTargets(self):
        return None
    
    def getRandomTarget(self):
        index = random.randrange(len(self.allTargets()))
        target = self.allTargets()[index]
        self.owner.token += str(target.index)
        self.owner.tokenIndex += 1
        self.targets.append(target)
        return target
    
    def getInputTarget(self):
        print(f"Now all possible targets of {self.owner.name}'s {self.name} are {[target.__str__() for target in self.allTargets()]}")
        index = int(input("Please input the index of your target place: "))
        for target in self.allTargets():
            if target.index == index:
                self.owner.token += str(index)
                self.owner.tokenIndex += 1
                self.targets.append(target)
                return target
        print("That's not a valid index.")
        return self.getInputTarget()

    def getTokenTarget(self):
        index = int(self.owner.token[self.owner.tokenIndex])
        self.owner.tokenIndex += 1
        for target in self.allTargets():
            if target.index == index:
                self.targets.append(target)
                return target
    
    def getMixTarget(self):
        if self.tokenIndex < len(self.token):
            return self.getTokenTarget()
        instruction = input("Please add some action token or input 'random' for random mode or 'input' for input mode.\n")
        if instruction == "random":
            self.getTarget = self.getRandomTarget
            return self.getTarget()
        if instruction == "input":
            self.getTarget = self.getInputTarget
            return self.getTarget()
        self.owner.token.append(instruction)
        return self.getTokenTarget()

    def switchPolicy(self, policy):
        if policy == "random":
            self.getTarget = self.getRandomTarget
        if policy == "input":
            self.getTarget = self.getInputTarget
        if policy == "token":
            self.getTarget = self.getTokenTarget
        if policy == "mix":
            self.getTarget = self.getMixTarget



    def narration(self):
        nar = self.name
        for target in self.targets:
            nar += "-(" + target.name + ")"
        self.targets = []
        return nar

class GiveUp(Skill):
    def __init__(self):
        super().__init__()
        self.setName("End")
        self.addLabels("anyState")
        self.setButton(".")