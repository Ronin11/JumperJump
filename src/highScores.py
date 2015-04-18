import menu

class highScores:
    def __init__(self):
        self.file = open("../Assets/scores", 'r')
        self.strings = []
        #Player then Score.
        self.scores = [[],[]]
        for line in self.file:
            line = line.rstrip()
            self.strings.append(line)
            temp = line.split(':')
            self.scores[0].append(temp[0])
            self.scores[1].append(temp[1])
        self.file.close()

    def getMenuItems(self):
        self.list = []
        for line in self.strings:
            self.list.append(menu.menuItem(line))
        return self.list

    def isHighScore(self, newScore):
        if len(self.scores[1]) < 3:
            return True
        for i in range(len(self.scores[1])):
            if int(newScore) > int(self.scores[1][i]):
                return True
        return False
    
    def addHighScore(self, newScore, playerName):
        self.scores[0].append(playerName)
        self.scores[1].append(newScore)
        for j in range(len(self.scores[1])-1):
            for i in range(len(self.scores[1])-1):
                if int(self.scores[1][i]) < int(self.scores[1][i+1]):
                    tempScore =  self.scores[1][i+1]
                    tempName = self.scores[0][i+1]
                    self.scores[1][i+1] = self.scores[1][i]
                    self.scores[0][i+1] = self.scores[0][i]
                    self.scores[1][i] = tempScore
                    self.scores[0][i] = tempName
        if len(self.scores[1]) > 3:
            self.scores[0].pop()
            self.scores[1].pop()

        self.writeScores()

    def writeScores(self):
        self.file = open("../Assets/scores", 'w')
        for i in range(len(self.scores[0])):
            self.file.write(str(self.scores[0][i]) + ":" + str(self.scores[1][i]) + "\n")
        self.file.close()
        self = highScores()
