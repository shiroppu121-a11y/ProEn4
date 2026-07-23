import pygame

from settings import (
    PLAYER_INITIAL_SPEED,
    GRAVITY,
    JUMP_POWER,
    GROUND_Y,
    WORLD_WIDTH,
)


class Player:
    def __init__(self):
        self.x = 400
        self.y = 300

        self.image = pygame.image.load(
            "assets/player/player.png"
        ).convert_alpha()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.speed = PLAYER_INITIAL_SPEED

        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        """入力、移動、重力を処理する。"""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

        self.apply_gravity()
        self.keep_inside_world()

    def apply_gravity(self):
        """重力と地面との衝突を処理する。"""

        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.on_ground = True

    def keep_inside_world(self):
        """プレイヤーがワールド外へ出ないようにする。"""

        if self.x < 0:
            self.x = 0

        if self.x + self.width > WORLD_WIDTH:
            self.x = WORLD_WIDTH - self.width

    def get_rect(self):
        """当たり判定用のRectを返す。"""

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def speed_up(self, amount=2):
        """アイテム取得時に移動速度を上げる。"""

        self.speed += amount

    def draw(self, screen, camera_x, camera_y):

        screen.blit(
        self.image,
        (
            self.x - camera_x,
            self.y - camera_y
        )
    )