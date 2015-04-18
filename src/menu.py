import pygame
from pygame.locals import *
import time, highScores

class menuItem:
    def __init__(self, name):
        self.name = name
        self.font = pygame.font.SysFont("arial", 48)
        self.label = self.font.render(self.name, 5, (255,255,255))
        self.dimensions = self.font.size(self.name)
        self.isSelected = False
        self.offset = 200
        
    def display(self, iterator, screen):
        center = ((screen.get_width() - self.dimensions[0])/2, (self.dimensions[1]+25)*iterator+self.offset)
        self.label = self.font.render(self.name, 5, (255,255,255))
        if self.isSelected:
            self.label = self.font.render(self.name, 5, (0,0,0))
            rect = pygame.Rect((screen.get_width() - self.dimensions[0])/2-25, (self.dimensions[1]+25)*iterator+self.offset-15, self.font.size(self.name)[0]+50, self.font.size(self.name)[1]+30)
            self.rect = pygame.draw.rect(screen, (255,255,255), rect, 0)        
        screen.blit(self.label, center)

class deathNote(menuItem):
    def __init__(self, name):
        menuItem.__init__(self, name)
        self.font = pygame.font.SysFont("arial", 100)
        self.label = self.font.render(self.name, 5, (255,0,0))
        
class title:
    def __init__(self, name):
        self.name = name
        self.font = pygame.font.SysFont("arial", 85)
        self.label = self.font.render(self.name, 5, (255,255,255))
        self.dimensions = self.font.size(self.name)
        self.offset = 35
        
    def display(self, screen):
        center = ((screen.get_width() - self.dimensions[0])/2, self.offset)       
        screen.blit(self.label, center)
        
class mainTitle(title):
    def __init__(self):
        title.__init__(self,"Jumper     Jump")
        self.offset = 50
        self.pic = pygame.image.load("../Assets/img/JumpingRight.gif").convert_alpha()
        
    def display(self, screen):
        center2 = ((screen.get_width() - 100)/2+40, self.offset+30)
        screen.blit(self.pic, center2)
        center = ((screen.get_width() - self.dimensions[0])/2, self.offset)       
        screen.blit(self.label, center)
        
class menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill((0,0,0))
        self.title = mainTitle()
        self.runMenu = True
        self.sleepTime = 0.15
        self.beepTime = 0.1
        self.beep = pygame.mixer.Sound("../Assets/sounds/beep.ogg")
        self.yes = pygame.mixer.Sound("../Assets/sounds/yes.ogg")
        self.death = pygame.mixer.Sound("../Assets/sounds/death.ogg")
        self.menuItems = [menuItem("")]
        self.selected = 0
        self.menuItems[self.selected].isSelected = True
        
    def displayMenu(self):
        self.screen.fill((0,0,0))
        for i in range(len(self.menuItems)):
            self.menuItems[i].display(i, self.screen)

    def moveSelection(self, keys):
        if keys[K_UP]:
            if self.selected > 0:
                 if not self.mute:
                     self.beep.play()
                     time.sleep(self.beepTime)
                 self.menuItems[self.selected].isSelected = False
                 self.selected -= 1
                 self.menuItems[self.selected].isSelected = True
                 self.displayMenu()
                 self.title.display(self.screen)
                    
        elif keys[K_DOWN]:
             if self.selected < len(self.menuItems)-1:
                 if not self.mute:
                     self.beep.play()
                     time.sleep(self.beepTime)
                 self.menuItems[self.selected].isSelected = False
                 self.selected += 1
                 self.menuItems[self.selected].isSelected = True
                 self.displayMenu()
                 self.title.display(self.screen)
                    
            
class mainMenu(menu):
    def __init__(self, screen):
        menu.__init__(self, screen)
        self.menuItems = [menuItem("Play Game"), menuItem("Instructions"), menuItem("High Scores"), menuItem("Settings"), menuItem("Quit")]
        self.mute = False 
        self.high = highScores.highScores()
        self.menuItems[self.selected].isSelected = True
        self.displayMenu()
        self.title.display(self.screen)
        
    def start(self):
        time.sleep(self.sleepTime)
        while self.runMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit(0)
            keys=pygame.key.get_pressed()

            self.moveSelection(keys)

            if keys[K_RETURN]:
                    if not self.mute:
                        self.yes.play()
                        
                    if self.selected == 0:
                        self.runMenu = False
                        if not self.mute:
                            pygame.mixer.music.load("../Assets/sounds/escapeFromTheCity.ogg")
                            pygame.mixer.music.play(-1)
                        
                    elif self.selected == 1:
                        instructs = instructionScreen(self.screen)
                        instructs.run(self)
                        
                    elif self.selected == 2:
                        scores = highScoreScreen(self.screen)
                        scores.run(self)
                        
                    elif self.selected == 3:
                        gameSettings = settings(self.screen)
                        gameSettings.run(self)
                        
                    elif self.selected == 4:
                        runMenu = False
                        pygame.display.quit()
                        exit(0)
                        
            pygame.display.update()
            time.sleep(self.sleepTime)
            
    def died(self, screen, score):
        if not self.mute:
            self.death.play()
        death = deathNote("You Died")
        center = ((screen.get_width() - death.dimensions[0])/2, (screen.get_height() - death.dimensions[1])/2)
        screen.blit(death.label, center)
        pygame.display.update()
        time.sleep(3)
        if self.high.isHighScore(score.sendScore()):
            enterScores = enterHighScore(screen)
            name = enterScores.run(self)
            self.high.addHighScore(score.sendScore(), name)
        score.reset()
        self = mainMenu(self.screen)
        self.start()
