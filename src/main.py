import pygame

pygame.init()

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

# プレイヤー
player_x = 400
player_y = 300
player_width = 50
player_height = 50

player_speed = 5

# 重力
velocity_y = 0
gravity = 0.8
jump_power = -15
on_ground = False

# 地面
ground_y = 500

# ワールドの広さ
WORLD_WIDTH = 2400

# カメラ
camera_x = 0
camera_y = 0


# フォント
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 36)

# ポーズ状態
paused = False


running = True
while running:
    clock.tick(60)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    if not paused:
        # キー入力
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_d]:
            player_x += player_speed

        if keys[pygame.K_w] and on_ground:
            velocity_y = jump_power
            on_ground = False

        # 重力
        velocity_y += gravity
        player_y += velocity_y

        # 地面との当たり判定
        if player_y + player_height >= ground_y:
            player_y = ground_y - player_height
            velocity_y = 0
            on_ground = True

        # カメラのデッドゾーン
        left_limit = WIDTH * 0.15
        right_limit = WIDTH * 0.85
        # 画面上でのプレイヤー位置
        player_screen_x = player_x - camera_x

        # プレイヤーが左の限界より左に行ったらカメラを左へ
        if player_screen_x < left_limit:
            camera_x = player_x - left_limit

        # プレイヤーが右の限界より右に行ったらカメラを右へ
        elif player_screen_x + player_width > right_limit:
            camera_x = player_x + player_width - right_limit

        # カメラがワールド外を映さないようにする
        if camera_x < 0:
            camera_x = 0

        if camera_x > WORLD_WIDTH - WIDTH:
            camera_x = WORLD_WIDTH - WIDTH

        camera_x = int(camera_x)
    # 描画
    screen.fill(BLACK)

    # 背景の目印として縦線を描く
    for x in range(0, WORLD_WIDTH, 100):
        screen_x = x - camera_x
        pygame.draw.line(screen, WHITE, (screen_x, 0), (screen_x, HEIGHT), 1)

    # 地面を描画
    pygame.draw.rect(
        screen,
        GREEN,
        (0 - camera_x, ground_y - camera_y, WORLD_WIDTH, HEIGHT - ground_y)
    )

    # プレイヤーを描画
    pygame.draw.rect(
        screen,
        BLUE,
        (
            player_x - camera_x,
            player_y - camera_y,
            player_width,
            player_height
        )
    )

    pygame.display.flip()

pygame.quit()