import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def drawScreen(screen,player1, player2):
    player1.draw(screen)
    pygame.display.flip()
    
class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y, w, h, speed=(0, 0)):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (int(w), int(h)))
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.speed = speed
        self.life = 70

    def moveUp(self):
        self.rect.y -= self.speed[1]

    def moveDown(self):
        self.rect.y += self.speed[1]

    def moveLeft(self):
        self.rect.x -= self.speed[0]

    def moveRight(self):
        self.rect.x += self.speed[0]

    def draw(self, screen):
        pygame.draw.rect(screen, RED,
                         (self.rect.x, self.rect.y-10, 70, 5))
        pygame.draw.rect(screen, GREEN, 
                         (self.rect.x, self.rect.y-10, self.life, 5))
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()


class Gun(pygame.sprite.Sprite):
    def __init__(self, name, x, y, w, h, gun_image, hit):
        super().__init__()


class Knife(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()


class Clip(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()


class Hide(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()
