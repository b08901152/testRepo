import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, up, down, left, right, attack, change, pick, x, y, w, h, speed=(0, 0)):
        super().__init__()
        self.name = name
        self.speed = speed
        self.rect = pygame.rect.Rect(x, y, w, h)
        # player的生命值
        self.life = 70
        # index從0到6分別代表上下左右 攻擊 換武器 撿武器
        # 要輸入的up,down,left,right是按鍵的名子
        self.control_list = [up, down, left, right, attack, change, pick]

        image = pygame.transform.scale(image, (int(w), int(h)))
        self.image = image
        self.angle = 0  # 用來處理player轉方向的時候，圖也要跟著轉
        self.weapon = []
        self.present_weapon = None

        #screen.blit(self.failImage, self.bounds)

    def update(self, *args):
        pass

    def move_up(self):
        if self.rect.top <= 0:
            pass
        else:
            self.rect.y -= self.speed[1]

    def move_down(self):
        if self.rect.bottom >= screen.get_height():
            pass
        else:
            self.rect.y += self.speed[1]

    def move_left(self):
        if self.rect.left < 0:
            pass
        else:
            self.rect.x -= self.speed[0]

    def move_right(self):
        if self.rect.right > screen.get_width():
            pass
        else:
            self.rect.x += self.speed[0]

    def strike(self, bullet_sprites):
        collide_bullet = pygame.sprite.spritecollide(
            self, bullet_sprites, True)
        if len(collide_bullet) > 0:
            self.life -= 10

    def is_survive(self):
        return self.life > 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.rect.x, self.rect.y-10, 70, 10))
        pygame.draw.rect(screen, (0, 127, 0),
                         (self.rect.x, self.rect.y-10, self.life, 10))


class Bullet(pygame.sprite.Sprite):
    shoot_delay = 500  # 兩發子彈的間隔時間
    last_shoot_time = 0

    def __init__(self, position):
        # position是用來設定子彈的位置
        super().__init__()
        image = pygame.image.load('../lib/image/bullet.png').convert()
        self.image = pygame.transform.scale(image, (20, 5))
        self.rect = self.image.get_rect()
        self.speed = (10, 0)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y -= self.speed[1]


class Gun(pygame.sprite.Sprite):
    def __init__(self, name, x, y, w, h, gun_image, hit):
        super().__init__()
        self.name = name
        image = pygame.transform.scale(gun_image, (int(2*w), int(2*h)))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_ammunition = 10  # 彈藥限制
        self.ammunition = 10  # 現在的彈藥
        self.shoot_delay = 500  # 兩發子彈的間隔時間
        self.last_shoot_time = 0
        self.bullet_speed = 40
        self.gun_origin_image = pygame.Surface.copy(self.image)
        self.gun_turn_image = pygame.Surface.copy(self.image)
        self.hit = hit

    def update(self):
        if self in player1.weapon:
            # player1拿槍之後槍的位置
            self.rect.centerx = player1.rect.centerx
            self.rect.centery = player1.rect.centery
        if self in player2.weapon:
            # player2拿槍之後槍的位置
            self.rect.centerx = player2.rect.centerx
            self.rect.centery = player2.rect.centery

    def new_bullet(self, position):
        if pygame.time.get_ticks() - self.last_shoot_time > self.shoot_delay:
            self.last_shoot_time = pygame.time.get_ticks()
            return Bullet(position)


class Knife(pygame.sprite.Sprite):
    cut_delay = 250

    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()
        image = pygame.image.load('../lib/image/knife.png').convert_alpha()
        image = pygame.transform.scale(image, (int(w), int(h)))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_cut_time = 0

    def update(self):
        pass

    def new_cut(self):
        if pygame.time.get_ticks() - self.last_cut_time > Knife.cut_delay:
            self.last_cut_time = pygame.time.get_ticks()
            return True

    # 彈夾


class Clip(pygame.sprite.Sprite):
    delay = 5000  # 彈夾消失之後下次出現的時間

    def __init__(self, position):
        # position是用來設定彈夾的位置
        super().__init__()
        image = pygame.image.load('../lib/image/clip.png').convert_alpha()
        self.image = pygame.transform.scale(image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.last_time = 0  # 上次消失的時間
        self.exist = True  # 用來表示彈夾現在存不存在

    def update(self):
        pass

    def new_clip(self):
        if pygame.time.get_ticks() - self.last_time > Clip.delay:
            self.exist = True
            return True


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()
        image = pygame.image.load('../lib/image/grass.png').convert_alpha()
        image = pygame.transform.scale(image, (int(4*w), int(4*h)))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class Hide(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()
        image = pygame.image.load('../lib/image/hide.png').convert_alpha()
        image = pygame.transform.scale(image, (int(w), int(h)))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


def show_text(word, color, position, font_size):
    sys_font = pygame.font.SysFont('Comic Sans MS', font_size)
    score_surface = sys_font.render(word, False, color)
    screen.blit(score_surface, position)


def collision(source, target):
    if not source.colliderect(target):  # return bool if collide
        return
    overlap = source.clip(target)
    if overlap.width > overlap.height:  # vert collision
        if source.y < target.y:  # top
            source.bottom = target.top
        else:
            source.top = target.bottom
    else:  # horizontal collision
        if source.x < target.x:  # left
            source.right = target.left
        else:
            source.left = target.right
