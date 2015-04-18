import pygame
import environmentGenerator

class block:
    def __init__(self, pic, posx, posy):
        self.pic = pygame.image.load("../Assets/img/" + pic + ".bmp").convert_alpha()
        self.posx = posx
        self.posy = posy

class scenery:
    def __init__(self, pic, posx, posy):
        self.pic = pygame.image.load("../Assets/img/" + pic + ".gif").convert_alpha()
        self.posx = posx
        self.posy = posy

class background:
    def __init__(self, pic, posx, posy):
        temp = pygame.image.load("../Assets/img/" + pic + ".bmp").convert()
        self.pic = pygame.transform.scale(temp, (500, 500))
        self.pic.set_alpha(100)
        self.posx = posx
        self.posy = posy
        
class nothing:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy 

class environment:
    def __init__(self):
        self.generator = environmentGenerator.environmentGenerator()
        self.board = [[block("Asphalt", (i*100), 500),scenery("Lightpole", (i*100), 400)]*1 for i in range(9)]
        self.backgrounds = [background("city", i*500, 0) for i in range(3)]
        
    def printTerrain(self, screen):
        screen.fill((0,0,0))
        for i in range(len(self.backgrounds)):
            screen.blit(self.backgrounds[i].pic, (self.backgrounds[i].posx, self.backgrounds[i].posy))
        for i in range(len(self.board)):
            for j in range (len(self.board[0])):
                if not isinstance(self.board[i][j], nothing):
                    screen.blit(self.board[i][j].pic, (self.board[i][j].posx, self.board[i][j].posy))

    def detectCollision(self, player):
        player.inAir = True
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if isinstance(self.board[i][j], block) and player.feetRect.colliderect(pygame.Rect(self.board[i][j].posx, self.board[i][j].posy, 100, 2)):
                    player.inAir = False
                    player.onWall = False
                    player.vely = 0
                elif isinstance(self.board[i][j], block) and player.otherRect.colliderect(pygame.Rect(self.board[i][j].posx, self.board[i][j].posy, 100, 100)):
                    player.inAir = False
                    player.onWall = True
                    if player.velx > 0:
                        player.wallSide = 1
                    elif player.velx < 0:
                        player.wallSide = 2
                    player.velx = 0
                    
    def move(self, deltaX, playerScore):
        for i in range(len(self.backgrounds)):
            self.backgrounds[i].posx -= deltaX
            if self.backgrounds[i].posx < -500:
                self.backgrounds.append(self.generator.getNextBackground(self.backgrounds[i].posx+1500))
                self.backgrounds.pop(0)
                                        
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].posx -= deltaX
                if self.board[i][j].posx < -100:
                    #Add a new column of blocks
                    self.board.append(self.generator.getNextCol(self, j))
                    #Delete the column of blocks that are off screen on the left side
                    self.board.pop(0)
                    playerScore.increment()

    def updateDifficulty(self, score):
        self.generator.updateDifficulty(score)
                
