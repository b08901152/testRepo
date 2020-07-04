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
weapon = Gun('normal', player1.rect.x, player1.rect.y, 15, 15, weaponImage,10)
bullets1 = []
bullets2 = []
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player1.moveHandleP2(keys, bullets1)
    # player2.moveHandleP2(keys, bullets2)

    bulletsHandle(bullets1)
    bulletsHandle(bullets2)

    drawScreen(screen, player1, None, background, bullets1, bullets2, weapon)

pygame.quit()
