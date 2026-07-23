import os
import pygame


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


ASSETS_DIR = os.path.join(
    BASE_DIR,
    "assets"
)


def load_image(filename):

    path = os.path.join(
        ASSETS_DIR,
        filename
    )

    image = pygame.image.load(
        path
    ).convert_alpha()

    return image