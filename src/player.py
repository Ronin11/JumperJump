import pygame

class player(object):
        
        def __init__(self):
                self.friction = 0.3
                self.accel = 1
                self.maxSpeed = 5
                self.gravity = 0.1
                self.jumpPower = 6
                self.pic = pygame.image.load("../Assets/img/StandingRight.gif").convert_alpha()
                self.standingRight = pygame.image.load("../Assets/img/StandingRight.gif").convert_alpha()
                self.standingLeft = pygame.image.load("../Assets/img/StandingLeft.gif").convert_alpha()
                self.jumpingRight = pygame.image.load("../Assets/img/JumpingRight.gif").convert_alpha()
                self.jumpingLeft = pygame.image.load("../Assets/img/JumpingLeft.gif").convert_alpha()
                self.walkRightRight = pygame.image.load("../Assets/img/WalkingRightRight.gif").convert_alpha()
                self.walkRightLeft = pygame.image.load("../Assets/img/WalkingRightLeft.gif").convert_alpha()
                self.walkLeftRight = pygame.image.load("../Assets/img/WalkingLeftRight.gif").convert_alpha()
                self.walkLeftLeft = pygame.image.load("../Assets/img/WalkingLeftLeft.gif").convert_alpha()
                self.jumpSound = pygame.mixer.Sound("../Assets/sounds/jump.wav")
                self.posx = 300
                self.posy = 300
                self.velx = 0
                self.vely = 0
                self.inAir = False
                self.onWall = False
                #Wall Side collision 0 = none, 1 = Right, 2 = Left
                self.wallSide = 0
                #Prev State 0 = Standing, 1 = Jumping, 2 = WalkingRight, 3 = Walking Left.
                self.prevState = 0
                self.heldTime = 0
                #Amount of iterations before switching pics for the walk cycles
                self.walkFrames = 10
                self.feetRect = pygame.Rect(self.posx+25, self.posy+98, 25, 2)
                self.otherRect = pygame.Rect(self.posx+20, self.posy, 60, 90)

        def moveRight(self):
                if self.velx < self.maxSpeed and not self.inAir:
                        self.velx += self.accel

        def moveLeft(self):
                if self.velx > -self.maxSpeed and not self.inAir:
                        self.velx -= self.accel

        def jump(self, mute):
                if not self.inAir:
                        if not mute:
                                self.jumpSound.play()
                        self.vely -= self.jumpPower
                        self.inAir = True
                        self.onWall = False
                        #self.prevAir = True
                        self.posy -= 2 #Offset to stop the collision detection
                elif self.onWall:
                        if not mute:
                                self.jumpSound.play()
                        self.vely -= self.jumpPower/2
                        if self.wallSide == 2:
                                self.velx -= self.jumpPower/2
                                self.posx -= 5 #Offset to stop the collision detection
                        elif self.wallSide == 1:
                                self.velx += self.jumpPower/2
                                self.posx += 5 #Offset to stop the collision detection
                        self.inAir = True
                        self.onWall = False
                if self.vely < -self.maxSpeed:
                        self.vely = -self.maxSpeed               

        def duck(self):
                print "duck"

        def physics(self):
                if self.inAir:
                        self.vely += self.gravity
                else:
                        if self.velx > 0:
                                self.velx -= self.friction
                        elif self.velx < 0:
                                self.velx += self.friction
                if abs(self.velx) < self.friction:
                        self.velx = 0
        def updatePic(self):
                if self.inAir:
                        self.prevState = 1
                        if self.velx >= 0:
                                self.pic = self.jumpingRight
                        else:
                                self.pic = self.jumpingLeft
                else:
                        if self.velx > 0:
                                if self.prevState == 2:
                                        self.heldTime += 1
                                else:
                                        self.heldTime = 0
                                self.prevState = 2
                                self.pic = self.standingRight
                                if self.heldTime > self.walkFrames:
                                        self.pic = self.walkRightRight
                                if self.heldTime > (self.walkFrames*2):
                                        self.pic = self.standingRight
                                if self.heldTime > (self.walkFrames*3):
                                        self.pic = self.walkLeftRight
                                if self.heldTime > (self.walkFrames*4):
                                        self.pic = self.standingRight
                                        self.heldTime = 0
                                        
                        elif self.velx < 0:
                                if self.prevState == 3:
                                        self.heldTime += 1
                                else:
                                        self.heldTime = 0
                                self.prevState = 3
                                self.pic = self.standingLeft
                                if self.heldTime > self.walkFrames:
                                        self.pic = self.walkRightLeft
                                if self.heldTime > (self.walkFrames*2):
                                        self.pic = self.standingLeft
                                if self.heldTime > (self.walkFrames*3):
                                        self.pic = self.walkLeftLeft
                                if self.heldTime > (self.walkFrames*4):
                                        self.pic = self.standingLeft
                                        self.heldTime = 0
                
        def updatePlayer(self, screen, terrain, score):
                self.physics()
                self.posx += self.velx
                if self.posx > 300:
                        terrain.move(self.posx-300, score)
                        self.posx = 300
                elif self.posx < 0:
                        self.posx = 0
                self.posy += self.vely
                self.feetRect = pygame.Rect(self.posx+25, self.posy+98, 25, 2)
                self.otherRect = pygame.Rect(self.posx+20, self.posy, 60, 90)
                screen.blit(self.pic, (self.posx, self.posy))

        def endGame(self):
                if self.posy > 605:
                        return True
                else:
                        return False
