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


def bulletsHandle(bullets, player):
    for bullet in bullets:
        bullet.x += bullet.vel[0]
        bullet.y += bullet.vel[1]
        bullet.hit(player)


def drawScreen(screen, player1, player2, background, bullets1, bullets2, all_weapons, clips,grasses,hides):
    pygame.display.flip()
    screen.blit(background, (0, 0))

    player1.draw(screen)
    for weapon in all_weapons:
        weapon.draw(screen)
    player2.draw(screen)

    for bullet in bullets1:
        bullet.draw(screen)
    for clip in clips:
        clip.draw(screen)
    for grass in grasses:
        grass.draw(screen)
    for hide in hides:
        hide.draw(screen)


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
        image = pygame.transform.scale(image, (int(w), int(h)))
        self.imgString = pygame.image.tostring(image, "RGB")
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.speed = speed
        self.life = 70
        self.facing = 0
        self.middleX = self.x+self.w//2
        self.middleY = self.y+self.h//2
        self.weapons = []
        self.can_pick=True
        self.present_weapon = None

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
        pick_count=0
        for weapon in weapons:
            if not weapon.isTaken and pygame.sprite.collide_rect(weapon, self) and pick_count==0:
                weapon.isTaken = True
                # 如果玩家武器數小於2 直接append到self
                if len(self.weapons) < 2:
                    self.weapons.append(weapon)

                    self.present_weapon = weapon
                    pick_count=1
                #如果玩家武器數等於2 退掉第一個 再加新的一個
                elif len(self.weapons)==2 :
                    self.present_weapon.isTaken = False
                    self.weapons.remove(self.present_weapon)
                    self.weapons.append(weapon)
                    self.present_weapon = weapon
                    pick_count=1
            
        

    def pickUpClips(self, clips):
        for clip in clips:
            if not clip.isTaken and pygame.sprite.collide_rect(clip, self):
                clip.isTaken = True
                self.weapons[0].ammunition+=10
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
        self.facing = self.calFacing()
        image = pygame.image.fromstring(
            self.imgString, (self.w, self.h), "RGB")
        rotate_image = pygame.transform.rotate(
            image, -self.facing*180/math.pi)
        self.rect = rotate_image.get_rect(
            center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotate_image, (self.rect.x, self.rect.y))

    """
     def moveHandleP1(self, keys, bullets):
         if keys[pygame.K_LEFT]:
             self.moveLeft()
         if keys[pygame.K_RIGHT]:
             self.moveRight()
         if keys[pygame.K_UP]:
             self.moveUp()
         if keys[pygame.K_DOWN]:
             self.moveDown()
         if keys[pygame.K_SPACE]:
             bullets.append(Bullet(round(self.rect.x+self.w//2),
                                   round(self.rect.y+self.h//2),
                                   self.facing))
    """

    def moveHandleP2(self, keys, allWeapons, clips):
        if keys[pygame.K_a]:
            self.moveLeft()
        if keys[pygame.K_d]:
            self.moveRight()
        if keys[pygame.K_w]:
            self.moveUp()
        if keys[pygame.K_s]:
            self.moveDown()
        if keys[pygame.K_SPACE] and self.can_pick==True:
            self.pickUpWeapon(allWeapons)
# <<<<<<< HEAD
            self.pickUpClips(clips)
        if keys[pygame.K_r]:
# =======
#             self.can_pick=False
#         if not keys[pygame.K_SPACE] and self.can_pick==False:
#             self.can_pick=True
#         if keys[pygame.K_s]:
# >>>>>>> e82948477d5767465d71406e7d10755f26c7f7f7
            self.changeWeapon()
        if pygame.mouse.get_pressed()[0]:
            for weapon in self.weapons:
                weapon.attack()

    def calFacing(self):  # 算人物面向的角度
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


class Gun(pygame.sprite.Sprite):
    def __init__(self, name, x, y, w, h, gun_image, max_ammunition, atkPoint, player, shoot_delay, isTaken):
        super().__init__()
        self.name = name
        self.image = pygame.transform.scale(gun_image, (int(2*w), int(2*h)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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
        if (pygame.time.get_ticks() - self.last_shoot_time > self.shoot_delay) and self.ammunition:
            self.last_shoot_time = pygame.time.get_ticks()
            self.ammunition -= 1
            self.player.bullets.append(Bullet(round(self.player.middleX),
                                              round(self.player.middleY),
                                              self.player.facing, self.atkPoint))
            return

    def draw(self, screen):
        self.update()
        if not self.isTaken:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            return
        facing = self.player.calFacing()
        rotate_image = pygame.transform.rotate(
            self.image, -facing*180/math.pi)
        self.rect = rotate_image.get_rect(
            center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotate_image, (self.rect.x, self.rect.y))


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


class Knife(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()


class Clip(pygame.sprite.Sprite):

    def __init__(self, image, position):
        super().__init__()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.isTaken = False
 

    def draw(self, screen):
        if not self.isTaken:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            return


class Grass(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = pygame.transform.scale(image, (300, 150))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return


class Hide(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = pygame.transform.scale(image, (300, 150))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.isTaken = False
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

