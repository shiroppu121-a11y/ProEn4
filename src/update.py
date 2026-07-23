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

    if player.invincible_time > 0:
        player.invincible_time -= 1

    state["elapsed_time"] += dt

    # プレイヤーを更新
    player.update(game_map, enemies)

    check_stage_collision(
        player,
        game_map
    )

    # カメラを更新
    update_camera(state, player)

    # 敵を更新
    for enemy in enemies:
        enemy.update()

    

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
    """プレイヤーを中心にカメラ追従"""

    target_x = (
        player.x
        + player.width // 2
        - WIDTH // 2
    )

    # 滑らかに追従
    state["camera_x"] += (
        target_x - state["camera_x"]
    ) * 0.1


    # 左端制限
    if state["camera_x"] < 0:
        state["camera_x"] = 0


    # 右端制限
    if state["camera_x"] > WORLD_WIDTH - WIDTH:
        state["camera_x"] = WORLD_WIDTH - WIDTH


    state["camera_x"] = int(
        state["camera_x"]
    )

def check_stage_collision(
    player,
    game_map
):

    player_rect = player.get_rect()

    for x, y in game_map.blocks:

        block_rect = pygame.Rect(
            x,
            y,
            game_map.block_size,
            game_map.block_size
        )

        if player_rect.colliderect(block_rect):

            # 上から乗る処理
            if player.velocity_y > 0:

                player.y = (
                    y - player.height
                )

                player.velocity_y = 0
                player.on_ground = True

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

            if player.invincible_time > 0:
                continue

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