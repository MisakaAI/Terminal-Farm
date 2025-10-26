# main.py
import time
import threading
from pathlib import Path
from blessed import Terminal
from core.save import SaveData
from core.player import Player
from core.world import World
from core.time import GameTime
from translation import Translator
from renderer.ascii_renderer import AsciiRenderer
from core.control import Control
from core.save import SaveData

# 游戏视口尺寸
VIEW_W, VIEW_H = 0, 20
# 存档路径
SAVE_PATH = Path("save.json")


def main():
    # 初始化终端对象
    term = Terminal()

    # 加载存档
    save_data = SaveData.load(SAVE_PATH)

    # 初始化翻译器
    translator = Translator(lang=save_data.settings["language"])

    # 游戏渲染帧率
    fps = save_data.settings["fps"]

    # 加载地图
    map_path = save_data.world
    if not Path(map_path).exists():
        map_path = f"map/{map_path}.npy"
    world = World(map_path)

    # 加载游戏时间
    game_time = GameTime(
        save_data=save_data.time,
        translator=translator,
    )

    # 从存档中加载玩家位置
    player_pos = save_data.player
    player = Player(x=player_pos.get("x"), y=player_pos.get("y"))

    # 初始化渲染器
    renderer = AsciiRenderer(term=term, view_w=VIEW_W, view_h=VIEW_H)

    # 初始化控制器
    control = Control(term=term)

    # 玩家位置锁
    # 确保玩家位置和游戏状态在渲染和输入操作中不会冲突
    player_lock = threading.Lock()

    running = True  # 游戏运行状态
    time_running = True  # 游戏时间流动

    # 时间推进线程
    def time_loop():
        """后台线程，每秒推进游戏时间1分钟"""
        nonlocal time_running
        while running:
            if time_running:
                with player_lock:
                    # 每秒游戏时间推进1分钟
                    game_time.tick(minutes=1)
            time.sleep(1)

    time_thread = threading.Thread(target=time_loop, daemon=True)
    time_thread.start()

    # 输入处理线程
    def input_loop():
        """后台线程，监听键盘输入并执行动作"""
        nonlocal running, time_running
        while running:
            # 获取键盘动作 (key, action)
            item = control.get_action()
            if not item:
                time.sleep(0.01)
                continue

            key, action = item

            if action:
                with player_lock:
                    if action[0] == "move":
                        # 移动
                        dx, dy = action[1], action[2]
                        player.move(dx, dy, world)
                    elif action[0] == "save":
                        # 保存
                        save_data.player = {"x": player.x, "y": player.y}
                        save_data.world = world.name
                        save_data.time = game_time.to_dict()
                        save_data.save(SAVE_PATH)
                    elif action[0] == "quit":
                        # 退出
                        running = False
                    elif action[0] == "pause":
                        # 暂停
                        time_running = not time_running

    input_thread = threading.Thread(target=input_loop, daemon=True)
    input_thread.start()

    # 主渲染循环
    try:
        # 使用上下文管理器进入全屏模式并隐藏光标
        with term.fullscreen(), term.hidden_cursor():
            # 计算每帧的时间间隔（秒）
            frame_time = 1.0 / fps

            # 准备调试信息列表
            debug_info = "Welcome to the world!"
            while running:
                # 记录帧开始时间
                start_time = time.time()
                # 渲染和玩家状态同步
                with player_lock:

                    # 如果有新的游戏日，加入 debug 信息
                    if game_time.debug_message:
                        debug_info = game_time.debug_message
                        game_time.debug_message = ""  # 加入后清空

                    renderer.draw(
                        world,  # 当前地图
                        player,  # 玩家对象
                        game_time,  # 游戏时间
                        debug_info,  # 调试信息显示
                    )

                # 计算渲染耗时
                elapsed = time.time() - start_time
                # 计算剩余休眠时间，保证帧率接近 fps
                sleep_time = max(0, frame_time - elapsed)
                # 等待剩余时间后进入下一帧
                time.sleep(sleep_time)
    finally:
        # 停止控制器线程
        control.stop()


if __name__ == "__main__":
    main()
