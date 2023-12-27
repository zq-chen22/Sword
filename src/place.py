class Place:

    placeId = 0

    def __init__(self):
        Place.placeId += 1
        self.champions = []
        self.neighbors = []
        self.affects = []
        self.name = f"place{Place.placeId}"
        self.index = Place.placeId
        self.nextTurnAffects = []
        self.screenPos = None
        self.cname = f"地点{Place.placeId}"
        self.window = None
        self.placeImg = None
    
    def setName(self, name):
        self.name = name

    def setIndex(self, index):
        self.index = index

    def setChampion(self, champion):
        self.champions.append(champion)
        if champion.position:
            champion.position.removeChampion(champion)
        champion.setPosition(self)

    def removeChampion(self, champion):
        self.champions.remove(champion)

    def settle(self, priority = 4000):
        for affect in self.affects:
            # self.affects.remove(affect)
            if affect.priority <= priority:
                affect.settle()

    def newAffects(self):
        self.affects = self.nextTurnAffects
        self.nextTurnAffects = []

    def narration(self):
        narration = f"{self.index}.{self.name} with champions {[champion.name for champion in self.champions]}."
        return narration

    def showAt(self, pos = None):
        pass

    def __str__(self):
        return f"{self.index}.{self.name}"
    
    def placeImgInit(self):
        pass


