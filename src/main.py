import pygame

from settings import WIDTH, HEIGHT, FPS
from game_state import create_game_state
from update import update_game
import draw
from player import Player
from enemy import Enemy
from item import Item
from records import load_clear_times, add_clear_time
from map import Map

def create_enemies():
    """ステージに配置する敵を作成する。"""

    return [

        Enemy(
            x=550,
            y=380,
            left_limit=400,
            right_limit=650,
            enemy_type="slime"
        ),

        Enemy(
            x=1200,
            y=300,
            left_limit=1150,
            right_limit=1250,
            enemy_type="bat"
        ),

        Enemy(
            x=1850,
            y=450,
            left_limit=1800,
            right_limit=1900,
            enemy_type="rabbit"
        ),

    ]
def create_items():
    """アイテム出現地点"""

    return [
        Item(
            x=800,
            y=330
        ),

        Item(
            x=1500,
            y=430
        ),

        Item(
            x=1600,
            y=330
        ),
    ]

def reset_game(scene):

    new_state = create_game_state(scene)
    new_player = Player()
    new_enemies = create_enemies()
    new_items = create_items()
    new_map = Map()

    return (
        new_state,
        new_player,
        new_enemies,
        new_items,
        new_map
    )
   


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("カメラ追従する2Dゲーム")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 36)

# 保存済みのクリアタイムを読み込む
clear_times = load_clear_times()

# ベストタイムを設定する
if clear_times:
    best_time = clear_times[0]
else:
    best_time = None

state, player, enemies, items, game_map = reset_game("title")

running = True


while running:
    dt = clock.tick(FPS) / 1000

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # タイトル画面
            if state["scene"] == "title":
                # Enterキーでゲーム開始
                if event.key == pygame.K_RETURN:
                    state, player, enemies, items, game_map = reset_game("playing")

                    print("ゲーム開始")

                # Hキーで記録画面を開く
                if event.key == pygame.K_h:
                    state["scene"] = "records"

            # 記録画面
            elif state["scene"] == "records":
                # EscキーまたはTキーでタイトルへ戻る
                if (
                    event.key == pygame.K_ESCAPE
                    or event.key == pygame.K_t
                ):
                    state, player, enemies, items, game_map = reset_game("title")

            # ゲーム画面
            elif state["scene"] == "playing":
                # Escキーでポーズ切り替え
                if event.key == pygame.K_ESCAPE:
                    if (
                        not state["game_over"]
                        and not state["goal_reached"]
                    ):
                        state["paused"] = not state["paused"]

                # Rキーでリスタート
                if event.key == pygame.K_r:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state, player, enemies, items, game_map = reset_game("playing")

                        print("リスタート")

                # Tキーでタイトルへ戻る
                if event.key == pygame.K_t:
                    if (
                        state["game_over"]
                        or state["goal_reached"]
                    ):
                        state, player, enemies, items, game_map = reset_game("title")

                        print("タイトル画面に戻る")

                # Eキーでアイテム使用
                if event.key == pygame.K_e:

                    print("E押された")
                    print("所持:", player.holding_item)

                    if player.holding_item is not None:

                        player.use_item(enemies)

                        print("アイテム使用")

    # ゲーム更新
    if (
        state["scene"] == "playing"
        and not state["paused"]
        and not state["game_over"]
        and not state["goal_reached"]
    ):
        # 更新前のゴール状態
        goal_was_reached = state["goal_reached"]

        best_time = update_game(
            state,
            player,
            enemies,
            items,
            game_map,
            dt,
            best_time
        )
        # このフレームで初めてゴールした場合
        if (
            not goal_was_reached
            and state["goal_reached"]
            and state["clear_time"] is not None
        ):
            clear_times = add_clear_time(
                clear_times,
                state["clear_time"]
            )

            # 最速記録をベストタイムにする
            best_time = clear_times[0]

            print(
                "クリアタイムを保存しました:",
                state["clear_time"]
            )

    # 描画
    draw.draw_screen(
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
    )

    pygame.display.flip()


pygame.quit()