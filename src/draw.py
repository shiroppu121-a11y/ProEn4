import pygame

from settings import (
    WIDTH,
    HEIGHT,
    WORLD_WIDTH,
    BLACK,
    GREEN,
    WHITE,
    RED,
    YELLOW,
    GROUND_Y,
    GOAL_X,
    GOAL_Y,
    GOAL_WIDTH,
    GOAL_HEIGHT,
)


def draw_screen(
    screen,
    state,
    player,
    enemies,
    items,
    stage,
    font,
    small_font,
    best_time
):
    screen.fill(BLACK)

    # タイトル画面
    if state["scene"] == "title":
        draw_title(
            screen,
            font,
            small_font
        )
        return

    # ゲーム世界を描画
    draw_world(
        screen,
        state,
        player,
        enemies,
        items,
        stage
    )

    # 速度とタイマーを描画
    draw_status(
        screen,
        state,
        player,
        small_font
    )

    # ポーズ画面
    if state["paused"]:
        draw_pause(
            screen,
            font,
            small_font
        )

    # ゲームオーバー画面
    if state["game_over"]:
        draw_game_over(
            screen,
            font,
            small_font
        )

    # ステージクリア画面
    if state["goal_reached"]:
        draw_clear(
            screen,
            state,
            font,
            small_font,
            best_time
        )


def draw_world(
    screen,
    state,
    player,
    enemies,
    items,
    stage
):
    camera_x = state["camera_x"]
    camera_y = state["camera_y"]

    # 背景の縦線
    for x in range(0, WORLD_WIDTH, 100):
        screen_x = x - camera_x

        pygame.draw.line(
            screen,
            WHITE,
            (screen_x, 0),
            (screen_x, HEIGHT),
            1
        )

    # 地面
    # ステージを描画
    stage.draw(
        screen,
        camera_x,
        camera_y
    )

    # ゴールのポール
    pygame.draw.rect(
        screen,
        WHITE,
        (
            GOAL_X - camera_x,
            GOAL_Y - camera_y,
            GOAL_WIDTH,
            GOAL_HEIGHT
        )
    )

    # ゴールの旗
    pygame.draw.polygon(
        screen,
        YELLOW,
        [
            (
                GOAL_X + GOAL_WIDTH - camera_x,
                GOAL_Y - camera_y
            ),
            (
                GOAL_X + GOAL_WIDTH + 60 - camera_x,
                GOAL_Y + 25 - camera_y
            ),
            (
                GOAL_X + GOAL_WIDTH - camera_x,
                GOAL_Y + 50 - camera_y
            )
        ]
    )

    # プレイヤーを描画
    player.draw(
        screen,
        camera_x,
        camera_y
    )

    # すべての敵を描画
    for enemy in enemies:
        enemy.draw(
            screen,
            camera_x,
            camera_y
        )

    # すべてのアイテムを描画
    for item in items:
        item.draw(
            screen,
            camera_x,
            camera_y
        )


def draw_status(
    screen,
    state,
    player,
    small_font
):
    speed_text = small_font.render(
        f"Speed: {player.speed}",
        True,
        WHITE
    )

    timer_text = small_font.render(
        f"Time: {state['elapsed_time']:.2f}",
        True,
        WHITE
    )

    screen.blit(speed_text, (20, 20))
    screen.blit(timer_text, (20, 55))


def draw_overlay(screen, alpha=170):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(alpha)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))


def draw_title(
    screen,
    font,
    small_font
):
    title_text = font.render(
        "2D ACTION GAME",
        True,
        WHITE
    )

    start_text = small_font.render(
        "Press ENTER to start",
        True,
        WHITE
    )

    operation_text = small_font.render(
        "A / D: Move    W: Jump",
        True,
        WHITE
    )

    title_rect = title_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 80
        )
    )

    start_rect = start_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 20
        )
    )

    operation_rect = operation_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 70
        )
    )

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(operation_text, operation_rect)


def draw_pause(
    screen,
    font,
    small_font
):
    draw_overlay(screen, 150)

    pause_text = font.render(
        "PAUSED",
        True,
        WHITE
    )

    guide_text = small_font.render(
        "Press ESC to resume",
        True,
        WHITE
    )

    pause_rect = pause_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 40
        )
    )

    guide_rect = guide_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 30
        )
    )

    screen.blit(pause_text, pause_rect)
    screen.blit(guide_text, guide_rect)


def draw_game_over(
    screen,
    font,
    small_font
):
    draw_overlay(screen)

    game_over_text = font.render(
        "GAME OVER",
        True,
        RED
    )

    guide_text = small_font.render(
        "R: Restart    T: Title",
        True,
        WHITE
    )

    game_over_rect = game_over_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 40
        )
    )

    guide_rect = guide_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 30
        )
    )

    screen.blit(game_over_text, game_over_rect)
    screen.blit(guide_text, guide_rect)


def draw_clear(
    screen,
    state,
    font,
    small_font,
    best_time
):
    draw_overlay(screen)

    clear_text = font.render(
        "STAGE CLEAR",
        True,
        YELLOW
    )

    clear_time_text = small_font.render(
        f"Clear Time: {state['clear_time']:.2f} sec",
        True,
        WHITE
    )

    best_time_text = small_font.render(
        f"Best Time: {best_time:.2f} sec",
        True,
        YELLOW
    )

    guide_text = small_font.render(
        "R: Restart    T: Title",
        True,
        WHITE
    )

    clear_rect = clear_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 90
        )
    )

    clear_time_rect = clear_time_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2
        )
    )

    best_time_rect = best_time_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 40
        )
    )

    guide_rect = guide_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 100
        )
    )

    screen.blit(clear_text, clear_rect)
    screen.blit(clear_time_text, clear_time_rect)
    screen.blit(best_time_text, best_time_rect)
    screen.blit(guide_text, guide_rect)