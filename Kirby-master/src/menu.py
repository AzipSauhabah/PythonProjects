# Azip Sauhabah
#Azip Sauhabah

# menu.py

import pygame, os, sys, load
from pygame.locals import *

# start menu class
class menu(object):
    def __init__(self):
        self.menu1 = load.load_image("menu1.png")
        self.menu2 = load.load_image("menu2.png")
        self.menu3 = load.load_image("menu3.png")
        self.menu = [self.menu1,self.menu2,self.menu3]
        self.instruction = load.load_image("instruction.png")
        self.index = 0
        self.start = False
        self.info = False
        self.menuSound = load.load_sound("menuDing.WAV")
        self.enter = False

    # the run function
    def run(self,screen,event,key):
        if event.type == KEYDOWN:
            if event.key == K_DOWN and not self.info:
                self.index += 1
            if event.key == K_UP and not self.info:
                self.index -= 1
            if event.key == K_RETURN:
                self.enter = True
        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter = False
        screen.blit(self.menu[self.index%3],(0,0))
        if self.info == False:
            if self.index%3 == 0 and self.enter: # start game
                self.start = True
            elif self.index%3 == 2 and self.enter: # exit game
                sys.exit()
            elif self.index%3 == 1 and self.enter: # instruction
                self.info = True
        if self.info: # if instruction selected, draw the info image
            screen.blit(self.instruction,(50,25))
        if self.info and key[pygame.K_ESCAPE]:
            self.info = False
        
        
