# Azip Sauhabah
#Azip Sauhabah

# block.py

from pygame.locals import *
import pygame

# Create the block class for checking collision
class Block(pygame.sprite.Sprite):
    def __init__(self,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill((255,0,0)) 
        self.rect = self.image.get_rect()
