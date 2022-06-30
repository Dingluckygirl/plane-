import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")

        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建时钟
        self.clock = pygame.time.Clock()
        # 调用精灵组精灵私有方法
        self.__creat_sprites()

    def __creat_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_ground = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 创建子弹
        self.hero_bullets = pygame.sprite.Group()

    def start_game(self):
        print("游戏开始。。。")

        while True:
            # 1. 设置刷新频率
            self.clock.tick(FRANE_PER_SEC)
            # 2  事件监听
            self.__event_handler()
            # 3  碰撞检测
            self.__check_collide()
            # 4  更新精灵组
            self.__update_sprites()
            # 5  更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            #  判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场。。。")
                # 创建敌机精灵，添加到精灵组
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            """
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                print("向右移动")
            # 事件监听，按多长事件都是一次  
            """
        # get_pressed 返回按键元组
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            print("向右移动。。。")
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            print("向左移动。。。")
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 敌机摧毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 判断列表是否有内容
        if len(enemies) > 0:
            print("英雄牺牲")
            self.hero.kill()
            print("结束游戏")
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.back_ground.update()
        self.back_ground.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.start_game()