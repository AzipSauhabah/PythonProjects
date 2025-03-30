# Azip Sauhabah
#Azip Sauhabah

# load.py
# functions for loading resources

from pygame.locals import *
import os, pygame

def load_image(name):
    path = os.path.join('Kirby-master','data','images',name)
    image = pygame.image.load(path)
    return image

def load_scene(name):
    path = os.path.join('Kirby-master','data','scenery',name)
    scenery = pygame.image.load(path)
    return scenery

def load_font(name,size):
    path = os.path.join('Kirby-master','data','fonts',name)
    font = pygame.font.Font(path,size)
    return font

def load_sound(name):
    path = os.path.join('Kirby-master','data','sounds',name)
    sound = pygame.mixer.Sound(path)
    return sound

def load_music(name):
    path = os.path.join('Kirby-master','data','music',name)
    music = pygame.mixer.Sound(path)
    return music
