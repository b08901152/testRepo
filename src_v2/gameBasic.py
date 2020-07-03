import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, up, down, left, right, attack, change, pick, x, y, w, h, speed=(0, 0)):
        super().__init__()

    def draw(self, screen):


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
