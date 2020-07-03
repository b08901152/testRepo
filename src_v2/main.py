import pygame
import random
from gameBasic import *

WIDTH = 1400
HEIGHT = 800
FPS = 40

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()



failImage = pygame.image.load(
    '../lib/image/player1.png').convert_alpha()  # player1要用的圖
man = Player("harry", failImage, 200, 200, 64, 64, (10, 10))

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        man.moveLeft()
    if keys[pygame.K_RIGHT]:
        man.moveRight()
    if keys[pygame.K_UP]:
        man.moveUp()
    if keys[pygame.K_DOWN]:
        man.moveDown()

    screen.fill(BLACK)
    drawScreen(screen,man,None)

pygame.quit()
