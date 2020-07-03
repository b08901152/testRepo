import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


SCREENWIDTH = 700
SCREENHEIGHT = 400
FPS = 40


def drawScreen(screen, player1, player2, background, bullets1, bullets2):
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()
    screen.blit(background, (0, 0))
    for bullet in bullets1:
        bullet.draw(screen)
    for bullet in bullets2:
        bullet.draw(screen)


def createCharacter():
    Image = pygame.image.load(
        '../lib/image/player1.png').convert_alpha()  # player1要用的圖
    player1 = Player("harry", Image, 200, 200, 64, 64, (10, 10))

    Image2 = pygame.image.load(
        '../lib/image/player2.png').convert_alpha()  # player1要用的圖
    player2 = Player("hary", Image2, 200, 200, 64, 64, (10, 10))
    return player1, player2


class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y, w, h, speed=(0, 0)):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(image, (int(w), int(h)))
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.speed = speed
        self.life = 70
        self.facing = [-1, 0]
        self.last_facing = [-1, 0]

    def moveUp(self):
        if not self.rect.top < 0:
            self.rect.y -= self.speed[1]

    def moveDown(self):
        if not self.rect.bottom >= SCREENHEIGHT:
            self.rect.y += self.speed[1]

    def moveLeft(self):
        if not self.rect.left < 0:
            self.rect.x -= self.speed[0]

    def moveRight(self):
        if not self.rect.right > SCREENWIDTH:
            self.rect.x += self.speed[0]

    def draw(self, screen):
        pygame.draw.rect(screen, RED,
                         (self.rect.x, self.rect.y-5, 70, 5))
        pygame.draw.rect(screen, GREEN,
                         (self.rect.x, self.rect.y-5, self.life, 5))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def moveHandleP1(self, keys, bullets):
        if keys[pygame.K_LEFT]:
            self.moveLeft()
            self.facing = [-1, 0]
        if keys[pygame.K_RIGHT]:
            self.moveRight()
            self.facing = [1, 0]
        if keys[pygame.K_UP]:
            self.moveUp()
            self.facing = [0, -1]
        if keys[pygame.K_DOWN]:
            self.moveDown()
            self.facing = [0, 1]
        if not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]\
           and keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.facing = self.last_facing
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(round(self.rect.x+self.w//2),
                                  round(self.rect.y+self.h//2),
                                  self.facing))
        self.last_facing = self.facing

    def moveHandleP2(self, keys, bullets):
        if keys[pygame.K_a]:
            self.moveLeft()
            self.facing = [-1, 0]
        if keys[pygame.K_d]:
            self.moveRight()
            self.facing = [1, 0]
        if keys[pygame.K_w]:
            self.moveUp()
            self.facing = [0, -1]
        if keys[pygame.K_s]:
            self.moveDown()
            self.facing = [0, 1]
        if not keys[pygame.K_a] and keys[pygame.K_d]\
           and keys[pygame.K_w] and keys[pygame.K_s]:
            self.facing = self.last_facing
        if keys[pygame.K_f]:
            bullets.append(Bullet(round(self.rect.x+self.w//2),
                                  round(self.rect.y+self.h//2),
                                  self.facing))
        self.last_facing = self.facing


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, facing):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (240, 240, 240)
        self.facing = facing
        self.vel = (100 * facing[0], 100*facing[1])
        if(facing[0]):
            self.l = 20
            self.w = 1
        if(facing[1]):
            self.l = 1
            self.w = 20

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.l, self.w))


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
