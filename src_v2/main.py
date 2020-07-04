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
weaponImage = pygame.image.load("../lib/image/gun.png")

player1, player2 = createCharacter()

gun=Gun('normal', player1.rect.x, player1.rect.y, 15, 15, weaponImage,10,player1)
all_weapons =  []

player1.weapon.append(gun)
all_weapons.append(gun)

player1.bullets = []
player2.bullets = []

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player1.moveHandleP2(keys)
    # player2.moveHandleP2(keys, player2.bullets)

    bulletsHandle(player1.bullets)
    bulletsHandle(player2.bullets)

    drawScreen(screen, player1, None, background, player1.bullets, player2.bullets, all_weapons)

pygame.quit()
