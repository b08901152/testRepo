import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, up, down, left, right, attack, change, pick, x, y, w, h, speed=(0, 0)):
        super().__init__()

    def draw(self, screen):
        pass

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
