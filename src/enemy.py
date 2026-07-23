import pygame

from settings import (
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPEED,
    GROUND_Y,
)

from assets import load_image


class Enemy:

    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit,
        enemy_type="slime"
    ):

        self.x = x
        self.y = y

        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.enemy_type = enemy_type


        self.speed = ENEMY_SPEED
        self.direction = 1

        # ジャンプ用
        self.velocity_y = 0
        self.on_ground = False

        # 敵の種類ごとに画像を読み込む
        # 画像読み込み
        if self.enemy_type == "bat":

            self.image = load_image(
                "bat.png"
            )

            self.image = pygame.transform.scale(
                self.image,
                (100, 70)
            )

        elif self.enemy_type == "slime":

            self.image = load_image(
                "slime.png"
            )

            self.image = pygame.transform.scale(
                self.image,
                (70, 70)
            )

        elif self.enemy_type == "rabbit":

            self.image = load_image(
                "rabbit.png"
            )

            self.image = pygame.transform.scale(
                self.image,
                (80, 100)
            )


        # 画像の大きさを当たり判定に合わせる
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):

        if self.enemy_type == "bat":

                self.update_bat()

        elif self.enemy_type == "slime":

            self.update_slime()

        elif self.enemy_type == "rabbit":

            self.update_rabbit()

    def update_bat(self):

        # 空中を左右に移動
        self.x += (
            self.speed
            * self.direction
        )

        if self.x < self.left_limit:

            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:

            self.x = self.right_limit
            self.direction = -1

    def update_slime(self):

        # 地面を左右に移動
        self.x += (
            self.speed
            * self.direction
        )

        if self.x < self.left_limit:

            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:

            self.x = self.right_limit
            self.direction = -1

    def update_rabbit(self):

        # 重力
        self.velocity_y += 0.8

        self.y += self.velocity_y

        # 地面に着地
        if self.y + self.height >= GROUND_Y:

            self.y = GROUND_Y - self.height

            self.velocity_y = 0

            self.on_ground = True

        # 左右移動
        self.x += (
            self.speed
            * self.direction
        )

        if self.x < self.left_limit:

            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:

            self.x = self.right_limit
            self.direction = -1

        # 着地したらジャンプ
        if self.on_ground:

            self.velocity_y = -12

            self.on_ground = False

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(
        self,
        screen,
        camera_x,
        camera_y
    ):

        screen.blit(
            self.image,
            (
                self.x - camera_x,
                self.y - camera_y
            )
        )