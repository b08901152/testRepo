import pygame
import random
from gameBasic import *
from network import Network


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Twilight War")
clock = pygame.time.Clock()
background = pygame.image.load("../lib/image/map.png")
background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
weaponImage2 = pygame.image.load("../lib/image/machine_gun.png")
weaponImage3 = pygame.image.load("../lib/image/knife.png")
weaponImage = pygame.image.load("../lib/image/gun.png")
clipImg = pygame.image.load("../lib/image/clip.png")
grassImg = pygame.image.load("../lib/image/grass.png")
hideImg = pygame.image.load("../lib/image/hide.png")
hideImg2 = pygame.image.load("../lib/image/hide2.png")

p1temp, p2temp = createCharacter()
gun1 = Gun('1', 100, 100,
           15, 15, weaponImage, 10, 10, p1temp, shoot_delay=1000, isTaken=False)
gun2 = Gun('2', 100+100, 100+100,
           15, 15, weaponImage2, 30, 5, p1temp, shoot_delay=300, isTaken=False)
gun3 = Gun('3', 100+200, 100+200,
           15, 15, weaponImage3, 5, 50, p1temp, shoot_delay=3000, isTaken=False)
clips = []
clips.append(Clip(clipImg,(300,150)))
all_weapons = []
all_weapons.append(gun1)
all_weapons.append(gun2)
all_weapons.append(gun3)
grasses = []
grasses.append(Grass(grassImg,(300,500)))
hides = []
hides.append(Hide(hideImg,(200,400)))





n = Network()
p = n.getP()
p.bullets = []
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    p2 = n.send(p)
    keys = pygame.key.get_pressed()

# <<<<<<< HEAD
#     player1.moveHandleP2(keys, all_weapons,clips)
#     if player1.hiding(hides) ==True:
#         hides = []
#         hides.append(Hide(hideImg2,(200,400)))
#     elif player1.hiding(hides) ==False:
#         hides = []
#         hides.append(Hide(hideImg,(200,400)))

# =======
    p.moveHandleP2(keys, all_weapons,clips)
    # player2.moveHandleP2(keys, player2.bullets)    
    bulletsHandle(p.bullets,p2)
    # bulletsHandle(p2.bullets,p)


    drawScreen(screen, p, p2, background,
               p.bullets, None, all_weapons,clips,grasses,hides)

pygame.quit()
