import pygame
from assets import load_image


class Map:

    def __init__(self):

        self.block_size = 50
        # 先に作る
        self.blocks = []

        # 地面
        for x in range(0,2400,50):
            self.blocks.append(
                (x,500)
            )


        # 少し高い足場
        for x in range(700, 900, self.block_size):
            self.blocks.append((x, 450))

        # 段差
        for x in range(1300, 1500, self.block_size):
            self.blocks.append((x, 400))


        self.block_image = load_image(
            "ground.png"
        )


    def draw(
        self,
        screen,
        camera_x,
        camera_y
    ):

        for x,y in self.blocks:

            screen.blit(
                self.block_image,
                (
                    x-camera_x,
                    y-camera_y
                )
            )