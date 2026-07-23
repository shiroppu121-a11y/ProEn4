import json
from pathlib import Path


# records.py と同じフォルダに保存する
RECORD_FILE = Path(__file__).with_name("clear_times.json")


def load_clear_times():
    """保存済みのクリアタイムを読み込む。"""

    if not RECORD_FILE.exists():
        return []

    try:
        with RECORD_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        # 数値だけを残す
        clear_times = [
            float(clear_time)
            for clear_time in data
            if isinstance(clear_time, (int, float))
        ]

        # 速い順に並べる
        clear_times.sort()

        return clear_times

    except (json.JSONDecodeError, OSError):
        print("クリアタイムの読み込みに失敗しました")
        return []


def save_clear_times(clear_times):
    """クリアタイムをファイルに保存する。"""

    try:
        with RECORD_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                clear_times,
                file,
                ensure_ascii=False,
                indent=4
            )

    except OSError:
        print("クリアタイムの保存に失敗しました")


def add_clear_time(clear_times, new_time):
    """新しいクリアタイムを追加して保存する。"""

    clear_times.append(round(new_time, 2))
    clear_times.sort()

    save_clear_times(clear_times)

    return clear_times