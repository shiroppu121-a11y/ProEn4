import pygame


class Stage:
    def __init__(self):
        self.platforms = [
            # 地面
            pygame.Rect(
                0,
                500,
                2400,
                100
            ),

            # 空中の足場
            pygame.Rect(
                500,
                400,
                250,
                30
            ),

            pygame.Rect(
                900,
                350,
                250,
                30
            ),

            pygame.Rect(
                1400,
                420,
                300,
                30
            ),
        ]

    def draw(
        self,
        screen,
        camera_x,
        camera_y
    ):
        for platform in self.platforms:

            pygame.draw.rect(
                screen,
                (80, 200, 120),
                (
                    platform.x - camera_x,
                    platform.y - camera_y,
                    platform.width,
                    platform.height
                )
            )