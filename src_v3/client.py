import pygame
from network import Network
from player import Player
from group import Group
import gun 
from gamebasic import *
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Client")
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))

all_sprites  = Group()
gun_sprites  = Group()
clip_sprites = Group()

guns = gun.createGuns(number=3)
for i in range(3):
    gun_sprites.add(guns[i])
    all_sprites.add(guns[i])


def main():
    run = True
    n = Network()
    me = n.getP()
    all_sprites.add(me)

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        me.keys = pygame.key.get_pressed()
        me.mouse_get_pressed = pygame.mouse.get_pressed()
        me.mouse_get_pos = pygame.mouse.get_pos()
        me.moveHandle(gun_sprites,None)

        other = n.send(me)
        all_sprites.add(other)

        all_sprites.update()
        
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()

        all_sprites.remove(other)


main()
