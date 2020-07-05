import pygame
import random
from gameBasic import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Twilight War")
clock = pygame.time.Clock()
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
weaponImage2 = pygame.image.load("../lib/image/machine_gun.png")
weaponImage3 = pygame.image.load("../lib/image/knife.png")
weaponImage = pygame.image.load("../lib/image/gun.png")


player1, player2 = createCharacter()
weapons = []
weapons.append(Gun('normal', player1.rect.x,
                   player1.rect.y, 15, 15, weaponImage, 10))
weapons.append(Gun('normal', player1.rect.x+100,
                   player1.rect.y+100, 30, 30, weaponImage2, 10))
weapons.append(Gun('normal', player1.rect.x+300,
                   player1.rect.y+300, 30, 30, weaponImage3, 10))
weapons.append(Gun('normal', player1.rect.x+200,
                   player1.rect.y+200, 30, 30, weaponImage3, 10))
bullets1 = []
bullets2 = []
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player1.moveHandleP2(keys, bullets1, weapons)
    # player2.moveHandleP2(keys, bullets2)

    bulletsHandle(bullets1)

    drawScreen(screen, player1, None, background, bullets1, None, weapons)

pygame.quit()
