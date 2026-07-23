import pygame
import random

from settings import (
    ITEM_WIDTH,
    ITEM_HEIGHT,
    YELLOW,
)


ITEM_TYPES = [
    "speed",
    "invincible",
    "throw",
]


class Item:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.width = ITEM_WIDTH
        self.height = ITEM_HEIGHT

        # ランダム決定
        self.type = random.choice(
            ITEM_TYPES
        )

        self.available = True


    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


    def collect(self, player):

        # すでに持っていたら取得不可
        if player.holding_item:
            return


        player.holding_item = self.type

        print(
            "取得:",
            self.type
        )

        self.available = False



    def draw(
        self,
        screen,
        camera_x,
        camera_y
    ):

        if not self.available:
            return


        pygame.draw.rect(
            screen,
            YELLOW,
            (
                self.x-camera_x,
                self.y-camera_y,
                self.width,
                self.height
            )
        )