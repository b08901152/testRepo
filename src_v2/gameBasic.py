import pygame
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


SCREENWIDTH = 700
SCREENHEIGHT = 700
FPS = 40


def bulletsHandle(bullets):
    for bullet in bullets:
        bullet.x += bullet.vel[0]
        bullet.y += bullet.vel[1]


def drawScreen(screen, player1, player2, background, bullets1, bullets2, weapons):
    player1.draw(screen)
    for weapon in weapons:
        weapon.draw(screen, player1)
    # player2.draw(screen)

    pygame.display.flip()
    screen.blit(background, (0, 0))
    for bullet in bullets1:
        bullet.draw(screen)



def createCharacter():
    Image = pygame.image.load(
        '../lib/image/player1.png').convert_alpha()  # player1要用的圖
    player1 = Player("harry", Image, 200, 200, 64, 64, (10, 10))

    Image2 = pygame.image.load(
        '../lib/image/player2.png').convert_alpha()  # player2要用的圖
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
        self.facing = 0
        self.middleX = self.x+self.w//2
        self.middleY = self.y+self.h//2
        self.weapons = []

    def moveUp(self):
        if not self.rect.top < 0:
            self.rect.y -= self.speed[1]
            self.y -= self.speed[1]
            self.middleY = self.y+self.h//2

    def moveDown(self):
        if not self.rect.bottom >= SCREENHEIGHT:
            self.rect.y += self.speed[1]
            self.y += self.speed[1]
            self.middleY = self.y+self.h//2

    def moveLeft(self):
        if not self.rect.left < 0:
            self.rect.x -= self.speed[0]
            self.x -= self.speed[0]
            self.middleX = self.x+self.w//2

    def moveRight(self):
        if not self.rect.right > SCREENWIDTH:
            self.rect.x += self.speed[0]
            self.x += self.speed[0]
            self.middleX = self.x+self.w//2
            
    def pickUpWeapon(self,weapons):
        for weapon in weapons:
            if pygame.sprite.collide_rect(weapon, self):
                weapon.is_taken = True
                self.weapons.append(weapon)

    def draw(self, screen):
        pygame.draw.rect(screen, RED,
                         (self.rect.centerx-self.w/2, self.rect.centery-self.h/1.5, 70, 5))
        pygame.draw.rect(screen, GREEN,
                         (self.rect.centerx-self.w/2, self.rect.centery-self.h/1.5, self.life, 5))

        self.facing = self.calFacing()
        rotate_image = pygame.transform.rotate(
            self.image, -self.facing*180/math.pi)
        self.rect = rotate_image.get_rect(
            center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotate_image, (self.rect.x, self.rect.y))


    def moveHandleP2(self, keys, bullets, weapons):
        if keys[pygame.K_a]:
            self.moveLeft()
        if keys[pygame.K_d]:
            self.moveRight()
        if keys[pygame.K_w]:
            self.moveUp()
        if keys[pygame.K_s]:
            self.moveDown()
        if keys[pygame.K_SPACE]:
            self.pickUpWeapon(weapons)
        if pygame.mouse.get_pressed()[0]:
            bullets.append(Bullet(round(self.x+self.w//2),
                                  round(self.y+self.h//2),
                                  self.facing))

    def calFacing(self):
        theta = 0
        pos = pygame.mouse.get_pos()
        deltaY = (pos[1] - self.middleY)
        deltaX = (pos[0] - self.middleX)

        if deltaX == 0 and deltaY > 0:
            return math.pi/2
        elif deltaX == 0 and deltaY < 0:
            return math.pi*3/2
        theta = math.atan(deltaY/deltaX)
        if deltaX < 0:
            theta += math.pi
        return theta


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, facing):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (240, 240, 240)
        self.facing = facing
        self.speed = 150
        self.vel = [self.speed *
                    math.cos(self.facing), self.speed * math.sin(self.facing)]
        self.l = 30
        self.start_pos = [self.x, self.y]
        self.end_pos = [
            self.x+self.l * math.cos(self.facing), self.y + self.l * math.sin(self.facing)]

    def draw(self, window):
        # line(surface, color, start_pos, end_pos, width) -> Rect
        pygame.draw.line(window, self.color, self.start_pos, self.end_pos, 1)
        self.start_pos[0] += self.vel[0]
        self.start_pos[1] += self.vel[1]
        self.end_pos[0] += self.vel[0]
        self.end_pos[1] += self.vel[1]


class Gun(pygame.sprite.Sprite):
    def __init__(self, name, x, y, w, h, gun_image, atkPoint):
        super().__init__()
        self.name = name
        self.image = pygame.transform.scale(gun_image, (int(2*w), int(2*h)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_ammunition = 10  # 彈藥限制
        self.ammunition = 10  # 現在的彈藥
        self.shoot_delay = 500  # 兩發子彈的間隔時間
        self.last_shoot_time = 0
        self.atkPoint = atkPoint
        self.is_taken = False

    def update(self, player):
        self.rect.centerx = player.middleX
        self.rect.centery = player.middleY
        self.rect.x = player.x
        self.rect.y = player.y


    def new_bullet(self, position):
        if pygame.time.get_ticks() - self.last_shoot_time > self.shoot_delay:
            self.last_shoot_time = pygame.time.get_ticks()
            return Bullet(position)

    def draw(self, screen,player):
        if not self.is_taken:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else: 
            facing = player.calFacing()
            self.update(player)
            rotate_image = pygame.transform.rotate(
                self.image, - facing*180/math.pi)
            screen.blit(rotate_image, (self.rect.x, self.rect.y))


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
