import pygame
import random
from gameBasic import *

WIDTH = 480
HEIGHT = 360
FPS = 30

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.display.flip()

pygame.quit()
