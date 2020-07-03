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


player1, player2 = createCharacter()
bullets1 = []
bullets2 = []
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player1.moveHandleP1(keys, bullets1)
    # player2.moveHandleP2(keys, bullets2)

    bulletsHandle(bullets1)
    bulletsHandle(bullets2)

    drawScreen(screen, player1, None, background, bullets1, bullets2)

pygame.quit()
