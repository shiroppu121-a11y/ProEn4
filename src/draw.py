import pygame
from assets import load_image
from map import Map

from settings import (
    WIDTH,
    HEIGHT,
    BLACK,
    WHITE,
    RED,
    YELLOW,
    GOAL_X,
    GOAL_Y,
    GOAL_WIDTH,
    GOAL_HEIGHT,
)

background_image = load_image(
    "background.png"
)


def draw_screen(
    screen,
    state,
    player,
    enemies,
    items,
    game_map,
    font,
    small_font,
    best_time,
    clear_times
):
    screen.fill(BLACK)

    # タイトル画面
    if state["scene"] == "title":
        draw_title(
            screen,
            font,
            small_font,
            best_time
        )
        return

    # クリアタイム一覧画面
    if state["scene"] == "records":
        draw_records(
            screen,
            font,
            small_font,
            clear_times
        )
        return

    # ゲーム世界を描画
    draw_world(
        screen,
        state,
        player,
        enemies,
        items,
        game_map
    )

    draw_status(
        screen,
        state,
        player,
        small_font
    )

    if state["paused"]:
        draw_pause(
            screen,
            font,
            small_font
        )

    if state["game_over"]:
        draw_game_over(
            screen,
            font,
            small_font
        )

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
    game_map
):

    camera_x = state["camera_x"]
    camera_y = state["camera_y"]

     # 背景を横方向に繰り返し表示
    background_width = background_image.get_width()

    start_x = -(
        camera_x
        % background_width
    )

    for x in range(
        start_x,
        WIDTH,
        background_width
    ):

        screen.blit(
            background_image,
            (
                x,
                -camera_y
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

    game_map.draw(
        screen,
        camera_x,
        camera_y
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

    item_name = {
        "speed":"Speed Up",
        "invincible":"Invincible",
        "throw":"Throw"
    }


    if player.holding_item:

        item_text = small_font.render(
            "ITEM : " + item_name[player.holding_item],
            True,
            YELLOW
        )

        screen.blit(
            item_text,
            (
                WIDTH-250,
                20
            )
        )


def draw_overlay(screen, alpha=170):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(alpha)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))


def draw_title(
    screen,
    font,
    small_font,
    best_time
):
    title_text = font.render(
        "Girl's Adventure",
        True,
        WHITE
    )

    start_text = small_font.render(
        "ENTER: Start",
        True,
        WHITE
    )

    records_text = small_font.render(
        "H: Clear Time Records",
        True,
        YELLOW
    )

    operation_text = small_font.render(
        "A / D: Move    W: Jump",
        True,
        WHITE
    )

    title_rect = title_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 120
        )
    )

    start_rect = start_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 - 20
        )
    )

    records_rect = records_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 30
        )
    )

    operation_rect = operation_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT // 2 + 90
        )
    )

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(records_text, records_rect)
    screen.blit(operation_text, operation_rect)

    # ベストタイムがある場合だけ表示
    if best_time is not None:
        best_text = small_font.render(
            f"Best Time: {best_time:.2f} sec",
            True,
            YELLOW
        )

        best_rect = best_text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 + 140
            )
        )

        screen.blit(best_text, best_rect)


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
    "ESC: Resume    T: Title",
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

def draw_records(
    screen,
    font,
    small_font,
    clear_times
):
    """保存済みのクリアタイム一覧を描画する。"""

    title_text = font.render(
        "CLEAR TIME RECORDS",
        True,
        YELLOW
    )

    title_rect = title_text.get_rect(
        center=(
            WIDTH // 2,
            70
        )
    )

    screen.blit(title_text, title_rect)

    # 記録がない場合
    if not clear_times:
        no_record_text = small_font.render(
            "No clear records yet",
            True,
            WHITE
        )

        no_record_rect = no_record_text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2
            )
        )

        screen.blit(
            no_record_text,
            no_record_rect
        )

    # 記録がある場合
    else:
        # 画面に収めるため上位10件を表示
        display_times = clear_times[:10]

        for index, clear_time in enumerate(display_times):
            rank = index + 1

            if rank == 1:
                color = YELLOW
            else:
                color = WHITE

            record_text = small_font.render(
                f"{rank:2}.  {clear_time:.2f} sec",
                True,
                color
            )

            record_rect = record_text.get_rect(
                center=(
                    WIDTH // 2,
                    145 + index * 36
                )
            )

            screen.blit(
                record_text,
                record_rect
            )

    back_text = small_font.render(
        "ESC / T: Back to Title",
        True,
        WHITE
    )

    back_rect = back_text.get_rect(
        center=(
            WIDTH // 2,
            HEIGHT - 40
        )
    )

    screen.blit(back_text, back_rect)