class settings(menu):    
    def __init__(self, screen):
        menu.__init__(self,screen)

    def run(self, menu):
        if menu.mute:
            self.menuItems = [menuItem("Mute: On"), menuItem("Done")]
        else:
            self.menuItems = [menuItem("Mute: Off"), menuItem("Done")]
        self.title = title("Settings:")
        self.menuItems[self.selected].isSelected = True
        self.displayMenu()
        self.mute = menu.mute
        self.title.display(self.screen)
        time.sleep(self.sleepTime)
        while self.runMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit(0)
                    
            keys=pygame.key.get_pressed()
        
            self.moveSelection(keys)

            if keys[K_RETURN]:
                    if self.selected == 0:
                        if not menu.mute:
                            menu.yes.play()
                            time.sleep(self.beepTime)
                        if menu.mute:
                            self.screen.fill((0,0,0))
                            menu.mute = False
                            self.mute = menu.mute
                            self.menuItems = [menuItem("Mute: Off"), menuItem("Done")]
                        else:
                            self.screen.fill((0,0,0))
                            menu.mute = True
                            self.mute = menu.mute
                            self.menuItems = [menuItem("Mute: On"), menuItem("Done")]
                        self.menuItems[self.selected].isSelected = True
                        self.displayMenu()
                        self.title.display(self.screen)
                        
                    elif self.selected == 1:
                        if not menu.mute:
                            menu.yes.play()
                            time.sleep(self.beepTime)
                        self.runMenu = False
                        menu.displayMenu()
                        menu.title.display(self.screen)
                        time.sleep(self.sleepTime)
                        break
                        
            pygame.display.update()
            time.sleep(self.sleepTime)
            
class highScoreScreen(menu):    
    def __init__(self, screen):
        menu.__init__(self,screen)

    def run(self, menu):
        self.menuItems = menu.high.getMenuItems()
        self.menuItems.append(menuItem("Done"))
        self.menuItems[len(self.menuItems)-1].isSelected = True
        self.title = title("High Scores:")
        self.displayMenu()
        time.sleep(self.sleepTime)
        self.title.display(self.screen)
        while self.runMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit(0)
                    
            keys=pygame.key.get_pressed()

            if keys[K_RETURN]:
                    if not menu.mute:
                            menu.yes.play()
                            time.sleep(self.beepTime)
                    self.runMenu = False
                    menu.displayMenu()
                    menu.title.display(self.screen)
                    time.sleep(self.sleepTime)
                    break
                        
            pygame.display.update()
            time.sleep(self.sleepTime)

