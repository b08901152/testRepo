#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#fuck

import pygame
import random
import math
from pygame.math import Vector2 
from math import cos,sin,pi,atan2
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (0, 126, 0)





def game():
    class Player(pygame.sprite.Sprite):
        def __init__(self,name,image,up,down,left,right,attack,change,pick,x,y,w,h,speed=(0,0)):
            super().__init__()
            self.name=name
            self.speed=speed
            self.rect=pygame.rect.Rect(x,y,w,h)
            #player的生命值
            self.life = 70 

            #index從0到6分別代表上下左右 攻擊 換武器 撿武器
            #要輸入的up,down,left,right是按鍵的名子
            self.control_list=[up,down,left,right,attack,change,pick]

            image=pygame.transform.scale(image,(int(w),int(h)))
            self.image=image
            self.angle=0#用來處理player轉方向的時候，圖也要跟著轉
            self.weapon=[]
            self.present_weapon=None
            

            #screen.blit(self.failImage, self.bounds)
        def update(self, *args):
            pass
        def move_up(self):
            if self.rect.top<=0:
                pass
            else: 
                self.rect.y -= self.speed[1] 
        def move_down(self):
            if self.rect.bottom>=screen.get_height():
                pass
            else: 
                self.rect.y += self.speed[1]
        def move_left(self):
            if self.rect.left<0:
                pass
            else: 
                self.rect.x -= self.speed[0] 
        def move_right(self):
            if self.rect.right>screen.get_width():
                pass
            else: 
                self.rect.x += self.speed[0] 
        def strike(self, bullet_sprites):
            collide_bullet = pygame.sprite.spritecollide(self,bullet_sprites, True)
            if len(collide_bullet) > 0:
                self.life -= 10
                
            
        def is_survive(self):
            return self.life > 0
        def draw(self,screen):
            pygame.draw.rect(screen,(255,0,0),(self.rect.x,self.rect.y-10,70,10))
            pygame.draw.rect(screen,(0,127,0),(self.rect.x,self.rect.y-10,self.life,10))



        


    class Bullet(pygame.sprite.Sprite):
        shoot_delay = 500 #兩發子彈的間隔時間
        last_shoot_time = 0

        def __init__(self,position): 
            #position是用來設定子彈的位置
            super().__init__()
            image=pygame.image.load('image/bullet.png').convert()
            self.image = pygame.transform.scale(image,(20,5))
            self.rect = self.image.get_rect() 
            self.speed = (10,0) 
            self.rect.x = position[0] 
            self.rect.y = position[1]

        def update(self):
            self.rect.x += self.speed[0]
            self.rect.y -= self.speed[1]


    class Gun(pygame.sprite.Sprite):
        def __init__(self,name,x,y,w,h,gun_image,hit):
            super().__init__()
            self.name=name
            image=pygame.transform.scale(gun_image,(int(2*w),int(2*h)))
            self.image=image
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
            self.max_ammunition=10 #彈藥限制
            self.ammunition=10     #現在的彈藥
            self.shoot_delay = 500 #兩發子彈的間隔時間
            self.last_shoot_time = 0
            self.bullet_speed=40
            self.gun_origin_image=pygame.Surface.copy(self.image)
            self.gun_turn_image=pygame.Surface.copy(self.image)
            self.hit=hit
        def update(self):
            if self in player1.weapon :
                #player1拿槍之後槍的位置
                self.rect.centerx=player1.rect.centerx
                self.rect.centery=player1.rect.centery
            if self in player2.weapon :
                #player2拿槍之後槍的位置
                self.rect.centerx=player2.rect.centerx
                self.rect.centery=player2.rect.centery
        def new_bullet(self, position): 
            if pygame.time.get_ticks() - self.last_shoot_time > self.shoot_delay: 
                self.last_shoot_time = pygame.time.get_ticks() 
                return Bullet(position)

    class Knife(pygame.sprite.Sprite):
        cut_delay = 250
        
        def __init__(self,x,y,w,h,speed=(0,0)):
            super().__init__()
            image=pygame.image.load('image/knife.png').convert_alpha() 
            image=pygame.transform.scale(image,(int(w),int(h)))
            self.image=image
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
            self.last_cut_time = 0
        def update(self):
            pass
            
        def new_cut(self): 
            if pygame.time.get_ticks() - self.last_cut_time > Knife.cut_delay: 
                self.last_cut_time = pygame.time.get_ticks() 
                return True

    #彈夾
    class Clip(pygame.sprite.Sprite):
        delay = 5000 #彈夾消失之後下次出現的時間
        def __init__(self,position): 
            #position是用來設定彈夾的位置
            super().__init__()
            image=pygame.image.load('image/clip.png').convert_alpha()
            self.image = pygame.transform.scale(image,(30,50))
            self.rect = self.image.get_rect() 
            self.rect.x = position[0] 
            self.rect.y = position[1]
            self.last_time = 0#上次消失的時間
            self.exist=True #用來表示彈夾現在存不存在
        def update(self):
            pass
        def new_clip(self): 
            if pygame.time.get_ticks() - self.last_time > Clip.delay: 
                self.exist=True
                return True 

    # 障礙物
    class Box(pygame.sprite.Sprite):
        def __init__(self,x,y,w,h,speed=(0,0)):
            super().__init__()
            image=pygame.image.load('image/box.png').convert_alpha()
            image=pygame.transform.scale(image,(int(w),int(h)))
            self.image=image
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
        def update(self):
            pass
    #草叢
    class Grass(pygame.sprite.Sprite):
        def __init__(self,x,y,w,h,speed=(0,0)):
            super().__init__()
            image=pygame.image.load('image/grass.png').convert_alpha()
            image=pygame.transform.scale(image,(int(4*w),int(4*h)))
            self.image=image
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
        def update(self):
            pass

    # 躲避處
    class Hide(pygame.sprite.Sprite):
        def __init__(self,x,y,w,h,speed=(0,0)):
            super().__init__()
            image=pygame.image.load('image/hide.png').convert_alpha()
            image=pygame.transform.scale(image,(int(w),int(h)))
            self.image=image
            self.rect = self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
        def update(self):
            pass

        

    def show_text(word, color, position, font_size):
        sys_font = pygame.font.SysFont('Comic Sans MS', font_size)
        score_surface = sys_font.render(word, False, color)
        screen.blit(score_surface, position)

    def collision(source,target):
        if not source.colliderect(target):#return bool if collide
            return
        overlap=source.clip(target)

        if overlap.width>overlap.height:#vert collision
            if source.y<target.y:#top
                source.bottom=target.top
            else:
                source.top=target.bottom
        else:#horizontal collision
            if source.x<target.x:#left
                source.right=target.left
            else:
                source.left=target.right
    """
    def game_over_text():
        over_text = pygame.font('GAME OVER', (30, 20), (255, 255, 255))
        screen.blit(over_text, (500, 300))"""




    BLUE = (0 ,0, 255)

    pygame.init()
    pygame.mixer.init() ## For sound
    screen = pygame.display.set_mode((1400, 800))
    #background
    background = pygame.image.load("image/map.png")
    background = pygame.transform.scale(background,(int(1400),int(800)))

    pygame.display.set_caption("final_project")
    clock = pygame.time.Clock()


    #music
    pygame.mixer.music.load('music/backg.mp3')
    pygame.mixer.music.play(loops=-1)

    #player1
    failImage = pygame.image.load('image/player1.png').convert_alpha()#player1要用的圖
    player1=Player('123',failImage,pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,K_SPACE,K_TAB,K_q,
        50,400,100,100,(15,15))
    player1_origin_image=pygame.Surface.copy(player1.image)

    #player2
    failImage = pygame.image.load('image/player2.png').convert_alpha()#player2要用的圖
    player2=Player('123',failImage,pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,
        1150,400,100,100,(15,15))
    player2_origin_image=pygame.Surface.copy(player2.image)


    normal_gun_image=pygame.image.load('image/gun.png').convert_alpha()
    #小槍
    gun=Gun('normal',660,50,30,30,normal_gun_image,10)
    gun2=Gun('normal',660,750,30,30,normal_gun_image,10)

    machine_gun_image=pygame.image.load('image/machine_gun.png').convert_alpha()
    #機關槍
    machine_gun= Gun('machine_gun',660,400,30,30,machine_gun_image,1)
    machine_gun.bullet_speed=30
    machine_gun.shoot_delay =250
    machine_gun.max_ammunition= 30
    machine_gun.ammunition= 30

    # gun_origin_image=pygame.Surface.copy(gun.image)
    # gun_turn_image=pygame.Surface.copy(gun.image)
    gun_sprites = pygame.sprite.Group()
    gun_sprites.add(gun)
    gun_sprites.add(gun2)
    gun_sprites.add(machine_gun)

    #彈夾
    clip_sprites = pygame.sprite.Group()
    pos=(20,20)#彈夾的位置
    pos1=(1360,20)
    clip=Clip(pos)
    clip1=Clip(pos1)
    clip_sprites.add(clip)
    clip_sprites.add(clip1)

    #player1的刀
    player1_knife=Knife(player1.rect.centerx,player1.rect.centery,100,100)
    player1_knife_origin_image=pygame.Surface.copy(player1_knife.image)
    player1_knife_turn_image=pygame.Surface.copy(player1_knife.image)
    player1_knife_central=Vector2(player1_knife.rect.w/2+player1.rect.w/2-30,player1.rect.h/2-player1_knife.rect.h/2-10)
    new_player1_knife_central=Vector2(player1_knife.rect.w/2+player1.rect.w/2-30,player1.rect.h/2-player1_knife.rect.h/2-10)
    player1_knife_central_to_handle=Vector2(-player1_knife.rect.w/2,player1_knife.rect.h/2)
    new_player1_knife_central_to_handle=Vector2(-player1_knife.rect.w/2,player1_knife.rect.h/2)

    player1_count=0 #這是用來處理揮刀的時候，揮出去到最大角度的過程中player1_count=0，從最大角度回來的時候player1_count=1

    player1.weapon.append(player1_knife)
    player1.present_weapon=player1_knife#一開始player1就拿了一把刀
    cut_player1_count=0#揮刀過程中的角度
    player1_cut=False#用來代表player1有沒有在揮刀
    player1_knife_kill=0#揮一次刀只能扣player2一次血


    #player2的刀
    player2_knife=Knife(player2.rect.centerx,player2.rect.centery,100,100)
    player2_knife_origin_image=pygame.Surface.copy(player2_knife.image)
    player2_knife_turn_image=pygame.Surface.copy(player2_knife.image)
    player2_knife_central=Vector2(player2_knife.rect.w/2+player2.rect.w/2-30,player2.rect.h/2-player2_knife.rect.h/2-10)
    new_player2_knife_central=Vector2(player2_knife.rect.w/2+player2.rect.w/2-30,player2.rect.h/2-player2_knife.rect.h/2-10)
    player2_knife_central_to_handle=Vector2(-player2_knife.rect.w/2,player2_knife.rect.h/2)
    new_player2_knife_central_to_handle=Vector2(-player2_knife.rect.w/2,player2_knife.rect.h/2)

    player2_count=0 #這是用來處理揮刀的時候，揮出去到最大角度的過程中player2_count=0，從最大角度回來的時候player2_count=1

    player2.weapon.append(player2_knife)
    player2.present_weapon=player2_knife#一開始player2就拿了一把刀
    cut_player2_count=0#揮刀過程中的角度
    player2_cut=False#用來代表player2有沒有在揮刀
    player2_knife_kill=0#揮一次刀只能扣player1一次血

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(gun)
    all_sprites.add(gun2)
    all_sprites.add(machine_gun)
    all_sprites.add(clip)
    all_sprites.add(clip1)
    weapon_sprites = pygame.sprite.Group()
    weapon_sprites.add(gun)
    weapon_sprites.add(gun2)
    weapon_sprites.add(machine_gun)
    weapon_sprites.add(player1_knife)
    weapon_sprites.add(player2_knife)

    # 生成一堆障礙物
    box_list = []
    box_x = []
    box_y = []
    for i in range(5):
        box_x.append(random.randint(100,610))
        box_y.append(random.randint(100,700))
    for i in range(5):
        box_x.append(random.randint(710,1300))
        box_y.append(random.randint(100,700))

    for i in range(10):
        box_list.append(Box(box_x[i],box_y[i],100,100))

    box_sprites= pygame.sprite.Group()
    for box in box_list:
        box_sprites.add(box)
        all_sprites.add(box)


    # 生成一堆草叢
    grass_list = []
    grass_x = []
    grass_y = []

    while True:
        grass_location = True
        x, y = random.randint(100,1100), random.randint(100,700)
        # 讓草叢和障礙物不會重疊
        for i in range(10):
            d = ((x-box_x[i])**2 + (y-box_y[i])**2)**(1/2)
            if d <= 142: 
                grass_location = False
            d = ((x-660)**2 + (y-400)**2)**(1/2)
            if d <= 100: 
                grass_location = False
        if grass_location:
            grass_x.append(x)
            grass_y.append(y)
        if len(grass_x) == 10:
            break

    for i in range(10):
        grass_list.append(Grass(grass_x[i],grass_y[i],100,100))

    grass_sprites= pygame.sprite.Group()
    for grass in grass_list:
        grass_sprites.add(grass)
        all_sprites.add(grass)


    # 生成一堆躲避區
    hide_list = []
    hide_x = []
    hide_y = []

    while True:
        hide_location = True
        x, y = random.randint(100,1100), random.randint(100,700)
        # 讓躲避區與草叢和障礙物不會重疊
        for i in range(10):
            d = ((x-box_x[i])**2 + (y-box_y[i])**2)**(1/2)
            if d <= 142: 
                hide_location = False
            d = ((x-grass_x[i])**2 + (y-grass_y[i])**2)**(1/2)
            if d <= 142: 
                hide_location = False
            d = ((x-660)**2 + (y-400)**2)**(1/2)
            if d <= 100: 
                hide_location = False
        if hide_location:
            hide_x.append(x)
            hide_y.append(y)
        if len(hide_x) == 10:
            break

    for i in range(10):
        hide_list.append(Hide(hide_x[i],hide_y[i],100,100))

    hide_sprites= pygame.sprite.Group()
    for hide in hide_list:
        hide_sprites.add(hide)
        all_sprites.add(hide)



    player1_bullet_sprites = pygame.sprite.Group() 
    player2_bullet_sprites = pygame.sprite.Group() 


    pygame.font.init()


    running = True
    while running:
        clock.tick(60)
        player1.draw(screen)
        player2.draw(screen)

        pygame.display.update()


        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

            if event.type == pygame.KEYDOWN:
                #player1
                if event.key == player1.control_list[0]:
                    #往上的時候逆時針轉90度
                    
                    player1.image=pygame.transform.rotate(player1_origin_image, 90)
                    player1.angle=90
                    player1.rect=player1.image.get_rect(center=(player1.rect.centerx,player1.rect.centery))

                    if player1_knife in player1.weapon :
                        player1_knife.image=pygame.transform.rotate(player1_knife_origin_image, 90)
                        player1_knife_turn_image=pygame.transform.rotate(player1_knife_origin_image, 90)
                        player1_knife.rect=player1_knife.image.get_rect()

                        new_player1_knife_central=player1_knife_central.rotate(-player1.angle)
                        new_player1_knife_central_to_handle=player1_knife_central_to_handle.rotate(-player1.angle)
                        
                    if gun in player1.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 90)
                        gun.rect=gun.image.get_rect()



                if event.key == player1.control_list[1]:
                    #往下的時候順時針轉90度
                    player1.image=pygame.transform.rotate(player1_origin_image, -90)
                    player1.angle=-90
                    player1.rect=player1.image.get_rect(center=(player1.rect.centerx,player1.rect.centery))

                    if player1_knife in player1.weapon :
                        player1_knife.image=pygame.transform.rotate(player1_knife_origin_image, -90)
                        player1_knife_turn_image=pygame.transform.rotate(player1_knife_origin_image, -90)
                        player1_knife.rect=player1_knife.image.get_rect()
                    
                        new_player1_knife_central=player1_knife_central.rotate(-player1.angle)
                        new_player1_knife_central_to_handle=player1_knife_central_to_handle.rotate(-player1.angle)

                    if gun in player1.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, -90)
                        gun.rect=gun.image.get_rect()


                    
                if event.key == player1.control_list[2]:
                    #往左的時候逆時針轉180度
                    player1.image=pygame.transform.rotate(player1_origin_image, 180)
                    player1.angle=180
                    player1.rect=player1.image.get_rect(center=(player1.rect.centerx,player1.rect.centery))

                    if player1_knife in player1.weapon :
                        player1_knife.image=pygame.transform.rotate(player1_knife_origin_image, 180)
                        player1_knife_turn_image=pygame.transform.rotate(player1_knife_origin_image, 180)
                        player1_knife.rect=player1_knife.image.get_rect()
                    
                        new_player1_knife_central=player1_knife_central.rotate(-player1.angle)
                        new_player1_knife_central_to_handle=player1_knife_central_to_handle.rotate(-player1.angle)

                    if gun in player1.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 180)
                        gun.rect=gun.image.get_rect()
                    
                    
                     
                if event.key == player1.control_list[3]:
                    #往右的時候就是原本的圖
                    player1.image=pygame.transform.rotate(player1_origin_image, 0)
                    player1.angle=0
                    player1.rect=player1.image.get_rect(center=(player1.rect.centerx,player1.rect.centery))

                    if player1_knife in player1.weapon :
                        player1_knife.image=pygame.transform.rotate(player1_knife_origin_image, 0)
                        player1_knife_turn_image=pygame.transform.rotate(player1_knife_origin_image, 0)
                        player1_knife.rect=player1_knife.image.get_rect()
                    
                        new_player1_knife_central=player1_knife_central.rotate(-player1.angle)
                        new_player1_knife_central_to_handle=player1_knife_central_to_handle.rotate(-player1.angle)

                    if gun in player1.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 0)
                        gun.rect=gun.image.get_rect()
                    
                if event.key == player1.control_list[4] and player1_knife == player1.present_weapon and player1_knife.new_cut(): 
                    player1_cut=True
                reload_sound=pygame.mixer.Sound("music/reload.wav")
                if event.key == player1.control_list[5] and len(player1.weapon)==2:
                    #player1換武器
                    weapon_player1_count=0 #讓player1按一次鍵只能換一次武器
                    for weapon in player1.weapon:
                        if weapon !=player1.present_weapon and weapon_player1_count==0:
                            reload_sound.play()
                            player1.present_weapon=weapon
                            weapon_player1_count=1

                player1_pick_count=0
                for weapon in weapon_sprites:
                    if event.key == player1.control_list[6] and pygame.sprite.collide_rect(player1,weapon) and (weapon not in player1.weapon) and (weapon not in player2.weapon):
                        #player1撿武器，最多兩個武器，武器滿的時候會把手上到武器丟掉，拿新的武器
                        if len(player1.weapon)==2 and player1_pick_count==0:
                            player1.weapon.remove(player1.present_weapon)
                            player1.weapon.append(weapon)
                            player1.present_weapon=weapon
                            player1_pick_count=1
                            
                        elif len(player1.weapon)==1 and player1_pick_count==0:
                            player1.weapon.append(weapon)
                            player1.present_weapon=weapon
                '''_________________________________________________________________________________________'''
                #player2
                if event.key == player2.control_list[0]:
                    #往上的時候逆時針轉90度
                    
                    player2.image=pygame.transform.rotate(player2_origin_image, 90)
                    player2.angle=90
                    player2.rect=player2.image.get_rect(center=(player2.rect.centerx,player2.rect.centery))

                    if player2_knife in player2.weapon :
                        player2_knife.image=pygame.transform.rotate(player2_knife_origin_image, 90)
                        player2_knife_turn_image=pygame.transform.rotate(player2_knife_origin_image, 90)
                        player2_knife.rect=player2_knife.image.get_rect()

                        new_player2_knife_central=player2_knife_central.rotate(-player2.angle)
                        new_player2_knife_central_to_handle=player2_knife_central_to_handle.rotate(-player2.angle)

                    if gun in player2.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 90)
                        gun.rect=gun.image.get_rect()



                if event.key == player2.control_list[1]:
                    #往下的時候順時針轉90度
                    player2.image=pygame.transform.rotate(player2_origin_image, -90)
                    player2.angle=-90
                    player2.rect=player2.image.get_rect(center=(player2.rect.centerx,player2.rect.centery))

                    if player2_knife in player2.weapon :
                        player2_knife.image=pygame.transform.rotate(player2_knife_origin_image, -90)
                        player2_knife_turn_image=pygame.transform.rotate(player2_knife_origin_image, -90)
                        player2_knife.rect=player2_knife.image.get_rect()
                    
                        new_player2_knife_central=player2_knife_central.rotate(-player2.angle)
                        new_player2_knife_central_to_handle=player2_knife_central_to_handle.rotate(-player2.angle)

                    if gun in player2.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, -90)
                        gun.rect=gun.image.get_rect()


                    
                if event.key == player2.control_list[2]:
                    #往左的時候逆時針轉180度
                    player2.image=pygame.transform.rotate(player2_origin_image, 180)
                    player2.angle=180
                    player2.rect=player2.image.get_rect(center=(player2.rect.centerx,player2.rect.centery))

                    if player2_knife in player2.weapon :
                        player2_knife.image=pygame.transform.rotate(player2_knife_origin_image, 180)
                        player2_knife_turn_image=pygame.transform.rotate(player2_knife_origin_image, 180)
                        player2_knife.rect=player2_knife.image.get_rect()
                    
                        new_player2_knife_central=player2_knife_central.rotate(-player2.angle)
                        new_player2_knife_central_to_handle=player2_knife_central_to_handle.rotate(-player2.angle)

                    if gun in player2.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 180)
                        gun.rect=gun.image.get_rect()
                    
                    
                     
                if event.key == player2.control_list[3]:
                    #往右的時候就是原本的圖
                    player2.image=pygame.transform.rotate(player2_origin_image, 0)
                    player2.angle=0
                    player2.rect=player2.image.get_rect(center=(player2.rect.centerx,player2.rect.centery))

                    if player2_knife in player2.weapon :
                        player2_knife.image=pygame.transform.rotate(player2_knife_origin_image, 0)
                        player2_knife_turn_image=pygame.transform.rotate(player2_knife_origin_image, 0)
                        player2_knife.rect=player2_knife.image.get_rect()
                    
                        new_player2_knife_central=player2_knife_central.rotate(-player2.angle)
                        new_player2_knife_central_to_handle=player2_knife_central_to_handle.rotate(-player2.angle)

                    if gun in player2.weapon :
                        gun.image=pygame.transform.rotate(gun.gun_origin_image, 0)
                        gun.rect=gun.image.get_rect()
                    
                if event.key == player2.control_list[4] and player2_knife == player2.present_weapon and player2_knife.new_cut(): 
                    player2_cut=True
                reload_sound=pygame.mixer.Sound("music/reload.wav")
                if event.key == player2.control_list[5] and len(player2.weapon)==2:
                    #player2換武器
                    weapon_player2_count=0 #讓player2按一次鍵只能換一次武器
                    for weapon in player2.weapon:
                        if weapon !=player2.present_weapon and weapon_player2_count==0:
                            reload_sound.play()
                            player2.present_weapon=weapon
                            weapon_player2_count=1

                player2_pick_count=0
                for weapon in weapon_sprites:
                    if event.key == player2.control_list[6] and pygame.sprite.collide_rect(player2,weapon) and (weapon not in player1.weapon) and (weapon not in player2.weapon):
                        #player2撿武器，最多兩個武器，武器滿的時候會把手上到武器丟掉，拿新的武器
                        if len(player2.weapon)==2 and player2_pick_count==0:
                            player2.weapon.remove(player2.present_weapon)
                            player2.weapon.append(weapon)
                            player2.present_weapon=weapon
                            player2_pick_count=1
                            
                        elif len(player2.weapon)==1 and player2_pick_count==0:
                            player2.weapon.append(weapon)
                            player2.present_weapon=weapon
        '''_________________________________________________________________________________________'''

        
        

                
                            

        
                    
        #player1上下左右動
        walk_sound=pygame.mixer.Sound('music/walk.wav')
        key_pressed = pygame.key.get_pressed()
        if key_pressed[player1.control_list[0]] : 
            player1.move_up()
            walk_sound.play() 
        if key_pressed[player1.control_list[1]] : 
            player1.move_down()
            walk_sound.play() 
        if key_pressed[player1.control_list[2]] :
            player1.move_left()
            walk_sound.play() 
        if key_pressed[player1.control_list[3]] :
            player1.move_right()
            walk_sound.play()
        '''_________________________________________________________________________________________'''

        #player2上下左右動
        walk_sound=pygame.mixer.Sound('music/walk.wav')
        key_pressed = pygame.key.get_pressed()
        if key_pressed[player2.control_list[0]] : 
            player2.move_up()
            walk_sound.play() 
        if key_pressed[player2.control_list[1]] : 
            player2.move_down()
            walk_sound.play() 
        if key_pressed[player2.control_list[2]] :
            player2.move_left()
            walk_sound.play() 
        if key_pressed[player2.control_list[3]] :
            player2.move_right()
            walk_sound.play()
        '''_________________________________________________________________________________________'''

        shoot_sound=pygame.mixer.Sound('music/gunshoot.wav')
        #player1拿槍的時候射子彈
        if key_pressed[player1.control_list[4]]:
            
            if  isinstance(player1.present_weapon,Gun) : 
                bullet = player1.present_weapon.new_bullet((player1.rect.centerx, player1.rect.centery))
                
                if bullet and player1.present_weapon.ammunition>0:
                    shoot_sound.play()
                    bullet.image=pygame.transform.rotate(bullet.image, player1.angle)
                    bullet.rect=bullet.image.get_rect(center=(bullet.rect.centerx,bullet.rect.centery))
                    if player1.present_weapon.name=='machine_gun':
                        angle=player1.angle+random.randint(-10,10)
                    else:
                        angle=player1.angle
                    speed=player1.present_weapon.bullet_speed
                    bullet.speed=(speed*cos(angle*pi/180),speed*sin(angle*pi/180))
                    bullet.hit=player1.present_weapon.hit
                    player1.present_weapon.ammunition-=1
                    player1_bullet_sprites.add(bullet) 
                    all_sprites.add(bullet)
                """
                #這幾行是讓子彈撞到箱子的時候消失
                if len(pygame.sprite.spritecollide(bullet,box_sprites,False))!=0:
                    for box in pygame.sprite.spritecollide(bullet,box_sprites,False):
                        bullet.rect.x = 2000"""
        '''_________________________________________________________________________________________'''

        #player2拿槍的時候射子彈
        if key_pressed[player2.control_list[4]]:
            
            if  isinstance(player2.present_weapon,Gun) : 
                bullet = player2.present_weapon.new_bullet((player2.rect.centerx, player2.rect.centery))
                if bullet and player2.present_weapon.ammunition>0:
                    shoot_sound.play()
                    bullet.image=pygame.transform.rotate(bullet.image, player2.angle)
                    bullet.rect=bullet.image.get_rect(center=(bullet.rect.centerx,bullet.rect.centery))
                    if player2.present_weapon.name=='machine_gun':
                        angle=player2.angle+random.randint(-10,10)
                    else:
                        angle=player2.angle
                    speed=player2.present_weapon.bullet_speed
                    bullet.speed=(speed*cos(angle*pi/180),speed*sin(angle*pi/180))
                    bullet.hit=player2.present_weapon.hit
                    player2.present_weapon.ammunition-=1
                    player2_bullet_sprites.add(bullet) 
                    all_sprites.add(bullet)
                    """
                    #這幾行是讓子彈撞到箱子的時候消失
                    if len(pygame.sprite.spritecollide(bullet,box_sprites,False))!=0:
                        for box in pygame.sprite.spritecollide(bullet,box_sprites,False):
                            bullet.rect.x = 2000"""
        '''_________________________________________________________________________________________'''



        #player1揮刀
        knife_sound=pygame.mixer.Sound("music/knife.wav")
        if player1_cut:
            knife_sound.play()
            if 0<=cut_player1_count<60 and player1_count==0:
                angle=cut_player1_count
                player1_knife.image=pygame.transform.rotate(player1_knife_turn_image, angle)
                player1_knife.rect=player1_knife.image.get_rect()
                cut_player1_count+=12
                try:
                    new_player1_knife_central.x-=diff.x
                    new_player1_knife_central.y-=diff.y
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y
                except:
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y

            elif cut_player1_count==60 and player1_count==0:
                angle=cut_player1_count
                player1_knife.image=pygame.transform.rotate(player1_knife_turn_image, angle)
                player1_knife.rect=player1_knife.image.get_rect()
                cut_player1_count-=12

                try:
                    new_player1_knife_central.x-=diff.x
                    new_player1_knife_central.y-=diff.y
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y
                except:
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y

                player1_count=1
            elif 0<cut_player1_count<60 and player1_count==1:
                angle=cut_player1_count
                player1_knife.image=pygame.transform.rotate(player1_knife_turn_image, angle)
                player1_knife.rect=player1_knife.image.get_rect()
                cut_player1_count-=12

                try:
                    new_player1_knife_central.x-=diff.x
                    new_player1_knife_central.y-=diff.y
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y
                except:
                    diff=new_player1_knife_central_to_handle-new_player1_knife_central_to_handle.rotate(-cut_player1_count)
                    new_player1_knife_central.x+=diff.x
                    new_player1_knife_central.y+=diff.y

                player1_count=1
            elif cut_player1_count==0 and player1_count==1:
                player1_count=0
                player1_knife_kill=0
                player1_cut=False

            
        '''_________________________________________________________________________________________'''

        #player2揮刀
        knife_sound=pygame.mixer.Sound("music/knife.wav")
        if player2_cut:
            knife_sound.play()
            if 0<=cut_player2_count<60 and player2_count==0:
                angle=cut_player2_count
                player2_knife.image=pygame.transform.rotate(player2_knife_turn_image, angle)
                player2_knife.rect=player2_knife.image.get_rect()
                cut_player2_count+=12

                try:
                    new_player2_knife_central.x-=diff.x
                    new_player2_knife_central.y-=diff.y
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y
                except:
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y

            elif cut_player2_count==60 and player2_count==0:
                angle=cut_player2_count
                player2_knife.image=pygame.transform.rotate(player2_knife_turn_image, angle)
                player2_knife.rect=player2_knife.image.get_rect()
                cut_player2_count-=12

                try:
                    new_player2_knife_central.x-=diff.x
                    new_player2_knife_central.y-=diff.y
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y
                except:
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y

                player2_count=1

            elif 0<cut_player2_count<60 and player2_count==1:
                angle=cut_player2_count
                player2_knife.image=pygame.transform.rotate(player2_knife_turn_image, angle)
                player2_knife.rect=player2_knife.image.get_rect()
                cut_player2_count-=12

                try:
                    new_player2_knife_central.x-=diff.x
                    new_player2_knife_central.y-=diff.y
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y
                except:
                    diff=new_player2_knife_central_to_handle-new_player2_knife_central_to_handle.rotate(-cut_player2_count)
                    new_player2_knife_central.x+=diff.x
                    new_player2_knife_central.y+=diff.y

                player2_count=1

            elif cut_player2_count==0 and player2_count==1:
                player2_count=0
                player2_knife_kill=0
                player2_cut=False

            
        '''_________________________________________________________________________________________'''



        #這下面四個是防止player1破圖
        if player1.rect.top<0:
            player1.rect.move_ip(0,-player1.rect.top)
        if player1.rect.bottom>=screen.get_height():
            player1.rect.move_ip(0,screen.get_height()-player1.rect.bottom)
        if player1.rect.left<0:
            player1.rect.move_ip(-player1.rect.left,0)
        if player1.rect.right>screen.get_width():
            player1.rect.move_ip(screen.get_width()-player1.rect.right,0)
        '''_________________________________________________________________________________________'''

        #這下面四個是防止player2破圖
        if player2.rect.top<0:
            player2.rect.move_ip(0,-player2.rect.top)
        if player2.rect.bottom>=screen.get_height():
            player2.rect.move_ip(0,screen.get_height()-player2.rect.bottom)
        if player2.rect.left<0:
            player2.rect.move_ip(-player2.rect.left,0)
        if player2.rect.right>screen.get_width():
            player2.rect.move_ip(screen.get_width()-player2.rect.right,0)
        '''_________________________________________________________________________________________'''


        #這幾行是讓player1撞到箱子的時候停住
        if len(pygame.sprite.spritecollide(player1,box_sprites,False))!=0:
            for box in pygame.sprite.spritecollide(player1,box_sprites,False):
                collision(player1.rect,box.rect)
        '''_________________________________________________________________________________________'''

        #這幾行是讓player2撞到箱子的時候停住
        if len(pygame.sprite.spritecollide(player2,box_sprites,False))!=0:
            for box in pygame.sprite.spritecollide(player2,box_sprites,False):
                collision(player2.rect,box.rect)
        '''_________________________________________________________________________________________'''


        #這幾行是讓player1拿刀的時候刀的位置相對於人是固定的
        if player1_knife in player1.weapon :
            player1_knife.rect.centerx= new_player1_knife_central.x+player1.rect.centerx
            player1_knife.rect.centery= new_player1_knife_central.y+player1.rect.centery
        '''_________________________________________________________________________________________'''

        #這幾行是讓player2拿刀的時候刀的位置相對於人是固定的
        if player2_knife in player2.weapon :
            player2_knife.rect.centerx= new_player2_knife_central.x+player2.rect.centerx
            player2_knife.rect.centery= new_player2_knife_central.y+player2.rect.centery
        '''_________________________________________________________________________________________'''


        #讓player1換武器的時候，其他手上的武器不要出現
        for weapon in player1.weapon:
            if player1.present_weapon == weapon :
                if not all_sprites.has(weapon):
                    all_sprites.add(weapon)
            else:
                all_sprites.remove(weapon)

        '''_________________________________________________________________________________________'''

        #讓player2換武器的時候，其他手上的武器不要出現
        for weapon in player2.weapon:
            if player2.present_weapon == weapon :
                if not all_sprites.has(weapon):
                    all_sprites.add(weapon)
            else:
                all_sprites.remove(weapon)

        '''_________________________________________________________________________________________'''

        #player1被player2的子彈射到扣血
        player1.strike(player2_bullet_sprites)
        #player1被player2的刀砍到扣血
        if pygame.sprite.collide_rect(player1,player2_knife) and player2_cut and player2_knife_kill==0:
            player2_knife_kill=1
            player1.life-=5
        # player1死亡從螢幕消失
        if player1.life <= 0:
            player1.rect.x = 2000
            pygame.time.delay(500)
            player2win()
            
        '''_________________________________________________________________________________________'''

        #player2被player1的子彈射到扣血
        player2.strike(player1_bullet_sprites)
        #player2被player1的刀砍到扣血
        if pygame.sprite.collide_rect(player2,player1_knife) and player1_cut and player1_knife_kill==0:
            player1_knife_kill=1
            player2.life-=5
        # player1死亡從螢幕消失
        if player2.life <= 0:
            player2.rect.x = 2000
            pygame.time.delay(500)
            player1win()

        '''_________________________________________________________________________________________'''

        #更新彈夾的狀態
        for clip in clip_sprites:
            clip.new_clip()
            if clip.exist and (clip not in all_sprites):
                all_sprites.add(clip)
        for clip1 in clip_sprites:
            clip1.new_clip()
            if clip1.exist and (clip1 not in all_sprites):
                all_sprites.add(clip1)
        #player1拿槍的時候撿彈夾會加子彈
        if key_pressed[player1.control_list[6]] :
            if  isinstance(player1.present_weapon,Gun) :
                collide_clip = pygame.sprite.spritecollide(player1,clip_sprites,False)
                if len(collide_clip)>0:
                     for clip in collide_clip:
                        if clip.exist:
                            player1.present_weapon.ammunition=min(player1.present_weapon.ammunition+30,player1.present_weapon.max_ammunition)
                            clip.exist=False
                            clip.last_time=pygame.time.get_ticks()
                            all_sprites.remove(clip)

        '''_________________________________________________________________________________________'''

        #player2拿槍的時候撿彈夾會加子彈
        if key_pressed[player2.control_list[6]] :
            if  isinstance(player2.present_weapon,Gun) :
                collide_clip = pygame.sprite.spritecollide(player2,clip_sprites,False)
                if len(collide_clip)>0:
                     for clip in collide_clip:
                        if clip.exist:
                            player2.present_weapon.ammunition=min(player2.present_weapon.ammunition+30,player2.present_weapon.max_ammunition)
                            clip.exist=False
                            clip.last_time=pygame.time.get_ticks()
                            all_sprites.remove(clip)
        '''_________________________________________________________________________________________'''
                    
        def strike(self, bullet_sprites):
            collide_bullet = pygame.sprite.spritecollide(self,bullet_sprites, True)
            if len(collide_bullet) > 0:
                self.life -= 10
        screen.fill(BLUE)
        screen.blit(background, (0, 0))
        
        
        all_sprites.update()
        player1_knife.update()
        all_sprites.draw(screen)
	









