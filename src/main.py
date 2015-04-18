import pygame
from pygame.locals import *
from sys import exit
import time, math
import player, environment, score, menu

#Init and Background Setup
pygame.init()
screen = pygame.display.set_mode((800,600))
character = player.player()
terrain = environment.environment()
gameMenu = menu.mainMenu(screen)

playerScore = score.score()

#Game Clock
clock = pygame.time.Clock()
sleepTime = 0.01

#Title
pygame.display.set_caption('Free Runner')

gameMenu.start()
time.sleep(sleepTime)
        
#Game Loop
while True:
        events = pygame.event.get()
        for event in events:
                if event.type == QUIT:
                        if not gameMenu.mute:
                                pygame.mixer.music.stop()
                        pygame.display.quit()
                        exit(0)
        keys=pygame.key.get_pressed()
        
        if keys[K_LEFT]:
                character.moveLeft()
        if keys[K_RIGHT]:
                character.moveRight()
        if keys[K_SPACE]:
                character.jump(gameMenu.mute)        
        if keys[K_DOWN]:
                character.duck()
        if keys[K_p]:
                gameMenu.pause()

        #Detect Collisions
        terrain.detectCollision(character)
        
        #Print the Environment
        terrain.printTerrain(screen)
        terrain.updateDifficulty(playerScore)

        #Print the player
        character.updatePlayer(screen, terrain, playerScore)
        character.updatePic()
        if character.endGame(): #Death check
                if not gameMenu.mute:
                        pygame.mixer.music.stop()
                gameMenu.died(screen, playerScore)
                character = player.player()
                terrain = environment.environment()
                
        #Print the Score
        playerScore.printScore(screen)

        #Update and wait till next iteration
        pygame.display.flip()
        time.sleep(sleepTime)
