# 
# Azip Sauhabah

# main.py

import pygame, os, sys, kirby, handCursor, time
import spriteGroup, landscape, enemies, menu, load, subscreen, powerup
from pygame.locals import *

#Pygame Init
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((600,400),0,32)
pygame.display.set_caption("Kirby")
screen = pygame.display.get_surface()

# Create instances
kirby = kirby.kirby()
hand = handCursor.Hand()
clock = pygame.time.Clock()
spriteGroup = spriteGroup.spriteGroup()
landscape = landscape.landscape()
menu = menu.menu()
subscreen = subscreen.subscreen()

# Use Struct to store globals
class Struct: pass
data = Struct()
data.menuMusic = load.load_sound("menu.wav")
data.gameMusic = load.load_sound("game.wav")
data.event = pygame.event.poll()
data.key = pygame.key.get_pressed()
data.mouse_pos = pygame.mouse.get_pos()
data.mouseEvent = pygame.mouse.get_pressed()

# Add Pikey
def addPikey():
    if kirby.frame_w % 173 == 50:
        pikey = enemies.pikey(600,336)
        data.pikeyList.append(pikey)
    for p in data.pikeyList:
        p.movement(screen,spriteGroup,hand,data.mouseEvent,data.key)
        if p.x < -26:
            data.pikeyList.remove(p)
            spriteGroup.enemies.remove(p.sprite)
        if p.dead:
            data.pikeyList.remove(p)
            spriteGroup.enemies.remove(p.sprite)
# Add Shotzo
def addShotzo():
    if kirby.frame_w % 253 == 0:
        shotzo = enemies.shotzo(600,336)
        data.shotzoList.append(shotzo)
    for s in data.shotzoList:
        s.movement(screen,spriteGroup,kirby)
        if s.frame % 67 == 15:
            bullet = enemies.bullet(s.x,s.y,s.dir)
            data.bulletList.append(bullet)
        if s.x < -26:
            data.shotzoList.remove(s)
            spriteGroup.enemies.remove(s.sprite1)
    for b in data.bulletList:
        b.shoot(screen,spriteGroup)
        if b.dead:
            data.bulletList.remove(b)
            spriteGroup.enemies.remove(b.sprite)
        elif b.x < -26 or b.x > 626:
            spriteGroup.enemies.remove(b.sprite)

# Add WaddleDee
def addWaddleDee():
    if kirby.frame_w % 211 == 20:
        waddleDee = enemies.waddleDee(600,336)
        data.waddleDeeList.append(waddleDee)
    for dee in data.waddleDeeList:
        dee.movement(screen,spriteGroup,hand,data.mouseEvent,data.key)
        if dee.x < -26:
            data.waddleDeeList.remove(dee)
            spriteGroup.enemies.remove(dee.sprite)
        if dee.dead:
            data.waddleDeeList.remove(dee)
            spriteGroup.enemies.remove(dee.sprite)

# Add WaddleDoo
def addWaddleDoo():
    if kirby.frame_w % 197 == 66:
        waddleDoo = enemies.waddleDoo(600,336)
        data.waddleDooList.append(waddleDoo)
    for doo in data.waddleDooList:
        doo.movement(screen,spriteGroup,hand,data.mouseEvent,data.key)
        if doo.x < -26:
            data.waddleDooList.remove(doo)
            spriteGroup.enemies.remove(doo.sprite)
        if doo.dead:
            data.waddleDooList.remove(doo)
            spriteGroup.enemies.remove(doo.sprite)

# Add Bird
def addBird():
    if kirby.frame_w % 217 == 30:
        bird = enemies.bird(600,300)
        data.birdList.append(bird)
    for b in data.birdList:
        b.movement(screen,spriteGroup,hand,data.mouseEvent)
        if b.x < -26:
            data.birdList.remove(b)
            spriteGroup.enemies.remove(b.sprite)
        if b.dead:
            data.birdList.remove(b)
            spriteGroup.enemies.remove(b.sprite)

# Add Flame
def addFlame():
    if kirby.frame_w % 183 == 90:
        flame = enemies.flame(600,320)
        data.flameList.append(flame)
    for f in data.flameList:
        f.movement1(screen,spriteGroup,hand,data.mouseEvent,kirby,data.key)
        if f.x < -26 or f.dead:
            data.flameList.remove(f)
            spriteGroup.enemies.remove(f.sprite1)
            spriteGroup.enemies.remove(f.sprite2)


# Add Potion
def addPotion():
    if kirby.frame_w % 523 == 300:
        potion = powerup.potion(600,326)
        data.potionList.append(potion)
    for p in data.potionList:
        p.movement(screen,spriteGroup,kirby)
        if p.x < -36 or p.dead:
            data.potionList.remove(p)
            spriteGroup.powerup.remove(p.sprite)

# Add Spark
def addSpark():
    if kirby.frame_w % 611 == 300:
        spark = powerup.spark(600,326)
        data.sparkList.append(spark)
        spark.time = time.time()
    for s in data.sparkList:
        s.movement(screen,spriteGroup,kirby,hand,data.mouseEvent,data.key)
        if s.x < -36 or s.dead:
            data.sparkList.remove(s)
            spriteGroup.powerup.remove(s.sprite)
        if time.time()-s.time > 20:
            s.dead = True
            
# Add Objects
def addObject():
    addPikey()
    addShotzo()
    addWaddleDee()
    addWaddleDoo()
    addBird()
    addFlame()
    addPotion()
    addSpark()

# Init function to restart the game
def init():
    data.startGame = False
    data.pause = False
    data.shotzoList = []
    data.pikeyList = []
    data.bulletList = []
    data.waddleDeeList = []
    data.waddleDooList = []
    data.birdList = []
    data.flameList = []
    data.potionList = []
    data.sparkList = []
    data.start = False
    data.restart = False
    data.play1 = False
    data.play2 = False
    spriteGroup.enemies.empty()
    spriteGroup.sparkshield.empty()
    kirby.init()

# the run function in the mainloop
def run(event,key,mouse_pos,mouseEvent):
    if data.restart:
        init()
        subscreen.init()
        hand.fistState = False
    if data.start: # Start the game
        if data.play2 == False:
            data.gameMusic.play(-1)
            data.play2 = True
        data.menuMusic.stop()
        if data.pause == False and kirby.life > 0:
            screen.fill((255,255,255))
            landscape.create(screen,spriteGroup) # load the background
            addObject()
            kirby.update(event,screen,key,spriteGroup) # Kirby's movement
            # mouse cursor
            hand.cursor(mouse_pos,mouseEvent,screen,kirby,spriteGroup,key)
        subscreen.run(screen,event,key,kirby,menu) # load subscreen
        clock.tick(20)
    else: # if the game is not started, show the menu
        data.gameMusic.stop()
        if data.play1 == False:
            data.menuMusic.play(-1)
            data.play1 = True
        menu.run(screen,event,key) # run menu
    pygame.display.update()

def mainloop():
    while 1:
        data.event = pygame.event.poll()
        data.key = pygame.key.get_pressed()
        data.mouse_pos = pygame.mouse.get_pos()
        data.mouseEvent = pygame.mouse.get_pressed()
        pygame.mouse.set_visible(False) # hide the cursor
        if data.event.type == QUIT:
            sys.exit()
        #Stores menu's and subscreen's properties into data
        data.start = menu.start
        data.pause = subscreen.pause
        data.restart = subscreen.restart
        run(data.event,data.key,data.mouse_pos,data.mouseEvent)
    
init()
mainloop()
