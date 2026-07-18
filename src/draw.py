import pygame

from settings import (
    WIDTH,
    HEIGHT,
    WORLD_WIDTH,
    BLACK,
    BLUE,
    GREEN,
    WHITE,
    RED,
    YELLOW,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ITEM_WIDTH,
    ITEM_HEIGHT,
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
    font,
    small_font,
    best_time
):
    screen.fill(BLACK)

    if state["scene"] == "title":
        draw_title(screen, font, small_font)
        return

    draw_world(screen,
               state,
                player
    )
    draw_status(screen, state, player, small_font)

    if state["paused"]:
        draw_pause(screen, font, small_font)

    if state["game_over"]:
        draw_game_over(screen, font, small_font)

    if state["goal_reached"]:
        draw_clear(
            screen,
            state,
            font,
            small_font,
            best_time
        )


def draw_world(screen, state, player):
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
    pygame.draw.rect(
        screen,
        GREEN,
        (
            -camera_x,
            GROUND_Y - camera_y,
            WORLD_WIDTH,
            HEIGHT - GROUND_Y
        )
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

    # プレイヤー
    player.draw(
        screen,
        camera_x,
        camera_y
        )

    # 敵
    pygame.draw.rect(
        screen,
        RED,
        (
            state["enemy_x"] - camera_x,
            state["enemy_y"] - camera_y,
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )
    )

    # アイテム
    if state["item_available"]:
        pygame.draw.rect(
            screen,
            YELLOW,
            (
                state["item_x"] - camera_x,
                state["item_y"] - camera_y,
                ITEM_WIDTH,
                ITEM_HEIGHT
            )
        )


def draw_status(screen, state, player, small_font):
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


def draw_title(screen, font, small_font):
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

    screen.blit(
        title_text,
        title_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 80)
        )
    )

    screen.blit(
        start_text,
        start_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 20)
        )
    )

    screen.blit(
        operation_text,
        operation_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 70)
        )
    )


def draw_pause(screen, font, small_font):
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

    screen.blit(
        pause_text,
        pause_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 40)
        )
    )

    screen.blit(
        guide_text,
        guide_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 30)
        )
    )


def draw_game_over(screen, font, small_font):
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

    screen.blit(
        game_over_text,
        game_over_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 40)
        )
    )

    screen.blit(
        guide_text,
        guide_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 30)
        )
    )


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

    screen.blit(
        clear_text,
        clear_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 90)
        )
    )

    screen.blit(
        clear_time_text,
        clear_time_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )
    )

    screen.blit(
        best_time_text,
        best_time_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 40)
        )
    )

    screen.blit(
        guide_text,
        guide_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 100)
        )
    )