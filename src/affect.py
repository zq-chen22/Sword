class AffectProperty:
    def __init__(self):
        self.states = []

    def getDamage(self):
        damage = 0
        for state in self.states:
            damage += state.property.damage
        return damage


class Affect:
    '''Here an affect is what a skill adds on a place. An affect will settle at the end of a turn. 
    The owner of an affect is the champion with the skill that produces this effect'''
    def __init__(self, owner = None, ownerSkill = None ,position = None, name = None, **kwargs):
        self.owner = owner
        self.ownerSkill = ownerSkill
        self.position = position
        self.name = name
        self.kwargs = kwargs
        self.priority = 1000
        # print("self.position.affects.append(self)")
        self.position.affects.append(self)
        self.property = AffectProperty()
    
    def setOwner(self, owner):
        self.owner = owner

    def setOwnerSkill(self, ownerSkill):
        self.ownerSkill = ownerSkill

    def setName(self, name):
        self.name = name

    def getTargets(self):
        return None

    def settle(self):
        self.position.affects.remove(self)
        if "hitActivatedFunctions" in self.kwargs.keys():
            if self.getTargets():
                if len(self.getTargets()) > 0:
                    for hitActivatedFunc in self.kwargs["hitActivatedFunctions"]:
                        hitActivatedFunc()

    # def dealWithAffect(self, affect):
    #     return affect