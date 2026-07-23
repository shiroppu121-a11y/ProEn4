import pygame
from assets import load_image

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
        enemy_type="slime",
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

        self.velocity_y = 0

        self.jump_timer = 0

        if self.enemy_type == "bat":
            self.image = load_image("bat.png")
        elif self.enemy_type == "slime":
            self.image = load_image("slime.png")
        elif self.enemy_type == "rabbit":
            self.image = load_image("rabbit.png")
        else:
            self.image = load_image("slime.png")

    def update(self):

        if self.enemy_type == "bat":
            self.update_bat()
        elif self.enemy_type == "slime":
            self.update_slime()
        elif self.enemy_type == "rabbit":
            self.update_rabbit()

    def update_bat(self):

        self.x += self.speed * self.direction

        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:
            self.x = self.right_limit
            self.direction = -1

    def update_slime(self):

        self.x += self.speed * self.direction

        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:
            self.x = self.right_limit
            self.direction = -1

    def update_rabbit(self):

        self.x += self.speed * self.direction

        self.velocity_y += 0.8
        self.y += self.velocity_y

        ground_y = 500 - self.height

        if self.y >= ground_y:
            self.y = ground_y
            self.velocity_y = -12

        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:
            self.x = self.right_limit
            self.direction = -1   