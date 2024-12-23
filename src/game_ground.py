class GameGround:
    def __init__(self):
        self.turn = 0
        self.places = []
        self.champions = []
        self.motionLog = [""]
        self.gameover = False

    def insertPlace(self, place):
        self.places.append(place)
        place.window = self
        for champion in place.champions:
            if champion not in self.champions:
                self.champions.append(champion)
                champion.window = self
    
    def insertChampion(self, champion):
        self.champions.append(champion)
        champion.window = self

    def narration(self):
        narration = f"Now it is turn {self.turn}. There are {len(self.places)} places and {len(self.champions)} champions as following.\n"
        for ind, champion in enumerate(self.champions):
            narration += f"{ind + 1}. {champion.narration()}.\n"
        return narration
    
    def newLog(self):
        self.motionLog.append("")

    def reportLog(self):
        print(self.motionLog[-1])

    def beforeTurn(self):
        self.newLog()
        for champion in self.champions:
            champion.beforeTurn()
            
    def midTurn(self):
        for champion in self.champions:
            champion.midTurn(log = self.motionLog)
        
    def afterTurn(self):
        while True:
            priorities = []
            for place in self.places:
                for affect in place.affects:
                    priorities.append(affect.priority)
            for champion in self.champions:
                for state in champion.states:
                    priorities.append(state.priority)
            if len(priorities) == 0:
                break
            i = sorted(priorities)[0]
            for place in self.places:
                place.settle(priority = i)
            for champion in self.champions:
                champion.afterTurn(priority = i)
        for place in self.places:
            place.newAffects()
        for champion in self.champions:
            champion.newStates()
        self.reportLog()

    def runTurn(self):
        self.turn += 1
        self.beforeTurn()
        print(self.narration(), end="")
        self.midTurn()
        self.afterTurn()
        if self.checkWin():
            exit()

    def checkWin(self):
        if (self.champions[0].isSurvive() and self.champions[1].isSurvive()):
           return False
        if self.champions[0].isSurvive() and not self.champions[1].isSurvive():
            print(f"{self.champions[0].name} wins")
        if self.champions[1].isSurvive() and not self.champions[0].isSurvive():
            print(f"{self.champions[1].name} wins")
        if not self.champions[1].isSurvive() and not self.champions[0].isSurvive():
            print(f"It's a draw")
        for champion in self.champions:
            print(f"{champion.name}'s token:")
            print(champion.token)
        self.gameover = True
        return True
