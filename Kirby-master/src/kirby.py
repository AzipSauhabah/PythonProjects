# Azip Sauhabah
#Azip Sauhabah

# kirby.py

import pygame, load, random, spriteGroup, block, time
from pygame.locals import *

# Class Kirby, create the main character
class kirby(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadMove()
        self.loadJump()
        self.loadSpark()
        self.loadIcon()
        self.init()

    # Init properties
    def init(self):
        self.x, self.y = 300, 336
        self.speed_x, self.speed_y = 0, 0
        self.speed_x2, self.speed_y2 = 0, 0
        self.frame_w = 0
        self.frame_f = 0
        self.frame_turn = 0
        self.frame_blow = -1
        self.left = False
        self.gravity = 0.8
        self.gravity2 = 0.1
        self.airstate = False
        self.flystate = False
        self.blowstate = False
        self.doubleJump = False
        self.djTime = 0
        self.life = 6
        self.frame_spark = 0
        self.fire = False
        self.frame_inv = 0
        self.invincible = False
        self.dead = False
        self.sparkCount = 4
        self.score = 0

    # Init images for move
    def loadMove(self):
        self.kirby1 = load.load_image("Kirby1.png")
        self.kirbyMove1 = load.load_image("KirbyMove1.png")
        self.kirbyMove2 = load.load_image("KirbyMove2.png")
        self.kirbyMove3 = load.load_image("KirbyMove3.png")
        self.kirbyMove4 = load.load_image("KirbyMove4.png")
        self.kirbyMove5 = load.load_image("KirbyMove5.png")
        self.kirbyMove6 = load.load_image("KirbyMove6.png")
        self.kirbyMove7 = load.load_image("KirbyMove7.png")
        self.kirbyMove8 = load.load_image("KirbyMove8.png")
        self.kirbyMove9 = load.load_image("KirbyMove9.png")
        self.kirbyMove10 = load.load_image("KirbyMove10.png")
        self.kirbyMove = [self.kirby1, self.kirbyMove1,
        self.kirbyMove2, self.kirbyMove3, self.kirbyMove4, 
        self.kirbyMove5, self.kirbyMove6, self.kirbyMove7, 
        self.kirbyMove8, self.kirbyMove9, self.kirbyMove10]

    # Init images for jump
    def loadJump(self):
        self.kirbyJump1 = load.load_image("kirbyJump1.png")
        self.kirbyJump7 = load.load_image("kirbyJump7.png")


    # Init images for spark
    def loadSpark(self):
        self.spark1 = load.load_image("spark1.png")
        self.spark2 = load.load_image("spark2.png")
        self.spark3 = load.load_image("spark3.png")
        self.sparkle1 = load.load_image("sparkle1.png")
        self.sparkle2 = load.load_image("sparkle2.png")
        self.sparkle3 = load.load_image("sparkle3.png")
        self.spark = [self.spark1,self.spark2,self.spark3]
        self.sprite = block.Block(16,16)
        self.sprite_spark = block.Block(60,60)

    # Init images for icons
    def loadIcon(self):
        self.blood1 = load.load_image("blood1.png")
        self.blood2 = load.load_image("blood2.png")
        self.sparkIcon = load.load_image("sparkIcon.png")
        self.font = load.load_font("Transformers.ttf",25)

    # Defines kirby's movement
    def update(self,event,screen,key,spriteGroup):
        self.kirbyControl(screen,key,spriteGroup)
        self.checkState(screen,key,spriteGroup)
        if pygame.sprite.spritecollide(self.sprite,spriteGroup.enemies,False)\
                and self.invincible == False:
            self.invincible = True
            self.life -= 1
        if self.invincible:
            self.frame_inv += 1
        if self.frame_inv > 40:
            self.invincible = False
            self.frame_inv = 0
        self.drawLife(screen)
        self.drawSpark(screen)
        self.drawScore(screen)
        self.score += 1

    # Triggers the spark shield when called
    def fireSpark(self,screen,spriteGroup):
        self.sprite_spark.rect.x = self.x-17
        self.sprite_spark.rect.y = self.y-17
        spriteGroup.sparkshield.add(self.sprite_spark)
        screen.blit(self.spark[self.frame_spark%3],(self.x-21,self.y-21))
        self.frame_spark += 1

    # The control function for Kirby
    def kirbyControl(self,screen,key,spriteGroup):
        # fire spark
        if key[pygame.K_SPACE] and self.fire == False and self.sparkCount > 0:
            self.fire = True
            self.sparkCount -= 1
        if self.fire:
            self.fireSpark(screen,spriteGroup)
        if self.frame_spark > 150:
            self.fire = False
            self.frame_spark = 0
            spriteGroup.sparkshield.empty()
        if self.invincible == False:
            # blit different images according to the frame
            if self.airstate == False:
                screen.blit(self.kirbyMove[self.frame_w%11],(self.x,self.y))
            elif self.airstate == True and self.speed_y>0:
                screen.blit(self.kirbyJump1, (self.x, self.y))
            elif self.airstate == True and self.speed_y<=0:
                screen.blit(self.kirbyJump7, (self.x, self.y))
        else: # if Kirby is damaged, flash the images
            if self.airstate == False and self.frame_inv % 3 == 0:
                screen.blit(self.kirbyMove[self.frame_w%11],(self.x,self.y))
            elif self.airstate and self.speed_y>0 and self.frame_inv % 3 == 0:
                screen.blit(self.kirbyJump1, (self.x, self.y))
            elif self.airstate and self.speed_y<=0 and self.frame_inv % 3 == 0:
                screen.blit(self.kirbyJump7, (self.x, self.y))

    # The state function for Kirby
    def checkState(self,screen,key,spriteGroup):
        # Press 'Z' to jump and double jump
        if key[pygame.K_z] and self.airstate == False:
            self.djTime = time.time()
            self.speed_y = 10
            self.airstate = True
        elif self.airstate and key[pygame.K_z] and self.doubleJump == False:
            if time.time()-self.djTime > 0.3:
                self.doubleJump = True
                self.speed_y = 8
        # controled by gravity when in the air
        if self.airstate == True:
            self.y -= self.speed_y
            self.speed_y -= self.gravity      
        self.sprite.rect.x = self.x+5
        self.sprite.rect.y = self.y+5      
        if self.y > 336:
            self.airstate = False
            self.flystate = False
            self.doubleJump = False
            self.speed_y = 0
            self.speed_y2 = 0
            self.y = 336
        if self.y < 336:
            self.airstate = True
        self.frame_w += 1
        spriteGroup.player.add(self.sprite)

    # Draw life icons
    def drawLife(self,screen):
        w = self.blood1.get_width()
        x = 300-3*w
        y = 374
        for i in range(self.life):
            screen.blit(self.blood1,(x+i*w,y))
        for i in range(6-self.life):
            screen.blit(self.blood2,(x+5*w-i*w,y))

    # Draw spark icons
    def drawSpark(self,screen):
        w = self.sparkIcon.get_width()
        x = 25
        y = 30
        for i in range(self.sparkCount):
            screen.blit(self.sparkIcon,(x+i*w,y))

    def drawScore(self,screen):
        text = "SCORE: %d" % self.score
        text = self.font.render(text,True,(255,255,255))
        screen.blit(text,(25,10))    
