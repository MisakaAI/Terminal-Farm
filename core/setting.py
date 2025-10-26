# core/setting.py
# 设置

import json
from pathlib import Path
from blessed import Terminal
from save import SaveData

SAVE_PATH = Path("save.json")
SETTING_JSON = Path("translation/setting.json")


def settings():
    """
    设置界面
    - 支持语言切换
    - 支持 FPS 设置 (30/60)
    - 上下选择设置项，左右修改当前选项
    - 修改后自动保存
    """
    term = Terminal()

    # 加载存档
    save_data = SaveData.load(SAVE_PATH)

    # 加载语言数据
    with SETTING_JSON.open("r", encoding="utf-8") as f:
        lang_data = json.load(f)
    languages = list(lang_data.keys())  # ['zh-CN', 'en-US']

    # 设置选项
    settings_keys = ["language", "fps"]
    selected_index = 0  # 当前选择的设置项

    # FPS 可选值
    fps_options = [30, 60]

    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            while True:
                # 清屏
                print(term.home + term.clear, end="")

                # 当前语言
                current_lang = save_data.settings.get("language", "zh-CN")
                current_fps = save_data.settings.get("fps", 60)

                # 标题
                title = lang_data[current_lang]["title"]
                print(term.move(0, 0) + term.bold + title + term.normal)

                # 帮助提示
                help_text = lang_data[current_lang].get("help", "")
                print(term.move(term.height - 1, 0) + help_text, end="")

                # 打印设置项
                for idx, key in enumerate(settings_keys):
                    prefix = "→ " if idx == selected_index else "  "
                    if key == "language":
                        value_name = lang_data[save_data.settings["language"]]["name"]
                        display = f"{lang_data[current_lang]['language']}: {value_name} <{save_data.settings['language']}>"
                    elif key == "fps":
                        display = f"FPS: {current_fps}"
                    else:
                        display = key
                    print(term.move(2 + idx, 0) + prefix + display)

                # 阻塞式读取键盘
                key = term.inkey()

                if key.name == "KEY_ESCAPE":
                    break
                elif key.name == "KEY_UP":
                    selected_index = max(0, selected_index - 1)
                elif key.name == "KEY_DOWN":
                    selected_index = min(len(settings_keys) - 1, selected_index + 1)
                elif key.name in ("KEY_LEFT", "KEY_RIGHT"):
                    current_key = settings_keys[selected_index]
                    # 修改选项
                    if current_key == "language":
                        idx = languages.index(save_data.settings["language"])
                        if key.name == "KEY_LEFT":
                            idx = (idx - 1) % len(languages)
                        else:
                            idx = (idx + 1) % len(languages)
                        save_data.settings["language"] = languages[idx]
                        save_data.save(SAVE_PATH)
                    elif current_key == "fps":
                        idx = fps_options.index(save_data.settings.get("fps", 60))
                        if key.name == "KEY_LEFT":
                            idx = (idx - 1) % len(fps_options)
                        else:
                            idx = (idx + 1) % len(fps_options)
                        save_data.settings["fps"] = fps_options[idx]
                        save_data.save(SAVE_PATH)

    finally:
        print(term.clear)
        print("设置界面已退出。")


if __name__ == "__main__":
    settings()
