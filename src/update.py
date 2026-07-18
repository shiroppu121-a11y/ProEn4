import pygame

from settings import (
    WIDTH,
    WORLD_WIDTH,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPEED,
    ENEMY_LEFT_LIMIT,
    ENEMY_RIGHT_LIMIT,
    ITEM_WIDTH,
    ITEM_HEIGHT,
    ITEM_SPEED,
    ITEM_LEFT_LIMIT,
    ITEM_RIGHT_LIMIT,
    GOAL_X,
    GOAL_Y,
    GOAL_WIDTH,
    GOAL_HEIGHT,
)


def update_game(state, player, dt, best_time):
    """ゲーム内の各オブジェクトと当たり判定を更新する。"""

    state["elapsed_time"] += dt

    # プレイヤーの移動、ジャンプ、重力を更新
    player.update()

    # その他の処理を更新
    update_camera(state, player)
    update_enemy(state)
    update_item(state)

    # 当たり判定
    best_time = check_collisions(
        state,
        player,
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


def update_enemy(state):
    """敵を左右に移動させる。"""

    state["enemy_x"] += (
        ENEMY_SPEED * state["enemy_direction"]
    )

    # 左端に到達したら右向きにする
    if state["enemy_x"] < ENEMY_LEFT_LIMIT:
        state["enemy_x"] = ENEMY_LEFT_LIMIT
        state["enemy_direction"] = 1

    # 右端に到達したら左向きにする
    if state["enemy_x"] > ENEMY_RIGHT_LIMIT:
        state["enemy_x"] = ENEMY_RIGHT_LIMIT
        state["enemy_direction"] = -1


def update_item(state):
    """取得されていないアイテムを左右に移動させる。"""

    if not state["item_available"]:
        return

    state["item_x"] += (
        ITEM_SPEED * state["item_direction"]
    )

    # 左端に到達したら右向きにする
    if state["item_x"] < ITEM_LEFT_LIMIT:
        state["item_x"] = ITEM_LEFT_LIMIT
        state["item_direction"] = 1

    # 右端に到達したら左向きにする
    if state["item_x"] > ITEM_RIGHT_LIMIT:
        state["item_x"] = ITEM_RIGHT_LIMIT
        state["item_direction"] = -1


def check_collisions(state, player, best_time):
    """プレイヤーと敵、アイテム、ゴールの衝突を調べる。"""

    # Playerクラスから当たり判定を取得
    player_rect = player.get_rect()

    # 敵の当たり判定
    enemy_rect = pygame.Rect(
        state["enemy_x"],
        state["enemy_y"],
        ENEMY_WIDTH,
        ENEMY_HEIGHT
    )

    # ゴールの当たり判定
    goal_rect = pygame.Rect(
        GOAL_X,
        GOAL_Y,
        GOAL_WIDTH,
        GOAL_HEIGHT
    )

    # 敵との衝突
    if player_rect.colliderect(enemy_rect):
        state["game_over"] = True
        print("ゲームオーバー")

        return best_time

    # アイテムとの衝突
    if state["item_available"]:
        item_rect = pygame.Rect(
            state["item_x"],
            state["item_y"],
            ITEM_WIDTH,
            ITEM_HEIGHT
        )

        if player_rect.colliderect(item_rect):
            state["item_available"] = False
            player.speed_up(2)

            print("アイテム獲得")
            print("現在の移動速度:", player.speed)

    # ゴールとの衝突
    if player_rect.colliderect(goal_rect):
        state["goal_reached"] = True
        state["clear_time"] = state["elapsed_time"]

        # ベストタイムを更新
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