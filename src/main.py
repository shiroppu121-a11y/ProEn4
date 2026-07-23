import pygame

from settings import WIDTH, HEIGHT, FPS
from game_state import create_game_state
from update import update_game
import draw
from player import Player
from enemy import Enemy
from item import Item
from stage import Stage


def create_enemies():
    return [
        Enemy(
            x=900,
            y=450,
            left_limit=850,
            right_limit=1150
        ),
        Enemy(
            x=1500,
            y=450,
            left_limit=1400,
            right_limit=1700
        ),
    ]


def create_items():
    return [
        Item(
            x=600,
            y=450,
            left_limit=550,
            right_limit=750,
            effect="speed",
            amount=2
        ),
    ]


def reset_game(scene):

    new_state = create_game_state(scene)
    new_player = Player()
    new_enemies = create_enemies()
    new_items = create_items()
    new_stage = Stage()

    return (
        new_state,
        new_player,
        new_enemies,
        new_items,
        new_stage
    )


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("カメラ追従する2Dゲーム")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 36)

state, player, enemies, items, stage = reset_game("title")

best_time = None
running = True


while running:
    dt = clock.tick(FPS) / 1000

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # タイトル画面
            if state["scene"] == "title":
                if event.key == pygame.K_RETURN:
                    state, player, enemies, items, stage = reset_game("playing")

                    print("ゲーム開始")

            # ゲーム画面
            elif state["scene"] == "playing":
                # ポーズ切り替え
                if event.key == pygame.K_ESCAPE:
                    if (
                        not state["game_over"]
                        and not state["goal_reached"]
                    ):
                        state["paused"] = not state["paused"]

                # リスタート
                if event.key == pygame.K_r:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state, player, enemies, items, stage = reset_game("playing")

                        print("リスタート")

                # タイトルへ戻る
                if event.key == pygame.K_t:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state, player, enemies, items, stage = reset_game("title")

                        print("タイトル画面に戻る")

    # ゲーム更新
    if (
        state["scene"] == "playing"
        and not state["paused"]
        and not state["game_over"]
        and not state["goal_reached"]
    ):
        best_time = update_game(
            state,
            player,
            enemies,
            items,
            stage,
            dt,
            best_time
        )

    # 描画
    draw.draw_screen(
        screen,
        state,
        player,
        enemies,
        items,
        stage,
        font,
        small_font,
        best_time
    )

    pygame.display.flip()


pygame.quit()