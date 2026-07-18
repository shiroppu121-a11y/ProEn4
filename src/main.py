import pygame

pygame.init()

# 画面設定
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("カメラ追従する2Dゲーム")

clock = pygame.time.Clock()

# 色
BLACK = (30, 30, 30)
BLUE = (0, 200, 255)
GREEN = (80, 200, 120)
WHITE = (240, 240, 240)
RED = (255, 80, 80)
YELLOW = (255, 220, 80)

# プレイヤー設定
player_width = 50
player_height = 50

# 敵mob設定
enemy_width = 50
enemy_height = 50
enemy_speed = 2

# アイテム設定
item_width = 50
item_height = 50
item_speed = 3

# 重力設定
gravity = 0.8
jump_power = -15

# 地面
ground_y = 500

# ゴール設定
goal_width = 25
goal_height = 100
goal_x = 1200
goal_y = ground_y - goal_height

# ワールドの広さ
WORLD_WIDTH = 2400

# フォント
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 36)


# ゲーム状態を作る関数
def create_game_state(scene="title"):
    return {
        # 現在の画面
        "scene": scene,

        # プレイヤー
        "player_x": 400,
        "player_y": 300,
        "player_speed": 5,
        "velocity_y": 0,
        "on_ground": False,

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

        # ゲーム状態
        "paused": False,
        "game_over": False,
        "goal_reached": False,
    }


state = create_game_state()

running = True

