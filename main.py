# main.py
import time
from blessed import Terminal
from core.save import load_save, save_game
from core.player import Player
from core.map import World
from renderer.ascii_renderer import AsciiRenderer

VIEW_W, VIEW_H = 50, 20

def main():
    term = Terminal()
    save_data = load_save()
    # init world and player from save
    world = World(width=1000, height=1000)
    player_pos = save_data.get("player", {"x": 500, "y": 500})
    player = Player(x=player_pos.get("x", 500), y=player_pos.get("y", 500))

    renderer = AsciiRenderer(term=term, view_w=VIEW_W, view_h=VIEW_H)

    last_save_time = time.time()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        key = ""
        debug_msgs = ["Welcome"]
        last_tick = time.time()
        # we still want to refresh frequently to keep UI responsive
        while key.lower() != "q":
            now = time.time()
            # 现实时间驱动（每1秒前进1分钟），这个 demo 没实现 GameTime 类，这里仅做刷新计时示例
            if now - last_tick >= 1.0:
                last_tick = now
                # 如果需要在此推进游戏时间，可在此处调用
                debug_msgs = debug_msgs  # keep

            # 以玩家位置为中心渲染视口
            renderer.draw(world, player, debug_lines=debug_msgs)

            # 读取键（非阻塞）
            key = term.inkey(timeout=0.05)
            moved = False
            if key:
                # 处理方向键
                if key.name == "KEY_UP":
                    moved = player.move(0, -1, world)
                elif key.name == "KEY_DOWN":
                    moved = player.move(0, 1, world)
                elif key.name == "KEY_LEFT":
                    moved = player.move(-1, 0, world)
                elif key.name == "KEY_RIGHT":
                    moved = player.move(1, 0, world)
                elif key.lower() == "s":
                    # 手动保存
                    save_data["player"] = {"x": player.x, "y": player.y}
                    save_game(save_data)
                    debug_msgs = [f"Saved at ({player.x},{player.y})"]
                elif key.lower() == "q":
                    break

            # 自动保存：每 5 秒保存一次位置（可选）
            if now - last_save_time >= 5.0:
                save_data["player"] = {"x": player.x, "y": player.y}
                save_game(save_data)
                last_save_time = now

if __name__ == "__main__":
    main()
