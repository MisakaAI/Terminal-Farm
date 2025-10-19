from core.save import save_game

def settings(renderer, translator):
    term = renderer.term
    in_settings = True

    while in_settings:
        renderer.draw_settings()
        key = term.inkey(timeout=0.1)
        if not key:
            continue

        current_key = renderer.settings_keys[renderer.selected_index]

        if key.name == "KEY_ESCAPE":
            in_settings = False
        elif key.name == "KEY_UP":
            renderer.selected_index = max(0, renderer.selected_index - 1)
        elif key.name == "KEY_DOWN":
            renderer.selected_index = min(len(renderer.settings_keys) - 1, renderer.selected_index + 1)
        elif key.name in ("KEY_LEFT", "KEY_RIGHT"):
            if current_key == "language":
                options = ["zh-CN", "en-US"]
                current_value = renderer.save_data["settings"]["language"]
                idx = options.index(current_value)
                if key.name == "KEY_LEFT":
                    idx = (idx - 1) % len(options)
                else:
                    idx = (idx + 1) % len(options)
                renderer.save_data["settings"]["language"] = options[idx]
                translator.lang = options[idx]

        # 保存存档
        save_game(renderer.save_data)
