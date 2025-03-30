# Azip Sauhabah
#Azip Sauhabah

# powerup.py

from pygame.locals import *
import pygame, load, block, random

# Potion Class
class potion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.potion = load.load_image("potion.png")
        self.sprite = block.Block(30,30)
        self.x = x
        self.y = y
        self.dead = False

    def movement(self,screen,spriteGroup,kirby):
        self.x -= 3
        screen.blit(self.potion,(self.x,self.y))
        # if collided with Kirby, add 2 more lives
        if pygame.sprite.spritecollide(self.sprite,spriteGroup.player,False):
            self.dead = True
            if kirby.life < 6:
                kirby.life += 1
        self.sprite.rect.x = self.x+6
        self.sprite.rect.y = self.y+6
        spriteGroup.powerup.add(self.sprite)

class spark(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.spark = load.load_image("powerup.png")
        self.sprite = block.Block(30,30)
        self.x = x
        self.y = y
        self.y_i = y
        self.speed_x = random.random()*2+3
        self.speed_y = random.random()*2+3
        self.dead = False
        self.time = 0
        self.localGrab = False
        self.v_x = 0
        self.v_y = 0
        self.start = False
        
    # drag function
    def drag(self,spriteGroup,hand,event,key):
        if pygame.sprite.spritecollide(self.sprite,spriteGroup.handCursor,
                         False) and event[0] == 1 and hand.grab == False\
                         and not key[K_b]:
            hand.grab = True
            self.localGrab = True
        if self.localGrab: # if grabed, follow the hand cursor
            self.x = hand.x-9
            self.y = hand.y-9
        # if released, create vectors
        if self.localGrab and hand.grab == False:
            self.localGrab = False

    # movement function
    def movement(self,screen,spriteGroup,kirby,hand,event,key):
        self.drag(spriteGroup,hand,event,key)
        w = self.spark.get_width()
        # bouncing in the screen
        if self.localGrab == False:
            if self.start:
                if self.x < 0 or self.x > 600-w:
                    self.speed_x = -self.speed_x
                if self.y < 0 or self.y > self.y_i:
                    self.speed_y = -self.speed_y
            if self.y > self.y_i:
                self.y = self.y_i
            self.x -= self.speed_x
            self.y -= self.speed_y
        if self.start == False and self.x <= 600-w:
            self.start = True
        screen.blit(self.spark,(self.x,self.y))
        if pygame.sprite.spritecollide(self.sprite,spriteGroup.player,False):
            self.dead = True
            kirby.sparkCount += 1
        self.sprite.rect.x = self.x + 3
        self.sprite.rect.y = self.y + 3
        spriteGroup.powerup.add(self.sprite)
        
