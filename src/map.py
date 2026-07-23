import pygame
from assets import load_image


class Map:

    def __init__(self):

        self.block_size = 50
        # 先に作る
        self.blocks = []

        # 地面
        for x in range(0,4000,50):
            self.blocks.append(
                (x,500)
            )


        # 少し高い足場
        for x in range(700, 900, self.block_size):
            self.blocks.append((x, 450))

        # 段差
        for x in range(1300, 1500, self.block_size):
            self.blocks.append((x, 400))

        # 足場④：ウサギの前
        for x in range(1700, 1950, self.block_size):
            self.blocks.append((x, 400))


        # 足場⑤：終盤
        for x in range(2300, 2600, self.block_size):
            self.blocks.append((x, 450))

        # 足場⑤：終盤
        for x in range(2800, 3000, self.block_size):
            self.blocks.append((x, 380))

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