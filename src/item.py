import pygame

from settings import (
    ITEM_WIDTH,
    ITEM_HEIGHT,
    ITEM_SPEED,
    YELLOW,
)


class Item:
    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit,
        effect="speed",
        amount=2,
        speed=ITEM_SPEED
    ):
        self.x = x
        self.y = y

        self.width = ITEM_WIDTH
        self.height = ITEM_HEIGHT

        self.speed = speed
        self.direction = 1

        self.left_limit = left_limit
        self.right_limit = right_limit

        self.effect = effect
        self.amount = amount
        self.available = True

    def update(self):
        """取得されていないアイテムを左右に動かす。"""

        if not self.available:
            return

        self.x += self.speed * self.direction

        if self.x < self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        if self.x > self.right_limit:
            self.x = self.right_limit
            self.direction = -1

    def apply_effect(self, player):
        """アイテムの効果をプレイヤーへ適用する。"""

        if self.effect == "speed":
            player.speed_up(self.amount)

    def collect(self, player):
        """アイテムを取得する。"""

        if not self.available:
            return

        self.apply_effect(player)
        self.available = False

        print("アイテム獲得")
        print("現在の移動速度:", player.speed)

    def get_rect(self):
        """当たり判定用の四角形を返す。"""

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, screen, camera_x, camera_y):
        """取得されていない場合だけ描画する。"""

        if not self.available:
            return

        pygame.draw.rect(
            screen,
            YELLOW,
            (
                self.x - camera_x,
                self.y - camera_y,
                self.width,
                self.height
            )
        )