import pygame

from settings import (
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPEED,
    RED,
)


class Enemy:
    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit,
        speed=ENEMY_SPEED
    ):
        self.x = x
        self.y = y

        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT

        self.speed = speed
        self.direction = 1

        self.left_limit = left_limit
        self.right_limit = right_limit

    def update(self):
        """敵を左右に移動させる。"""

        self.x += self.speed * self.direction

        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:
            self.x = self.right_limit
            self.direction = -1

    def get_rect(self):
        """当たり判定用のRectを返す。"""

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, screen, camera_x, camera_y):
        """敵を画面に描画する。"""

        pygame.draw.rect(
            screen,
            RED,
            (
                self.x - camera_x,
                self.y - camera_y,
                self.width,
                self.height
            )
        )
    
    