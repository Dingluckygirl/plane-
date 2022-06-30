import random
import pygame

# 定义屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRANE_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT+1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的方法
        super().__init__()
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed


    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 调用父类实现精灵创建
        super().__init__("./images/background.png")
        # 判断是否为交替图像
        if is_alt:
            self.rect.y = - self.rect.height

    def update(self):
        # 1.调用父类方法
        super().update()

        # 2.判断是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        # 1 调用父类方法，指定敌机图片
        super().__init__("./images/enemy1.png")
        # 2 指定初始随机速度
        self.speed = random.randint(1, 3)
        # 3 指定初始位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 1.调用父类方法
        super().update()
        # 2.判断是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除。。。")
            self.kill()
            # kill 从精灵组移出，精灵就被自动销毁

    def __del__(self):
        pass
        # print("敌机挂了 %s" % self.rect)


class Hero(GameSprite):
    def __init__(self):
        # 1.调用父类方法，设置image&speed
        super().__init__("./images/me1.png", 0)
        # 2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 80
        # 3. 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed
        # 控制英雄不能移出屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹。。。")
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设置精灵位置
            bullet.rect.bottom = self.rect.y - i * 10
            bullet.rect.centerx = self.rect.centerx
            # 添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        # 调用父类方法，垂直飞行
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")
