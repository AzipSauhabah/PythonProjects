# Azip Sauhabah
#Azip Sauhabah

# subscreen.py

import pygame, os, sys, load, time
from pygame.locals import *

# subscreen class
class subscreen(object):
    def __init__(self):
        self.subscreen1 = load.load_image("subscreen1.png")
        self.subscreen2 = load.load_image("subscreen2.png")
        self.subscreen3 = load.load_image("subscreen3.png")
        self.subscreen4 = load.load_image("subscreen4.png")
        self.subscreen = [self.subscreen1,self.subscreen2]
        self.subscreen_d = [self.subscreen3,self.subscreen4]
        self.index1 = 0
        self.index2 = 0
        self.sub1 = False
        self.sub2 = False
        self.start = False
        self.startTime = 0
        self.pause = False
        self.enter = False
        self.restart = False

    # init function for restart
    def init(self):
        self.index1 = 0
        self.index2 = 0
        self.sub1 = False
        self.sub2 = False
        self.start = False
        self.startTime = 0
        self.pause = False
        self.up = False
        self.down = False
        self.enter = False
        self.restart = False

    # run function for subscreen menu
    def run(self,screen,event,key,kirby,menu):
        self.checkInput(event,kirby,key)
        if kirby.life <= 0 and self.sub2 == False and self.start == False:
            self.start = True
            self.sub1 = False
            self.startTime = time.time()
        # triggers the subscreen2 after the kirby dies (2s)
        if time.time()-self.startTime > 1 and kirby.life <= 0: self.sub2 = True
        # subscreen 1
        if self.sub1 and self.sub2 == False:
            screen.blit(self.subscreen[self.index1%2],(0,0))
            if self.enter and self.index1%2 == 0: # continue
                self.sub1, self.pause = False, False
            if self.enter and self.index1%2 == 1: # exit to menu
                menu.start = False
                self.sub1, self.pause, self.restart = False, False, True
        # subscreen 2
        if self.sub2:
            screen.blit(self.subscreen_d[self.index2%2],(0,0))
            if self.enter and self.index2%2 == 0: # restart
                self.init()
                self.restart = True
            if self.enter and self.index2%2 == 1: # exit to menu
                menu.start = False
                self.restart = True

    # checks the keyboard input
    def checkInput(self,event,kirby,key):   
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.sub1: self.index1 += 1
                if self.sub2: self.index2 += 1
            if event.key == K_UP:
                if self.sub1: self.index1 -= 1
                if self.sub2: self.index2 -= 1 
            if event.key == K_RETURN:
                self.enter = True
        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter = False
        # press 'esc' enter subscreen
        if key[K_ESCAPE] and kirby.life > 0:
            self.pause = True
            self.sub1 = True
            
        
                
        
        
