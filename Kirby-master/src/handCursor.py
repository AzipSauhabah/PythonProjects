# Azip Sauhabah
#Azip Sauhabah

# handCursor.py

from pygame.locals import *
import pygame, load, block
import kirby
import spriteGroup
import time
import math

class Hand(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadImage()
        self.frame_hand = 0
        self.grab = False
        self.circle_x = []
        self.circle_y = []
        self.block1 = block.Block(16,16)
        self.vector = (0,0)
        self.startPos = (0,0)
        self.endPos = (0,0)
        self.startTime = 0
        self.endTime = 0
        self.coordList = []
        self.fistState = False
        self.fistEnd = False
        self.x2, self.y2 = 0, 0
        self.sprite = block.Block(45,45)
        self.speed_y = 15
        self.frame = 0
        self.frame_end = 0
        self.brushState = False

    def loadImage(self):
        self.hand1 = load.load_image("hand1.png")
        self.hand2 = load.load_image("hand2.png")
        self.hand3 = load.load_image("hand3.png")
        self.hand4 = load.load_image("hand4.png")
        self.hand = [self.hand1,self.hand4]

        self.fist1 = load.load_image("fist1.png")
        self.fist2 = load.load_image("fist2.png")
        self.fist3 = load.load_image("fist3.png")
        self.fist4 = load.load_image("fist4.png")
        self.fist5 = load.load_image("fist5.png")
        self.fist = [self.hand1,self.fist1,self.fist2,self.fist3,
                     self.fist4,self.fist5,self.fist5,self.fist5,
                     self.fist5]
        self.brush = load.load_image("brush.png")
        self.particle = load.load_image("particle.png")

    # The hit function for the fist
    def hit(self,screen,spriteGroup):
        if self.y2 > 307:
            self.fistEnd = True
            self.y2 = 307
        elif self.fistEnd == False:
            self.y2 += self.speed_y
        if self.frame%9 != 7:
            self.frame += 1
        if self.fistEnd:
            spriteGroup.fist.empty()
            self.frame_end += 1
        if self.frame_end > 10:
            self.fistState = False
            self.frame_end = 0
            self.frame = 0
        screen.blit(self.fist[self.frame%9],(self.x2,self.y2))
        self.sprite.rect.x = self.x2+5
        self.sprite.rect.y = self.y2+10
        if self.fistEnd == False:
            spriteGroup.fist.add(self.sprite)

    # function for mouse control
    def mouseControl(self,pos,event,screen,kirby,spriteGroup,x,y,c_x,c_y,key):
        if event[0] == 1 and key[K_b] == 0:
            self.frame_hand = 1
            self.startPos = (x, y)
            self.startTime = time.time()
            self.fistState = False
            self.brushState = False
        elif event[0] == 0 and key[K_b] == 0:
            self.frame_hand = 0
            self.grab = False
            self.brushState = False
        # press the right button to trigger the fist state
        if event[2] == 1 and c_y < 307:
            self.fistState = True
            self.x2, self.y2 = c_x, c_y
            self.frame, self.frame_end = 0, 0
        self.mouseControl_draw(pos,event,screen,kirby,spriteGroup,key)
        
    def mouseControl_draw(self,pos,event,screen,kirby,spriteGroup,key):
        if key[K_b]:
            self.brushState = True
            if event[0] == 1:
                self.drawCircle(pos,event,screen,kirby,spriteGroup,key)
            if event[0] == 0:
                # create spark shield when drawing a circle
                if len(self.circle_x)>0 and not kirby.fire and kirby.sparkCount>0\
                    and self.checkCircle(self.circle_x,self.circle_y,kirby):
                    kirby.sparkCount -= 1
                    kirby.fire = True
                spriteGroup.circlePixel.empty()
                self.circle_x = []
                self.circle_y = []
            # draw the trace of the brush
            for i in xrange(len(self.circle_x)):
                x, y = self.circle_x[i], self.circle_y[i]
                screen.blit(self.particle,(x-8,y-8))
    
    def cursor(self,pos,event,screen,kirby,spriteGroup,key):
        x, y = pos
        self.x, self.y = x, y
        self.event = event
        c_x = x - self.hand1.get_width()*2/7
        c_y = y - self.hand1.get_height()*5/7
        self.block1.rect.x = x-8
        self.block1.rect.y = y-8
        spriteGroup.handCursor.add(self.block1)
        self.mouseControl(pos,event,screen,kirby,spriteGroup,x,y,c_x,c_y,key)
        if self.fistState == False:
            if not self.brushState:
                screen.blit(self.hand[self.frame_hand%2],(c_x,c_y))
            else: screen.blit(self.brush,(x,y))
            spriteGroup.fist.empty()
            self.fistEnd = False
        else: # if in fist state, call hit function
            self.hit(screen,spriteGroup)
        if self.grab: # if grabed, call createVector
            self.createVector(pos)
        # if released, init the vector
        elif self.grab == False and len(self.coordList) == 2:
            x1, y1 = self.coordList[0][0], self.coordList[0][1]
            x2, y2 = self.coordList[1][0], self.coordList[1][1]
            self.vector = ((x2-x1)/5.0,(y2-y1)/5.0)

    # drag function
    def drag(self,event,spriteGroup):
        if event[0] == 1:
            self.frame_hand = 1
        elif event[0] == 0:
            self.frame_hand = 0
            self.grab = False

    def drawCircle(self,pos,event,screen,kirby,spriteGroup,key):
        x, y = pos
        if event[0] == 1 and key[K_b]:
            block2 = block.Block(8,8)
            block2.rect.x = x-4
            block2.rect.y = y-4
            spriteGroup.circlePixel.add(block2)
            self.circle_x.append(x)
            self.circle_y.append(y)
        elif event[0] == 0 and key[K_b]:
            for element in spriteGroup.circlePixel:
                spriteGroup.circlePixel.remove(element)

    def checkCircle(self,xList,yList,kirby):
        total = 0
        for i in xrange(len(xList)):
            x, y = xList[i], yList[i]
            value = math.hypot(x-kirby.x-13,y-kirby.y-13)
            if value < 10 or value > 60:
                return False
            if i > 0:
                value = math.hypot(x-xList[i-1],y-yList[i-1])
                total += value
        d = math.hypot(xList[0]-xList[-1],yList[0]-yList[-1])
        if d > 30:
            return False
        if total < 50:
            return False
        return True

    # This function add the latest two coords to the list
    def createVector(self,pos):
        x,y = pos
        if self.grab:
            if len(self.coordList) > 1:
                self.coordList.pop(0)
            self.coordList.append((x,y))
        
            
            
