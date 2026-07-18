import pygame

from settings import WIDTH, HEIGHT, FPS
from game_state import create_game_state
from update import update_game
from draw import draw_screen
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("カメラ追従する2Dゲーム")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 36)

state = create_game_state()
player = Player()
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
                    state = create_game_state("playing")
                    player = Player()
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
                        state = create_game_state("playing")
                        player = Player()
                        print("リスタート")

                # タイトルへ戻る
                if event.key == pygame.K_t:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state = create_game_state("title")
                        player = Player()
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
            dt,
            best_time
        )

    # 描画
    draw_screen(
        screen,
        state,
        player,
        font,
        small_font,
        best_time
    )

    pygame.display.flip()


pygame.quit()