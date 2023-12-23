# The champions manipulated by people.
import random
from settings import *

class InTurnProperty:
    def __init__(self):
        self.isHit = False
        self.isHurt = False
        self.isControled = False
        self.skillAffects = []
        self.expectedDamage = 0

# class WindowProperty:
#     def __init__(self):
#         self.

class Champion:

    championId = 0

    def __init__(self):
        Champion.championId += 1
        self.position = None
        self.health = None
        self.skills = []
        self.states = []
        self.name = None
        self.policy = None
        self.maxHealth = None
        self.hasUtimate = True
        self.title = "DefaultChampion"
        if self.name is None:
            self.name = f"champion{Champion.championId}"
        self.setIdAsGroup()
        self.setPolicy("random")
        self.chooseSkillFunc = self.chooseSkillRandom
        self.getSkills()
        self.token = ""
        self.tokenIndex = 0
        self.nextTurnStates = []
        self.property = InTurnProperty()
        self.propertyHistory = []
        self.showPosition = "Left"
        # self.window = WindowProperty()

    def narration(self):
        nar = f"one {self.title} named {self.name} at {self.position.name} with health {self.health}/{self.maxHealth} and {len(self.states)} states"
        for state in self.states:
            nar += ", " + state.narration()
        return nar

    def setPosition(self, position):
        self.position = position

    def setName(self, name):
        self.name = name

    def setGroup(self, group):
        self.group = group

    def setIdAsGroup(self):
        self.group = self.championId

    def settleAllState(self, priority = 4000):
        for state in sorted(self.states, key = lambda state: state.priority):
            if state.priority <= priority:
                state.settle()

    def newStates(self):
        self.states = self.nextTurnStates
        self.nextTurnStates = []
    
    def getSkill(self, skill):
        self.skills.append(skill)
        skill.setOwner(self)

    def castSkill(self, skill):
        skill.cast()

    def canCastSkill(self, skill):
        for state in self.states:
            if not state.ownerCanCastSkill(skill):
                return False
        return skill in self.skills and skill.isCastable()

    def castableSkills(self):
        castableSkills = []
        for skill in self.skills:
            if self.canCastSkill(skill):
                castableSkills.append(skill)
        return castableSkills

    def getState(self, state):
        self.states.append(state)
        state.setOwner(self)

    def getNextTurnState(self, state):
        self.nextTurnStates.append(state)
        state.setOwner(self)

    def beforeTurn(self, **kwarg):
        self.propertyHistory.append(self.property)
        self.property = InTurnProperty()

    def midTurn(self, **kwarg):
        pass

    def afterTurn(self, **kwarg):
        self.settleAllState(**kwarg)

    def __str__(self):
        return self.title + " " + self.name

    def isSurvive(self):
        if self.health > 0:
            return True
        return False 
    
    def setPolicy(self, policy, **kwarg):
        self.policy = policy
        for skill in self.skills:
            skill.switchPolicy(policy)
        if policy == "random":
            self.chooseSkillFunc = self.chooseSkillRandom
        if policy == "input":
            self.chooseSkillFunc = self.chooseSkillInput
        if policy == "token":
            self.chooseSkillFunc = self.chooseSkillToken
            self.token = kwarg['token']
        if policy == "mix":
            self.chooseSkillFunc = self.chooseSkillMix
            if 'token' in kwarg.keys():
                self.token = kwarg['token']


    def midTurn(self, **kwarg):
        if "log" in kwarg.keys():
            kwarg["log"][-1] += f"{self.title} {self.name} chooses to take the following moves.\n"
        while self.castableSkills() != []:
            choosedSkill = self.chooseSkillFunc()
            if choosedSkill.button == ".":
                break
            self.castSkill(choosedSkill)
            if "log" in kwarg.keys():
                kwarg["log"][-1] += choosedSkill.narration()
                kwarg["log"][-1] += ","
        if "log" in kwarg.keys():
            kwarg["log"][-1] += "\n"
        if self.policy == "token":
            self.tokenIndex += 1
        else:
            self.tokenIndex += 1
            self.token += " "

    def chooseSkillRandom(self):
        skill = random.choice(self.castableSkills())
        button = skill.button
        self.token += button
        self.tokenIndex += 1
        return skill
  
    def chooseSkillInput(self): 
        print(f"Now all skills {self.name} can use are {[skill.button + '.' + skill.name for skill in self.castableSkills()]}")
        button = input("Please input the button of your target skill: ")
        for skill in self.castableSkills():
            if skill.button == button:
                self.token += button
                self.tokenIndex += 1
                return skill
        print("invalid skill.")
        return self.chooseSkillInput()

    def chooseSkillToken(self):
        button = self.token[self.tokenIndex]
        for skill in self.castableSkills():
            if skill.button == button:
                self.tokenIndex += 1
                return skill
        return None
    
    def chooseSkillMix(self):
        if self.tokenIndex < len(self.token):
            return self.chooseSkillToken()
        instruction = input("Please add some action token or input 'random' for random mode or 'input' for input mode.\n")
        if instruction == "random":
            self.chooseSkillFunc = self.chooseSkillRandom
            return self.chooseSkillFunc()
        if instruction == "input":
            self.chooseSkillFunc = self.chooseSkillInput
            return self.chooseSkillFunc()
        self.token.append(instruction)
        return self.chooseSkillToken()
        
    def hasState(self, stateName):
        for state in self.states:
            if state.name == stateName:
                return True
        return False

    # window display attributes
    def showSkills(self):
        buttonDict = {}
        for skill in self.skills:
            if skill.button in buttonDict.keys():
                buttonDict[skill.button].append(skill)
            else:
                buttonDict[skill.button] = [skill]
        if self.showPosition == "Left":
            skillPos = [0.5 * (WIDTH - 70 * len(buttonDict.keys())) , HEIGHT - 250]
        for i, k in enumerate(buttonDict.keys()):
            isActive = False
            for skill in buttonDict[k]:
                if skill.isCastable():
                    skill.showAt(skillPos)
                    isActive = True
                    break
            if not isActive:
                buttonDict[k][0].showAt(skillPos)
            if self.showPosition == "Left":
                skillPos[0] += int((len(skill.showTitle)-1)/4) * 50 + 70

            


if __name__ == "__main__":
    x = Champion()
    y = Champion()
    z = Champion()
    t = Champion()
    print(x.canCastSkill(1))
    print(x.group)
    print(y.group)
    print(z.group)
    print(t.group)
