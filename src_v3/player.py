import pygame
import math
from gamebasic import *

class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y, w, h, speed=(0, 0)):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        image = pygame.transform.scale(image, (int(w), int(h)))
        self.imgString = pygame.image.tostring(image, "RGBA")
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.speed = speed
        self.life = 70
        self.facing = 0
        self.middleX = self.x+self.w//2
        self.middleY = self.y+self.h//2
        self.weapons = []
        self.bullets = []
        self.can_pick = True
        self.present_weapon = None
        self.keys = None
        self.mouse_get_pressed = None
        self.mouse_get_pos = None


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

    def pickUpWeapon(self, weapons):
        pick_count = 0
        for weapon in weapons:
            if not weapon.isTaken and pygame.sprite.collide_rect(weapon, self) and pick_count == 0:
                weapon.isTaken = True
                weapon.player = self
                # 如果玩家武器數小於2 直接append到self
                if len(self.weapons) < 2:
                    self.weapons.append(weapon)

                    self.present_weapon = weapon
                    pick_count = 1
                #如果玩家武器數等於2 退掉第一個 再加新的一個
                elif len(self.weapons) == 2:
                    self.present_weapon.isTaken = False
                    self.weapons.remove(self.present_weapon)
                    self.weapons.append(weapon)
                    self.present_weapon = weapon
                    pick_count = 1

    def pickUpClips(self, clips):
        for clip in clips:
            if not clip.isTaken and pygame.sprite.collide_rect(clip, self):
                clip.isTaken = True
                self.weapons[0].ammunition += 10
        pygame.time.delay(100)

    def hiding(self, hides):
        for hide in hides:
            if not hide.isTaken and pygame.sprite.collide_rect(hide, self):
                hide.isTaken = True
            else:
                hide.isTaken = False
        return hide.isTaken

    def changeWeapon(self):
        if len(self.weapons) == 2:
            self.weapons[0], self.weapons[1] = self.weapons[1], self.weapons[0]
        print (self.weapons[0])

    def draw(self, screen):
        # 血條
        if self.life > 0:
            pygame.draw.rect(screen, RED,
                             (self.rect.centerx-self.w/2, self.rect.centery-self.h/1.5, 70, 5))
            pygame.draw.rect(screen, GREEN,
                             (self.rect.centerx-self.w/2, self.rect.centery-self.h/1.5, self.life, 5))
        else:
            pygame.draw.rect(screen, RED,
                             (self.rect.centerx-self.w/2, self.rect.centery-self.h/1.5, 70, 5))
        # 人物隨滑鼠旋轉
        
        image = pygame.image.fromstring(
            self.imgString, (self.w, self.h), "RGBA")
        rotate_image = pygame.transform.rotate(
            image, -self.facing*180/math.pi)
        self.rect = rotate_image.get_rect(
            center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotate_image, (self.rect.x, self.rect.y))

        if self.present_weapon :
            self.present_weapon.draw(screen)

        if self.bullets :
            for bullet in self.bullets :
                bullet.draw(screen)
                

    def moveHandle(self, allWeapons, other):
        keys = self.keys
        if keys[pygame.K_a]:
            self.moveLeft()
        if keys[pygame.K_d]:
            self.moveRight()
        if keys[pygame.K_w]:
            self.moveUp()
        if keys[pygame.K_s]:
            self.moveDown()
        if keys[pygame.K_SPACE] and self.can_pick == True:
            print("SPACE PRESSED")
            self.pickUpWeapon(allWeapons)
            # self.pickUpClips(clips)
        if keys[pygame.K_r]:
            print("r pressed")

            self.changeWeapon()
        if self.mouse_get_pressed[0] : 
            if self.present_weapon :
                self.present_weapon.attack()
        for bullet in self.bullets:
            bullet.hit(other)
            
    def calFacing(self):  # 算人物面向的角度
        theta = 0
        pos = self.mouse_get_pos
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

    def update(self):
        if self.mouse_get_pos :
            self.facing = self.calFacing()
        
