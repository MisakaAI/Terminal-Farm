# core/control.py
# 控制器

import queue
import threading
from blessed import Terminal


class Control:
    """
    控制器（非堵塞式）
    支持：
    - 方向键移动
    - P 暂停/恢复
    - Ctrl+W 保存
    - Ctrl+X 退出
    """

    # 定义方向键对应的移动向量 (dx, dy)
    MOVE_KEYS = {
        "KEY_UP": (0, -1),
        "KEY_DOWN": (0, 1),
        "KEY_LEFT": (-1, 0),
        "KEY_RIGHT": (1, 0),
    }

    # 定义 Ctrl 快捷键
    CTRL_KEYS = {
        "\x17": "save",  # Ctrl+W
        "\x18": "quit",  # Ctrl+X
    }

    # 初始化控制器
    def __init__(self, term=None):
        self.term = term if term else Terminal()
        # 存储动作的队列
        self.action_queue = queue.Queue()
        # 控制输入线程是否运行
        self.running = True
        # 启动输入线程（守护线程，程序退出时自动结束）
        self.thread = threading.Thread(target=self._input_loop, daemon=True)
        self.thread.start()

    def _input_loop(self):
        """
        输入线程主循环（非阻塞）
        - 使用 blessed 的 cbreak 模式读取按键
        - 将检测到的动作放入队列
        """
        with self.term.cbreak(), self.term.hidden_cursor():
            while self.running:
                # 非阻塞读取键盘输入，超时 0.05 秒
                key = self.term.inkey(timeout=0.05)
                if not key:
                    # 没有输入则继续循环
                    continue

                # 初始化动作为空
                action = None

                # 方向键
                if key.name in self.MOVE_KEYS:
                    dx, dy = self.MOVE_KEYS[key.name]
                    action = ("move", dx, dy)

                # Ctrl 快捷键
                elif key in self.CTRL_KEYS:
                    action = (self.CTRL_KEYS[key],)

                # P 暂停/恢复时间
                elif key.upper() == "P":
                    action = ("pause",)

                # 将动作放入队列（可能为空）
                self.action_queue.put((key, action))

    def get_action(self):
        """
        获取队列中的最新动作
        :return: tuple 动作信息，例如 ("move", 1, 0) 或 ("save",)，没有动作返回 None
        """
        try:
            return self.action_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """
        停止输入线程
        """
        self.running = False
        self.thread.join()  # 等待线程退出


if __name__ == "__main__":
    term = Terminal()
    control = Control(term)
    print(term.clear)
    print("按键测试（Ctrl+X 退出）：")

    KEY_SEQ_MAP = {
        "\x1b[A": "UP",
        "\x1b[B": "DOWN",
        "\x1b[C": "RIGHT",
        "\x1b[D": "LEFT",
        "\x17": "Ctrl+W",
        "\x18": "Ctrl+X",
    }

    try:
        with term.cbreak(), term.hidden_cursor():
            while True:
                key, action = None, None
                # 阻塞直到有按键
                item = control.action_queue.get()
                if item:
                    key, action = item

                # 获取按键名
                key_name = KEY_SEQ_MAP.get(
                    str(key), key.upper() if len(key) == 1 else "UNKNOWN"
                )

                # 构造显示内容
                display = f"按下键: {key_name}"
                if action:
                    display += f", 对应动作: {action}"

                # 实时刷新显示，不换行
                print(term.move_xy(0, 2) + term.clear_eol + display, end="", flush=True)

                # Ctrl+X退出
                if action and action[0] == "quit":
                    break

    finally:
        control.stop()
        print(term.move_down + "\n测试结束。")
