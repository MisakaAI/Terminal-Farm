import numpy as np
from pathlib import Path
from blessed import Terminal


class Map:
    def __init__(self):
        self.tiles = None
        self.name = ""
        self.width = 0
        self.height = 0

    def init_map(self, width: int, height: int, name: str):
        """初始化地图"""
        self.width = width
        self.height = height
        self.name = name
        self.tiles = np.empty((height, width, 6), dtype=object)

        self.tiles[:, :, 0] = " "  # 字符
        self.tiles[:, :, 1] = 1  # 可通行
        self.tiles[:, :, 2] = 1  # 地形
        self.tiles[:, :, 3:6] = -1  # 颜色

        # 设置地图边缘和对应值
        edges = [(0, "#"), (1, 0), (3, 150), (4, 150), (5, 150)]
        for channel, value in edges:
            self.tiles[0, :, channel] = value
            self.tiles[-1, :, channel] = value
            self.tiles[:, 0, channel] = value
            self.tiles[:, -1, channel] = value

        print(f"地图 {self.name} 初始化完成")

    def save_map(self, path: str):
        """保存地图"""
        f = Path(path)
        f.parent.mkdir(parents=True, exist_ok=True)  # 创建目录
        np.save(f, self.tiles)
        print(f"地图已保存到 {f}")

    def load_map(self, path: str):
        """加载地图"""
        f = Path(path)
        if not f.exists():
            raise FileNotFoundError(f"地图文件不存在: {f}")
        self.tiles = np.load(f, allow_pickle=True)
        self.height, self.width = self.tiles.shape[:2]
        self.name = f.stem
        print(f"地图 {self.name} 已加载")

    def show_help(self, term):
        """显示帮助菜单"""
        help_text = [
            "终端地图编辑器操作说明",
            "",
            "方向键  ↑ ↓ ← → ：移动光标",
            "Space ：选择区域起点 / 终点",
            "Backspace ：清除区域选择",
            "C ：修改字符",
            "R ：修改颜色 (RGB, 例: 255 128 0)",
            "T ：修改地形类型 (int)",
            "P ：切换通行状态",
            "S ：保存地图",
            "/ ：跳转到坐标 (x y)",
            "Q ：退出编辑器",
            "",
            "按任意键返回编辑界面...",
        ]
        print(term.home + term.clear)
        for line in help_text:
            print(term.green(line))
        term.inkey()  # 等待任意键继续

    def blocking_input(
        self, term, prompt: str, default: str = "", maxlen: int = 50
    ) -> str | None:
        """阻塞式终端输入函数"""

        buffer = default
        print(
            term.move(term.height - 1, 0) + term.clear_eol + f"{prompt}{buffer}",
            end="",
            flush=True,
        )

        try:
            with term.hidden_cursor():
                while True:
                    key = term.inkey()
                    if not key:
                        continue

                    # 回车确认
                    if key.name == "KEY_ENTER":
                        val = buffer.strip()
                        return val if val else (default.strip() if default else None)

                    # 取消输入
                    elif key.name == "KEY_ESCAPE":
                        print(
                            term.move(term.height - 1, 0) + term.clear_eol,
                            end="",
                            flush=True,
                        )
                        return None

                    # 删除
                    elif key.name == "KEY_BACKSPACE":
                        buffer = buffer[:-1]

                    # 普通字符
                    elif len(buffer) < maxlen and key.is_sequence is False:
                        buffer += key

                    # 刷新显示
                    print(
                        term.move(term.height - 1, 0)
                        + term.clear_eol
                        + f"{prompt}{buffer}",
                        end="",
                        flush=True,
                    )
        finally:
            print(term.normal_cursor, end="")

    def get_zone(self, region_start, region_end):
        """计算矩形区域范围"""
        y1, x1 = region_start
        y2, x2 = region_end
        ys = slice(min(y1, y2), max(y1, y2) + 1)
        xs = slice(min(x1, x2), max(x1, x2) + 1)
        return ys, xs

    def draw_viewport(
        self,
        term,
        cursor_x=0,
        cursor_y=0,
        view_w=50,
        view_h=20,
        color=True,
        region_start=False,
        region_end=False,
    ):
        """绘制终端视口 (支持彩色显示)

        参数:
            term: blessed.Terminal 实例
            cursor_x, cursor_y: 光标位置
            view_w, view_h: 视口宽高
            color: 是否渲染 RGB 颜色
            region_start,region_end: 标定位置
        """
        print(term.home + term.clear, end="")
        print(f"地图大小: ({self.tiles.shape[1]},{self.tiles.shape[0]})", end="")
        print(f"{' '*5}视口范围: {view_w}x{view_h}\n")

        # 计算视口左上角
        half_w = view_w // 2
        half_h = view_h // 2
        left = max(0, min(self.width - view_w, cursor_x - half_w))
        top = max(0, min(self.height - view_h, cursor_y - half_h))

        # 一次性裁剪出视口区域
        view = self.tiles[top : top + view_h, left : left + view_w]
        view_chars = view[:, :, 0].astype(str)
        view_colors = view[:, :, 3:6].astype(int)

        for y in range(view_chars.shape[0]):
            row_str = ""
            for x in range(view_chars.shape[1]):
                char = view_chars[y, x]
                # 显示光标位置 @
                if top + y == cursor_y and left + x == cursor_x:
                    char = term.red + "@"
                # 显示彩色
                elif color:
                    r, g, b = view_colors[y, x]
                    if r != -1 and g != -1 and b != -1:
                        char = term.color_rgb(r, g, b)(char)
                row_str += char
            print(row_str)

        # 显示光标所在格信息
        tile = self.tiles[cursor_y, cursor_x]
        C, P, T = tile[0], tile[1], tile[2]
        R, G, B = tile[3], tile[4], tile[5]

        print(f"\n位置: ({cursor_x}, {cursor_y})")
        print(f"字符: [{C}] ({R},{G},{B}) ", end="")
        if color:
            print(term.on_color_rgb(R, G, B)("  "))
        print(f"选择点: [{region_start} {region_end}]" + " " * 5)
        print(f"可通行: {bool(P)}" + " " * 5)
        print(f"地形类型: {T}" + " " * 5)

    def run_editor(self, path, start_x=0, start_y=0, view_w=50, view_h=20, color=True):
        term = Terminal()
        cursor_x, cursor_y = start_x, start_y

        if view_w <= 0 or view_h <= 0:
            view_w = term.width  # 终端列数（宽度）
            if term.height >= self.height:
                view_h = self.height  # 地图高度
            else:
                view_h = term.height - 10  # 终端行数（高度）

        # 区域选择坐标，初始为 None
        region_start = None
        region_end = None

        col = max(0, term.width - len(path))  # 文件路径显示列

        def refresh_view():
            # 刷新视口
            self.draw_viewport(
                term,
                cursor_x,
                cursor_y,
                view_w,
                view_h,
                color,
                region_start,
                region_end,
            )

            # 底部提示行
            print(
                term.move(term.height - 2, 0)
                + term.clear_eol
                + term.yellow("[Q]退出; [S]保存; [H]帮助;"),
                end="",
                flush=True,
            )

            # 显示文件路径
            print(term.move(term.height - 1, col - 2) + term.clear_eol + f"[{path}]", end="", flush=True)

        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            # 绘制视口
            refresh_view()
            while True:
                key = term.inkey()
                if not key:
                    continue

                # 启动坐标输入模式
                if key == "/":
                    coord = self.blocking_input(term, "跳转到坐标 (x y): ")
                    if coord:
                        try:
                            x, y = map(int, coord.split())
                            cursor_x = min(max(x, 0), self.width - 1)
                            cursor_y = min(max(y, 0), self.height - 1)
                        except:
                            pass

                # 移动光标
                elif key.name == "KEY_UP":
                    cursor_y = max(0, cursor_y - 1)
                elif key.name == "KEY_DOWN":
                    cursor_y = min(self.height - 1, cursor_y + 1)
                elif key.name == "KEY_LEFT":
                    cursor_x = max(0, cursor_x - 1)
                elif key.name == "KEY_RIGHT":
                    cursor_x = min(self.width - 1, cursor_x + 1)

                # 记录区域坐标
                elif key == " " or key.name == "KEY_SPACE":
                    if region_start is None:
                        region_start = (cursor_y, cursor_x)
                    elif region_end is None:
                        region_end = (cursor_y, cursor_x)
                    else:
                        # 第三次以后只更新第二个点
                        region_end = (cursor_y, cursor_x)

                # 清空区域坐标
                elif key.name == "KEY_BACKSPACE":
                    region_start = region_end = None

                # 修改字符
                elif key.upper() == "C":
                    print(
                        term.move(term.height - 1, 0) + "输入新字符: ",
                        end="",
                        flush=True,
                    )
                    char = term.inkey(timeout=None)
                    if char:
                        if region_start and region_end:
                            ys, xs = self.get_zone(region_start, region_end)
                            self.tiles[ys, xs, 0] = char  # 批量修改
                        else:
                            # 单格修改
                            self.tiles[cursor_y, cursor_x, 0] = char

                # 修改颜色
                elif key.upper() == "R":
                    v = self.blocking_input(
                        term, "输入颜色 RGB: "
                    )
                    if v is None or not v.strip():
                        r, g, b = -1, -1, -1
                    else:
                        try:
                            parts = [int(p) for p in v.replace(",", " ").split()]
                            r, g, b = parts if len(parts) == 3 else (-1, -1, -1)
                        except:
                            r, g, b = -1, -1, -1

                    # 批量修改区域或单格
                    if region_start and region_end:
                        ys, xs = self.get_zone(region_start, region_end)
                        self.tiles[ys, xs, 3:6] = [r, g, b]
                    else:
                        self.tiles[cursor_y, cursor_x, 3:6] = [r, g, b]

                # 切换通行状态
                elif key.upper() == "P":
                    if region_start and region_end:
                        ys, xs = self.get_zone(region_start, region_end)
                        self.tiles[ys, xs, 1] ^= 1
                    else:
                        self.tiles[cursor_y, cursor_x, 1] ^= 1

                # 修改地形
                elif key.upper() == "T":
                    t = self.blocking_input(term, "输入地形类型(int): ")
                    if t and t.isdigit():
                        if region_start and region_end:
                            ys, xs = self.get_zone(region_start, region_end)
                            self.tiles[ys, xs, 2] = int(t)
                        else:
                            self.tiles[cursor_y, cursor_x, 2] = int(t)

                # 显示帮助菜单
                elif key.upper() == "H":
                    self.show_help(term)

                # 保存
                elif key.upper() == "S":
                    self.save_map(path)

                # 退出
                elif key.upper() == "Q":
                    print(term.normal + term.clear, end="")
                    break

                # 刷新视口
                refresh_view()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="终端地图编辑器")
    parser.add_argument(
        "map_path", nargs="?", default="map/pasture.npy", help="地图文件路径"
    )
    parser.add_argument(
        "-W", "--width", type=int, default=100, help="地图宽度（仅当创建地图时有效）"
    )
    parser.add_argument(
        "-H", "--height", type=int, default=50, help="地图高度（仅当创建地图时有效）"
    )
    parser.add_argument("-v", "--view", type=str, default="0*0", help="视口宽高 50*20")
    parser.add_argument(
        "-p", "--position", type=str, default="1,1", help="初始光标位置 1,1"
    )
    parser.add_argument(
        "--no-color", action="store_false", dest="color", help="禁用彩色显示"
    )

    args = parser.parse_args()

    editor = Map()
    map_file = Path(args.map_path)

    # 解析 初始光标位置 & 视口宽高
    try:
        x, y = args.position.split(",")
        w, h = args.view.split("*")
    except:
        print("输入参数错误")

    # 地图文件是否存在
    if map_file.exists():
        editor.load_map(map_file)
    else:
        print(f"地图文件 {map_file} 不存在，将创建新地图 {args.width}x{args.height}")
        editor.init_map(width=args.width, height=args.height, name=map_file.stem)
        editor.save_map(map_file)

    editor.run_editor(
        path=args.map_path,
        start_x=int(x),
        start_y=int(y),
        view_w=int(w),
        view_h=int(h),
        color=args.color,
    )