while running:
    clock.tick(60)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # タイトル画面の入力
            if state["scene"] == "title":
                if event.key == pygame.K_RETURN:
                    state = create_game_state("playing")
                    print("ゲーム開始")

            # ゲーム中の入力
            elif state["scene"] == "playing":

                # Escキーでポーズ切り替え
                if event.key == pygame.K_ESCAPE:
                    if (
                        not state["game_over"]
                        and not state["goal_reached"]
                    ):
                        state["paused"] = not state["paused"]

                # ゲームオーバーまたはクリア後にRキーで再開
                if event.key == pygame.K_r:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state = create_game_state("playing")
                        print("リスタート")

    # ゲームの更新
    if (
        state["scene"] == "playing"
        and not state["paused"]
        and not state["game_over"]
        and not state["goal_reached"]
    ):
        keys = pygame.key.get_pressed()

        # 左右移動
        if keys[pygame.K_a]:
            state["player_x"] -= state["player_speed"]

        if keys[pygame.K_d]:
            state["player_x"] += state["player_speed"]

        # ジャンプ
        if keys[pygame.K_w] and state["on_ground"]:
            state["velocity_y"] = jump_power
            state["on_ground"] = False
            print("ジャンプ")

        # 重力
        state["velocity_y"] += gravity
        state["player_y"] += state["velocity_y"]

        # 地面との当たり判定
        if state["player_y"] + player_height >= ground_y:
            state["player_y"] = ground_y - player_height
            state["velocity_y"] = 0
            state["on_ground"] = True

        # プレイヤーがワールド外に出ないようにする
        if state["player_x"] < 0:
            state["player_x"] = 0

        if state["player_x"] + player_width > WORLD_WIDTH:
            state["player_x"] = WORLD_WIDTH - player_width

        # カメラのデッドゾーン
        left_limit = WIDTH * 0.15
        right_limit = WIDTH * 0.85

        # 画面上でのプレイヤー位置
        player_screen_x = (
            state["player_x"] - state["camera_x"]
        )

        # 左側の限界を超えたらカメラを動かす
        if player_screen_x < left_limit:
            state["camera_x"] = (
                state["player_x"] - left_limit
            )

        # 右側の限界を超えたらカメラを動かす
        elif player_screen_x + player_width > right_limit:
            state["camera_x"] = (
                state["player_x"]
                + player_width
                - right_limit
            )

        # カメラがワールド外を映さないようにする
        if state["camera_x"] < 0:
            state["camera_x"] = 0

        if state["camera_x"] > WORLD_WIDTH - WIDTH:
            state["camera_x"] = WORLD_WIDTH - WIDTH

        state["camera_x"] = int(state["camera_x"])

        # 敵mobの移動
        state["enemy_x"] += (
            enemy_speed * state["enemy_direction"]
        )

        # 敵の移動範囲
        if state["enemy_x"] < 850:
            state["enemy_x"] = 850
            state["enemy_direction"] = 1

        if state["enemy_x"] > 1150:
            state["enemy_x"] = 1150
            state["enemy_direction"] = -1

        # アイテムが存在するときだけ移動させる
        if state["item_available"]:
            state["item_x"] += (
                item_speed * state["item_direction"]
            )

            # アイテムの移動範囲
            if state["item_x"] < 550:
                state["item_x"] = 550
                state["item_direction"] = 1

            if state["item_x"] > 750:
                state["item_x"] = 750
                state["item_direction"] = -1

        # プレイヤーの当たり判定
        player_rect = pygame.Rect(
            state["player_x"],
            state["player_y"],
            player_width,
            player_height
        )

        # 敵の当たり判定
        enemy_rect = pygame.Rect(
            state["enemy_x"],
            state["enemy_y"],
            enemy_width,
            enemy_height
        )

        # ゴールの当たり判定
        goal_rect = pygame.Rect(
            goal_x,
            goal_y,
            goal_width,
            goal_height
        )

        # 敵との衝突
        if player_rect.colliderect(enemy_rect):
            state["game_over"] = True
            print("ゲームオーバー")

        # アイテムが存在するときだけ当たり判定する
        if state["item_available"]:
            item_rect = pygame.Rect(
                state["item_x"],
                state["item_y"],
                item_width,
                item_height
            )

            # アイテムの獲得
            if player_rect.colliderect(item_rect):
                state["item_available"] = False
                state["player_speed"] += 2

                print("アイテム獲得")
                print(
                    "現在の移動速度:",
                    state["player_speed"]
                )

        # ゲームオーバーになっていない場合だけゴール判定
        if not state["game_over"]:
            if player_rect.colliderect(goal_rect):
                state["goal_reached"] = True
                print("ゴール！")

    # 描画開始
    screen.fill(BLACK)

    # ゲーム画面を描画
    if state["scene"] == "playing":

        # 背景の目印として縦線を描画
        for x in range(0, WORLD_WIDTH, 100):
            screen_x = x - state["camera_x"]

            pygame.draw.line(
                screen,
                WHITE,
                (screen_x, 0),
                (screen_x, HEIGHT),
                1
            )

        # 地面を描画
        pygame.draw.rect(
            screen,
            GREEN,
            (
                -state["camera_x"],
                ground_y - state["camera_y"],
                WORLD_WIDTH,
                HEIGHT - ground_y
            )
        )

        # ゴールを描画
        pygame.draw.rect(
            screen,
            WHITE,
            (
                goal_x - state["camera_x"],
                goal_y - state["camera_y"],
                goal_width,
                goal_height
            )
        )

        # ゴールの旗を描画
        pygame.draw.polygon(
            screen,
            YELLOW,
            [
                (
                    goal_x
                    + goal_width
                    - state["camera_x"],
                    goal_y - state["camera_y"]
                ),
                (
                    goal_x
                    + goal_width
                    + 60
                    - state["camera_x"],
                    goal_y
                    + 25
                    - state["camera_y"]
                ),
                (
                    goal_x
                    + goal_width
                    - state["camera_x"],
                    goal_y
                    + 50
                    - state["camera_y"]
                )
            ]
        )

        # プレイヤーを描画
        pygame.draw.rect(
            screen,
            BLUE,
            (
                state["player_x"] - state["camera_x"],
                state["player_y"] - state["camera_y"],
                player_width,
                player_height
            )
        )

        # 敵mobを描画
        pygame.draw.rect(
            screen,
            RED,
            (
                state["enemy_x"] - state["camera_x"],
                state["enemy_y"] - state["camera_y"],
                enemy_width,
                enemy_height
            )
        )

        # アイテムを描画
        if state["item_available"]:
            pygame.draw.rect(
                screen,
                YELLOW,
                (
                    state["item_x"] - state["camera_x"],
                    state["item_y"] - state["camera_y"],
                    item_width,
                    item_height
                )
            )

        # 現在の移動速度を表示
        speed_text = small_font.render(
            f"Speed: {state['player_speed']}",
            True,
            WHITE
        )

        screen.blit(speed_text, (20, 20))

        # ポーズ画面
        if state["paused"]:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

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

        # ゲームオーバー画面
        if state["game_over"]:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            game_over_text = font.render(
                "GAME OVER",
                True,
                RED
            )

            restart_text = small_font.render(
                "Press R to restart",
                True,
                WHITE
            )

            game_over_rect = game_over_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 40
                )
            )

            restart_rect = restart_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 + 30
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            screen.blit(
                restart_text,
                restart_rect
            )

        # ステージクリア画面
        if state["goal_reached"]:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(170)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            clear_text = font.render(
                "STAGE CLEAR",
                True,
                YELLOW
            )

            restart_text = small_font.render(
                "Press R to restart",
                True,
                WHITE
            )

            clear_rect = clear_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 40
                )
            )

            restart_rect = restart_text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 + 30
                )
            )

            screen.blit(clear_text, clear_rect)
            screen.blit(restart_text, restart_rect)

    # タイトル画面
    if state["scene"] == "title":
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

    pygame.display.flip()

pygame.quit()