import pygame
import random

from settings import (
    PLAYER_INITIAL_SPEED,
    GRAVITY,
    JUMP_POWER,
    WORLD_WIDTH,
)


class Player:

    def __init__(self):

        self.x = 400
        self.y = 300

        self.image = pygame.image.load(
            "assets/player/player.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (50, 110)
        )

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.speed = PLAYER_INITIAL_SPEED
        self.holding_item = None

        self.velocity_y = 0
        self.on_ground = False

        # 無敵時間
        self.invincible_time = 0

        self.bullet = None


    def update(self, game_map, enemies):

        keys = pygame.key.get_pressed()

        dx = 0

        if keys[pygame.K_a]:
            dx -= self.speed

        if keys[pygame.K_d]:
            dx += self.speed


        # 横移動
        self.x += dx

        # 横衝突
        self.check_horizontal_collision(
            game_map,
            dx
        )


        # ジャンプ
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False


        # 重力
        self.apply_gravity(game_map)

        self.keep_inside_world()

        if self.bullet:

            self.bullet.update(
                enemies
            )

            if not self.bullet.active:
                self.bullet = None



    def apply_gravity(
        self,
        game_map
    ):

        self.velocity_y += GRAVITY

        self.y += self.velocity_y

        self.on_ground = False


        player_rect = self.get_rect()


        for x, y in game_map.blocks:

            block_rect = pygame.Rect(
                x,
                y,
                game_map.block_size,
                game_map.block_size
            )


            if player_rect.colliderect(block_rect):


                # 落下中
                if self.velocity_y > 0:

                    self.y = (
                        y - self.height
                    )

                    self.velocity_y = 0
                    self.on_ground = True


                # 上方向に衝突
                elif self.velocity_y < 0:

                    self.y = (
                        y + game_map.block_size
                    )

                    self.velocity_y = 0


    def use_item(self, enemies):

        if self.holding_item is None:
            return


        item = self.holding_item


        # スピードアップ
        if item == "speed":

            self.speed += 3
            print("スピードアップ")


        # 無敵5秒
        elif item == "invincible":

            self.invincible_time = 5
            print("5秒間無敵")


        # 投擲
        elif item == "throw":

            from bullet import Bullet

            self.bullet = Bullet(
                self.x + self.width,
                self.y + self.height // 2
            )

            print("投擲")


        self.holding_item = None

    def check_horizontal_collision(
            self,
            game_map,
            dx
        ):

        player_rect = self.get_rect()

        for x, y in game_map.blocks:

            block_rect = pygame.Rect(
                x,
                y,
                game_map.block_size,
                game_map.block_size
            )


            if player_rect.colliderect(block_rect):

                # 右へ移動中
                if dx > 0:
                    self.x = block_rect.left - self.width

                # 左へ移動中
                elif dx < 0:
                    self.x = block_rect.right



    def keep_inside_world(self):

        if self.x < 0:
            self.x = 0


        if self.x + self.width > WORLD_WIDTH:

            self.x = (
                WORLD_WIDTH - self.width
            )



    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )



    def speed_up(
        self,
        amount=2
    ):

        self.speed += amount



    def draw(self, screen, camera_x, camera_y):

        screen.blit(
            self.image,
            (
                self.x - camera_x,
                self.y - camera_y
            )
        )

        if self.bullet:

            self.bullet.draw(
                screen,
                camera_x,
                camera_y
            )