class enterHighScore(menu):    
    def __init__(self, screen):
        menu.__init__(self,screen)

    def run(self, menu):
        self.mute = menu.mute
        enteredName = " "
        self.menuItems = [menuItem(enteredName),menuItem("Done")]
        self.title = title("New Highscore:")
        self.menuItems[self.selected].isSelected = True
        self.displayMenu()
        time.sleep(self.sleepTime)
        self.title.display(self.screen)
        maxChars = 16
        while self.runMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit(0)
                    
            keys=pygame.key.get_pressed()
            if self.selected == 0:
                if keys[K_BACKSPACE]:
                    if enteredName != " ":
                        enteredName = enteredName[:-1]
                        self.menuItems = [menuItem(enteredName),menuItem("Done")]
                        self.menuItems[self.selected].isSelected = True
                        self.displayMenu()
                        self.title.display(self.screen)
                elif keys[K_a]:
                    if enteredName == " ":
                        enteredName = "A"
                    elif len(enteredName) < maxChars:
                        enteredName += "A"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_b]:
                    if enteredName == " ":
                        enteredName = "B"
                    elif len(enteredName) < maxChars:
                        enteredName += "B"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_c]:
                    if enteredName == " ":
                        enteredName = "C"
                    elif len(enteredName) < maxChars:
                        enteredName += "C"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_d]:
                    if enteredName == " ":
                        enteredName = "D"
                    elif len(enteredName) < maxChars:
                        enteredName += "D"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_e]:
                    if enteredName == " ":
                        enteredName = "E"
                    elif len(enteredName) < maxChars:
                        enteredName += "E"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_f]:
                    if enteredName == " ":
                        enteredName = "F"
                    elif len(enteredName) < maxChars:
                        enteredName += "F"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_g]:
                    if enteredName == " ":
                        enteredName = "G"
                    elif len(enteredName) < maxChars:
                        enteredName += "G"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_h]:
                    if enteredName == " ":
                        enteredName = "H"
                    elif len(enteredName) < maxChars:
                        enteredName += "H"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_i]:
                    if enteredName == " ":
                        enteredName = "I"
                    elif len(enteredName) < maxChars:
                        enteredName += "I"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_j]:
                    if enteredName == " ":
                        enteredName = "J"
                    elif len(enteredName) < maxChars:
                        enteredName += "J"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_k]:
                    if enteredName == " ":
                        enteredName = "K"
                    elif len(enteredName) < maxChars:
                        enteredName += "K"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_l]:
                    if enteredName == " ":
                        enteredName = "L"
                    elif len(enteredName) < maxChars:
                        enteredName += "L"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_m]:
                    if enteredName == " ":
                        enteredName = "M"
                    elif len(enteredName) < maxChars:
                        enteredName += "M"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_n]:
                    if enteredName == " ":
                        enteredName = "N"
                    elif len(enteredName) < maxChars:
                        enteredName += "N"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_o]:
                    if enteredName == " ":
                        enteredName = "O"
                    elif len(enteredName) < maxChars:
                        enteredName += "O"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_p]:
                    if enteredName == " ":
                        enteredName = "P"
                    elif len(enteredName) < maxChars:
                        enteredName += "P"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_q]:
                    if enteredName == " ":
                        enteredName = "Q"
                    elif len(enteredName) < maxChars:
                        enteredName += "Q"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_r]:
                    if enteredName == " ":
                        enteredName = "R"
                    elif len(enteredName) < maxChars:
                        enteredName += "R"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_s]:
                    if enteredName == " ":
                        enteredName = "S"
                    elif len(enteredName) < maxChars:
                        enteredName += "S"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_t]:
                    if enteredName == " ":
                        enteredName = "T"
                    elif len(enteredName) < maxChars:
                        enteredName += "T"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_u]:
                    if enteredName == " ":
                        enteredName = "U"
                    elif len(enteredName) < maxChars:
                        enteredName += "U"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_v]:
                    if enteredName == " ":
                        enteredName = "V"
                    elif len(enteredName) < maxChars:
                        enteredName += "V"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_w]:
                    if enteredName == " ":
                        enteredName = "W"
                    elif len(enteredName) < maxChars:
                        enteredName += "W"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_x]:
                    if enteredName == " ":
                        enteredName = "X"
                    elif len(enteredName) < maxChars:
                        enteredName += "X"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_y]:
                    if enteredName == " ":
                        enteredName = "Y"
                    elif len(enteredName) < maxChars:
                        enteredName += "Y"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                elif keys[K_z]:
                    if enteredName == " ":
                        enteredName = "Z"
                    elif len(enteredName) < maxChars:
                        enteredName += "Z"
                    self.menuItems = [menuItem(enteredName),menuItem("Done")]
                    self.menuItems[self.selected].isSelected = True
                    self.displayMenu()
                    self.title.display(self.screen)
                
            self.moveSelection(keys)
            
            if keys[K_RETURN]:    
                    if self.selected == 1:
                        self.runMenu = False
                        menu.displayMenu()
                        menu.title.display(self.screen)
                        time.sleep(self.sleepTime)
                        return enteredName
                        
            pygame.display.update()
            time.sleep(self.sleepTime)
            
class instructionScreen(menu):    
    def __init__(self, screen):
        menu.__init__(self,screen)

    def run(self, menu):
        self.menuItems = [menuItem("-Press Space to Jump"), menuItem("-Press Arrow Keys to Move"),menuItem("-You cannot change your"),menuItem("direction once you jump"),menuItem("Done")]
        self.menuItems[len(self.menuItems)-1].isSelected = True
        self.title = title("Instructions:")
        self.displayMenu()
        time.sleep(self.sleepTime)
        self.title.display(self.screen)
        while self.runMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    exit(0)
                    
            keys=pygame.key.get_pressed()

            if keys[K_RETURN]:
                    if not menu.mute:
                            menu.yes.play()
                            time.sleep(self.beepTime)
                    self.runMenu = False
                    menu.displayMenu()
                    menu.title.display(self.screen)
                    time.sleep(self.sleepTime)
                    break
                        
            pygame.display.update()
            time.sleep(self.sleepTime)
