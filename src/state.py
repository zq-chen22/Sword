class StateProperty:
    def __init__(self):
        self.damage = 0

class State:
    def __init__(self, owner = None, caster = None, name = None, priority = 0):
        self.owner = owner
        self.caster = caster
        self.name = name
        self.priority = priority
        self.property = StateProperty()
        self.cname = "状态"
        self.csubname = None
        self.visiable = True
    
    def setOwner(self, owner):
        self.owner = owner

    def getCsubname(self):
        return self.csubname

    def deal(self):
        '''The real consequece of a state.'''
        return None

    def settle(self, *arg, **kwarg):
        '''Check though all the other states and deal the result. This will also remove the state from states.'''
        self.owner.states.remove(self)
        self.deal()
    
    def narration(self):
        return f"{self.name}"

    def remove(self):
        if self.owner:
            self.owner.states.remove(self)

    def ownerCanCastSkill(self, skill):
        return True

        