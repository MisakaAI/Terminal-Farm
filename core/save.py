import json
from pathlib import Path

SAVE_PATH = Path("save.json")

# 默认存档数据
DEFAULT_SAVE = {
    "player": {"x": 0, "y": 0},
    "season": 0,
    "day": 1,
    "time": 1,
    "settings": {"language": "zh-CN"},
}


def load_save():
    """加载存档，如果没有文件则创建默认存档"""
    if SAVE_PATH.exists():
        try:
            with SAVE_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 文件损坏时重新创建默认存档
            save_game(DEFAULT_SAVE)
            return DEFAULT_SAVE
    else:
        # 文件不存在时创建默认存档
        save_game(DEFAULT_SAVE)
        return DEFAULT_SAVE


def save_game(save_data):
    """保存存档"""
    with SAVE_PATH.open("w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)