def player1win():
    player1winImg = pygame.image.load('p1_won.bmp')
    player1winImg = pygame.transform.scale(player1winImg, (1400, 800))
    screen.blit(player1winImg,(0,0))
    pygame.display.flip()
    run=True
    while run:
          for event in pygame.event.get():
                if event.type == QUIT:
                      sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu()
                    if event.key == K_RETURN:
                        game()
def player2win():
    player2winImg = pygame.image.load('p2_won.bmp')
    player2winImg = pygame.transform.scale(player2winImg, (1400, 800))
    screen.blit(player2winImg,(0,0))
    pygame.display.flip()
    run=True
    while run:
          for event in pygame.event.get():
                if event.type == QUIT:
                      sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu()
                    if event.key == K_RETURN:
                        game()
                
    

def help():
    helpImg = pygame.image.load('help.png')
    screen.blit(helpImg,(0,0))
    pygame.display.flip()
    run=True
    while run:
          for event in pygame.event.get():
                if event.type == QUIT:
                      sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run=False 
                       
                        
def menu():
    screen = pygame.display.set_mode((1400, 800))
    clock = pygame.time.Clock()

    #Background
    bg = pygame.image.load("main_list.jpg")
    bg = pygame.transform.scale(bg, (1400, 800)) 


    #Fonts
    FONT = pygame.font.SysFont ("Broadway", 60)


    text1 = FONT.render("START", True, WHITE)
    text2 = FONT.render("HELP", True, WHITE)
    text3 = FONT.render("QUIT", True, WHITE)



    #Buttons
    rect1 = pygame.Rect(300,300,205,80)
    rect2 = pygame.Rect(300,400,205,80)
    rect3 = pygame.Rect(300,500,205,80)


    buttons = [
        [text1, rect1, BLACK],
        [text2, rect2, BLACK],
        [text3, rect3, BLACK]
        
        ]
    pygame.display.update()
    running = True

    while  running:
            screen.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        if button[1].collidepoint(event.pos):
                            button[2] = HOVER_COLOR
                        
                        else:
                            button[2] = BLACK

                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if rect1.collidepoint(event.pos):
                            
                            buttons[0][2]=(255,255,0)
                        elif rect2.collidepoint(event.pos):
                            buttons[1][2]=(255,255,0)
                        elif rect3.collidepoint(event.pos):
                            buttons[2][2]=(255,255,0)
                for text, rect, color in buttons:
                    pygame.draw.rect(screen, color, rect)
                    screen.blit(text, rect)   
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x,y = pygame.mouse.get_pos()
                        if 300 <= x <= 505 and 300 <= y <= 380:
                            
                            running = False
                            game()
                        if 300 <= x <= 505 and 400 <= y <= 480:
                            #help
                            help()
                            
                        if 300 <= x <= 505 and 500 <= y <= 580:
                            pygame.quit()
                            
                pygame.display.flip()
                clock.tick(60)
menu()








