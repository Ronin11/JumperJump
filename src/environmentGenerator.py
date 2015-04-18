import random
import environment

class environmentGenerator:
    def __init__(self):
        random.seed()
        self.blocks = ["Asphalt", "Dirt", "Grass", "Ice"]
        self.scenery = ["Lightpole", "Bush", "Tree", "frozenBush"]
        self.sky = ["Smog", "Cloud", "Birds", "Snowing"]
        self.backgrounds = ["city", "forest", "Beach", "Glacier"]
        self.prev = 0
        self.difficulty = 1
        
    def getNextCol(self, terrain, iterator):
        isSpace = random.randint(0,100)
        if isSpace < self.difficulty/5:
            self.prev = 4
            empty = environment.nothing(terrain.board[len(terrain.board)-1][iterator].posx+100, 500)
            empty2 = environment.nothing(terrain.board[len(terrain.board)-1][iterator].posx+100, 400)
            empty3 = environment.nothing(terrain.board[len(terrain.board)-1][iterator].posx+100, 300)
            return [empty, empty2, empty3]
        if self.prev == 4:
            envType = random.randint(0,3)
        else:
            if random.randint(0,100) < 65:
                envType = self.prev
            else:
                envType = random.randint(0,3)
                
        self.prev = envType
        block = environment.block(self.blocks[envType], (terrain.board[len(terrain.board)-1][iterator].posx+100), 500)
        scenery = environment.scenery(self.scenery[envType], (terrain.board[len(terrain.board)-1][iterator].posx+100), 400)
        sky = environment.scenery(self.sky[envType], (terrain.board[len(terrain.board)-1][iterator].posx+100), 300)
        return [block, scenery, sky]

    def updateDifficulty(self, score):
        self.difficulty = score.score

    def getNextBackground(self, posy):
        if self.prev == 4:
            temp = environment.background(self.backgrounds[random.randint(0,3)],posy, 0)
        else:
            temp = environment.background(self.backgrounds[self.prev],posy, 0)
        return temp
