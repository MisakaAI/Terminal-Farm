# renderer/ascii_renderer.py
# ASCII 渲染器

from blessed import Terminal
from wcwidth import wcswidth


class AsciiRenderer:
    def __init__(self, term=None, view_w=0, view_h=20, color=True):
        """
        初始化 ASCII 渲染器
        :param term: blessed.Terminal 对象，用于终端控制
        :param view_w: 视口宽度，0 表示自动适配终端宽度
        :param view_h: 视口高度，0 表示自动适配终端高度
        :param color: 是否显示颜色
        """

        self.term = term if term else Terminal()
        self.view_w = view_w
        self.view_h = view_h
        self.color = color

        # 上一帧内容缓存 [(char, (r,g,b))] 用于双缓冲优化
        self.prev_buffer = []

    def draw(self, world, player, game_time=None, debug_info=None):
        """
        渲染游戏视口
        :param world: World 对象，提供地图数据
        :param player: Player 对象，提供玩家位置
        :param game_time: GameTime 对象，可选，用于显示游戏时间
        :param debug_info: 可选，显示调试信息
        """

        term = self.term

        # 自动调整视口大小
        view_w = self.view_w if self.view_w > 0 else term.width
        view_h = self.view_h if self.view_h > 0 else min(term.height - 10, world.height)

        # 防止意外为 0 的情况
        if view_w <= 0:
            view_w = term.width
        if view_h <= 0:
            view_h = (
                min(term.height - 10, world.height)
                if term.height < world.height
                else world.height
            )

        # 获取视口
        chars, colors = world.get_viewport(
            player.x, player.y, view_w, view_h, cursor_pos=(player.y, player.x)
        )

        # 获取实际视口尺寸（防止越界）
        actual_h = len(chars)
        actual_w = len(chars[0]) if actual_h > 0 else 0

        # 初始化 prev_buffer，如果大小不匹配则重建
        if len(self.prev_buffer) != actual_h or any(
            len(row) != actual_w for row in self.prev_buffer
        ):
            self.prev_buffer = [
                [("", (-1, -1, -1)) for _ in range(actual_w)] for _ in range(actual_h)
            ]

        # 清空首行内容
        print(term.move(0, 0) + term.clear_eol, end="")

        # 打印游戏时间
        if game_time:
            time_text = f"{game_time.get_date_text()} ({game_time.get_week_text()}) {game_time.get_time_text()}"
            right_x = max(0, term.width - wcswidth(time_text) - 1)
            print(term.move(0, right_x) + time_text, end="")

        # 双缓冲渲染
        # 遍历每个格子，只刷新有变化的部分
        start_y = 2  # 第2行开始
        for y in range(actual_h):
            row_changes = []
            x = 0
            while x < actual_w:
                start_x = x
                # 找连续变化区
                while x < actual_w and self.prev_buffer[y][x] != (
                    chars[y][x],
                    colors[y][x],
                ):
                    x += 1
                end_x = x

                if start_x < end_x:
                    # 有变化区
                    segment = ""
                    for i in range(start_x, end_x):
                        char = chars[y][i]
                        r, g, b = colors[y][i]
                        if self.color and r != -1:
                            segment += term.color_rgb(r, g, b)(char)
                        else:
                            segment += char
                    row_changes.append((start_x, segment))
                    for i in range(start_x, end_x):
                        self.prev_buffer[y][i] = (chars[y][i], colors[y][i])
                else:
                    # 没变化则跳过
                    x += 1

            # 合并输出一次
            if row_changes:
                out = []
                for start_x, seg in row_changes:
                    out.append(term.move(start_y + y, start_x) + seg)
                print("".join(out), end="")

        # 打印调试信息
        info_y = start_y + actual_h + 1
        if debug_info:
            # 清空该行再打印
            print(term.move(info_y, 0) + " " * term.width, end="")
            print(term.move(info_y, 0) + debug_info)
            info_y += 1

        # 底部提示
        print(
            term.move(info_y, 0) + term.clear_eol + "Ctrl+W 保存 / Ctrl+X 退出",
            end="",
        )
