import pygame

from settings import GROUND_Y


class Map:

    def __init__(self):

        self.blocks = []

        # 地面
        for x in range(0, 2400, 50):

            self.blocks.append(
                pygame.Rect(
                    x,
                    GROUND_Y,
                    50,
                    50
                )
            )


        # 足場
        self.blocks.append(
            pygame.Rect(
                500,
                400,
                200,
                50
            )
        )

        self.blocks.append(
            pygame.Rect(
                900,
                350,
                200,
                50
            )
        )


    def draw(
        self,
        screen,
        camera_x,
        camera_y
    ):

        for block in self.blocks:

            pygame.draw.rect(
                screen,
                (100,80,50),
                (
                    block.x-camera_x,
                    block.y-camera_y,
                    block.width,
                    block.height
                )
            )