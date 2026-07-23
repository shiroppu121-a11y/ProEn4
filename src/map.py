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


        # 追加したい足場
        self.blocks.extend([
            (400,400),
            (450,400),
            (500,400),

            (700,350),
            (750,350),
            (800,350),
        ])


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