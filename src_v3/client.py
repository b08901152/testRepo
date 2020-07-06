import pygame
from network import Network
from player import Player


pygame.init()
pygame.mixer.init()

width  = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (width, height))

my_sprites    = pygame.sprite.Group()




def redrawWindow(screen, me, other):
    #screen.fill((255, 255, 255))
    me.draw(screen)
    other.draw(screen)
    pygame.display.update()


def main():
    run = True
    n = Network()
    me = n.getP()
    my_sprites.add(me)

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        other = n.send(me)
        other_sprites = pygame.sprite.Group()
        other_sprites.add(other)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        me.moveHandle(keys)
        screen.blit(background, (0, 0))

        #my_sprites.draw(screen)
        #other_sprites.draw(screen)
        redrawWindow(screen, me, other)


main()
