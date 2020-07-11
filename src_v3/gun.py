import random
import pygame
import math

from gamebasic import *


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, facing, atkPoint):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (240, 240, 240)
        self.facing = facing
        self.speed = 100
        self.vel = [self.speed *
                    math.cos(self.facing), self.speed * math.sin(self.facing)]
        self.l = 15
        self.width = 3
        self.rect = pygame.rect.Rect(self.x, self.y, self.l, self.width)
        self.atkPoint = atkPoint
        self.start_pos = [self.x, self.y]
        self.end_pos = [
            self.x+self.l * math.cos(self.facing), self.y + self.l * math.sin(self.facing)]

    def draw(self, window):
        # line(surface, color, start_pos, end_pos, width) -> Rect
        pygame.draw.line(window, self.color, self.start_pos,
                         self.end_pos, self.width)
        self.start_pos[0] += self.vel[0]
        self.start_pos[1] += self.vel[1]
        self.end_pos[0] += self.vel[0]
        self.end_pos[1] += self.vel[1]
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

    def hit(self, player):
        if pygame.sprite.collide_rect(player, self):
            player.life -= self.atkPoint
            pygame.time.delay(100)

def createGuns(number):
    guns = []
    weaponImage = pygame.image.load("../lib/image/gun.png")
    for i in range(number):
        gun = Gun('i', random.randint(0, SCREENWIDTH),  random.randint(0, SCREENHEIGHT),
                15, 15, weaponImage, 10, 10, None, shoot_delay=1000, isTaken=False)
        guns.append(gun)
    return guns

class Gun(pygame.sprite.Sprite):
    def __init__(self, name, x, y, w, h, image, max_ammunition, atkPoint, player, shoot_delay, isTaken):
        super().__init__()
        self.name = name
        
        image = pygame.transform.scale(image, (int(w), int(h)))
        self.imgString = pygame.image.tostring(image, "RGBA")
        
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.max_ammunition = max_ammunition   # 彈藥限制
        self.ammunition = max_ammunition       # 現在的彈藥
        self.shoot_delay = shoot_delay     # 兩發子彈的間隔時間
        self.last_shoot_time = 0
        self.atkPoint = atkPoint
        self.player = player
        self.isTaken = isTaken

    def update(self):
        if not self.isTaken:
            return
        else:
            self.rect.centerx = self.player.middleX
            self.rect.centery = self.player.middleY

    def attack(self):    # 攻擊，也就是射新的子彈
        if self.player and (pygame.time.get_ticks() - self.last_shoot_time > self.shoot_delay) and self.ammunition:
            self.last_shoot_time = pygame.time.get_ticks()
            self.ammunition -= 1
            self.player.bullets.append(Bullet(round(self.player.middleX),
                                              round(self.player.middleY),
                                              self.player.facing, self.atkPoint))
            return

    def draw(self, screen):
        self.update()
        image = pygame.image.fromstring(
            self.imgString, (self.w, self.h), "RGBA")
        
        if not self.isTaken:
            screen.blit(image, (self.rect.x, self.rect.y))
            return
        else:
            facing = self.player.calFacing()
            
            rotate_image = pygame.transform.rotate(
                image, -facing*180/math.pi)
            self.rect = rotate_image.get_rect(
                center=(self.rect.centerx, self.rect.centery))
            screen.blit(rotate_image, (self.rect.x, self.rect.y))
