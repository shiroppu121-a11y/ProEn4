def create_game_state(scene="title"):
    return {
        "scene": scene,

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