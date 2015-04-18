import pygame

#Scoring Display
class score:
        def __init__(self):
                self.scoreFont = pygame.font.SysFont("arial", 45)
                self.scoreText = "Score:"
                self.score = 0
                
                
        def printScore(self, screen):
                label = self.scoreFont.render(self.scoreText+`self.score`, 5, (255,0,0))
                screen.blit(label, (550, 15))

        def increment(self):
                self.score += 1

        def reset(self):
                self.score = 0

        def sendScore(self):
                return self.score
                
