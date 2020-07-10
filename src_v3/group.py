import pygame
class Group(pygame.sprite.Group):
    def draw(self,screen):
        for sprites in self:
            sprites.draw(screen)

    