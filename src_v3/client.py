import pygame
from network import Network
from player import Player
import gun 
from gamebasic import *
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Client")
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))

all_sprites = pygame.sprite.Group()
gun_sprites = pygame.sprite.Group()
clip_sprites = pygame.sprite.Group()

guns = gun.createGuns(number=3)
for i in range(3):
    gun_sprites.add(guns[i])
    all_sprites.add(guns[i])


def redrawWindow(screen, me, other):
    screen.blit(background, (0, 0))
    me.draw(screen)
    other.draw(screen)
    guns[0].draw(screen)
    clip_sprites.draw(screen)
    pygame.display.update()

def main():
    run = True
    n = Network()
    me = n.getP()
    all_sprites.add(me)

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        me.moveHandle(keys,gun_sprites)
        all_sprites.update()

        other = n.send(me)
        all_sprites.add(other)
        redrawWindow(screen, me, other)
        #all_sprites.draw()
        all_sprites.remove(other)


main()
