# Azip Sauhabah
#Azip Sauhabah

# spriteGroup.py

from pygame.locals import *
import pygame

# spriteGroup class
class spriteGroup(object):
    def __init__(self):
        # init sprite groups for checking collision
        self.player = pygame.sprite.Group()
        self.handCursor = pygame.sprite.Group()
        self.fist = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.landscape = pygame.sprite.Group()
        self.dragable = pygame.sprite.Group()
        self.sparkshield = pygame.sprite.Group()
        self.circlePixel = pygame.sprite.Group()
        self.powerup = pygame.sprite.Group()
