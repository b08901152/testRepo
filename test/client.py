import pygame
from network import Network
from player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (width, height))

def drawScreen(screen, player1, player2):
    pygame.display.flip()
    screen.blit(background, (0, 0))
    player1.draw(screen)
    player2.draw(screen)

running = True
n = Network()
p = n.getP()
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    p2 = n.send(p)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    p.moveHandleP2(keys)
    # player2.moveHandleP2(keys, player2.bullets)

    drawScreen(win, p, p2)

pygame.quit()
