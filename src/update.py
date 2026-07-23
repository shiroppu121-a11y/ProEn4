import pygame

from settings import (
    WIDTH,
    WORLD_WIDTH,
    GOAL_X,
    GOAL_Y,
    GOAL_WIDTH,
    GOAL_HEIGHT,
)


def update_game(
    state,
    player,
    enemies,
    items,
    game_map,
    dt,
    best_time
):
    state["elapsed_time"] += dt

    # プレイヤーを更新
    player.update()

    check_stage_collision(
        player,
        game_map
    )

    # カメラを更新
    update_camera(state, player)

    # 敵を更新
    for enemy in enemies:
        enemy.update()

    # アイテムを更新
    for item in items:
        item.update()

    # 当たり判定
    best_time = check_collisions(
        state,
        player,
        enemies,
        items,
        best_time
    )

    return best_time


def update_camera(state, player):
    """プレイヤーの位置に応じてカメラを動かす。"""

    left_limit = WIDTH * 0.15
    right_limit = WIDTH * 0.85

    # 画面上でのプレイヤー位置
    player_screen_x = (
        player.x - state["camera_x"]
    )

    # プレイヤーが画面左側の限界を超えた場合
    if player_screen_x < left_limit:
        state["camera_x"] = (
            player.x - left_limit
        )

    # プレイヤーが画面右側の限界を超えた場合
    elif player_screen_x + player.width > right_limit:
        state["camera_x"] = (
            player.x
            + player.width
            - right_limit
        )

    # カメラをワールド内に制限
    state["camera_x"] = max(
        0,
        min(
            state["camera_x"],
            WORLD_WIDTH - WIDTH
        )
    )

    state["camera_x"] = int(state["camera_x"])

def check_stage_collision(player, game_map):

    player_rect = player.get_rect()


    for block in game_map.blocks:

        if player_rect.colliderect(block):

            # 上から乗る
            if player.velocity_y > 0:

                player.y = (
                    block.y
                    -
                    player.height
                )

                player.velocity_y = 0
                player.on_ground=True

def check_collisions(
    state,
    player,
    enemies,
    items,
    best_time
):
    player_rect = player.get_rect()

    goal_rect = pygame.Rect(
        GOAL_X,
        GOAL_Y,
        GOAL_WIDTH,
        GOAL_HEIGHT
    )

    # すべての敵との衝突を確認
    for enemy in enemies:
        if player_rect.colliderect(enemy.get_rect()):
            state["game_over"] = True
            print("ゲームオーバー")

            enemy.update()

            return best_time

    # すべてのアイテムとの衝突を確認
    for item in items:
        if not item.available:
            continue

        if player_rect.colliderect(item.get_rect()):
            item.collect(player)

    # ゴールとの衝突
    if player_rect.colliderect(goal_rect):
        state["goal_reached"] = True
        state["clear_time"] = state["elapsed_time"]

        if (
            best_time is None
            or state["clear_time"] < best_time
        ):
            best_time = state["clear_time"]
            print("ベストタイム更新")

        print(
            f"クリアタイム: "
            f"{state['clear_time']:.2f}秒"
        )

    return best_time