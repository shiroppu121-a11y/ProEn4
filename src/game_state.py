from settings import PLAYER_INITIAL_SPEED


def create_game_state(scene="title"):
    return {
        "scene": scene,

        # 敵
        "enemy_x": 900,
        "enemy_y": 450,
        "enemy_direction": 1,

        # アイテム
        "item_x": 600,
        "item_y": 450,
        "item_direction": 1,
        "item_available": True,

        # カメラ
        "camera_x": 0,
        "camera_y": 0,

        # タイマー
        "elapsed_time": 0.0,
        "clear_time": None,

        # ゲーム状態
        "paused": False,
        "game_over": False,
        "goal_reached": False,
    }