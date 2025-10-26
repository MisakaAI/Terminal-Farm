# core/world.py
# 世界地图

import numpy as np
from pathlib import Path

"""
[地图系统]
每个场景地图是 独立的 numpy 文件 (.npy)，存储整个地图数据。
地图文件路径可自定义，加载时通过 World(map_path) 指定。
如果指定地图文件不存在，则抛出 FileNotFoundError。
在存档中记录玩家位置 (x, y) 和地图名称。

[数据结构]
每个地图是一个 三维 numpy 数组 (height, width, 6)，每个格子包含如下信息：

索引    内容        类型     说明
0      字符        int      字符，存为 Unicode 整数
1      是否可通行   int      0=不可通行，1=可通行
2      地形类型    int       1=路面，2=田地，后续可扩展
3      R          int       颜色值 0-255，-1 表示透明
4      G          int       颜色值 0-255，-1 表示透明
5      B          int       颜色值 0-255，-1 表示透明
"""


class World:
    """
    地图系统
    - 加载 .npy 地图文件
    - 提供坐标访问与区域切片
    - 支持基于中心点的视口渲染（带颜色）
    """

    def __init__(self, map_path: str):
        """初始化地图"""
        f = Path(map_path)
        if not f.exists():
            raise FileNotFoundError(f"地图文件不存在: {f}")

        # 加载 numpy 地图文件
        self.tiles = np.load(f, allow_pickle=True)

        # 地图尺寸（高、宽）
        self.height, self.width = self.tiles.shape[:2]

        # 地图名称（不含扩展名）
        self.name = f.stem

    def is_walkable(self, x: int, y: int) -> bool:
        """判断坐标是否可通行"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return bool(self.tiles[y, x, 1])
        return False

    def get_tile(self, x: int, y: int):
        """获取单个格子数据"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        return self.tiles[y, x]

    def get_zone(self, start, end):
        """获取矩形区域对应的 numpy 切片"""
        y1, x1 = start
        y2, x2 = end
        ys = slice(min(y1, y2), max(y1, y2) + 1)
        xs = slice(min(x1, x2), max(x1, x2) + 1)
        return ys, xs

    def get_viewport(
        self, center_x: int, center_y: int, view_w: int, view_h: int, cursor_pos=None
    ):
        """
        获取以 (center_x, center_y) 为中心的地图视口（可显示在屏幕上）

        :param center_x: 中心 X 坐标
        :param center_y: 中心 Y 坐标
        :param view_w: 视口宽度（终端显示宽度）
        :param view_h: 视口高度（终端显示高度）
        :param cursor_pos: 可选，玩家位置 (y, x)，用于绘制 "@"
        :return:
            view_chars: list[list[str]] —— 字符矩阵
            view_colors: list[list[tuple]] —— 每格颜色 (R,G,B)
            left, top: 视口左上角地图坐标
        """

        # 限制视口范围不超过地图尺寸
        view_w = min(view_w, self.width)
        view_h = min(view_h, self.height)

        # 保证中心点在地图范围内
        center_x = max(0, min(center_x, self.width - 1))
        center_y = max(0, min(center_y, self.height - 1))

        # 计算视口边界
        half_w = view_w // 2
        half_h = view_h // 2

        left = max(0, min(self.width - view_w, center_x - half_w))
        top = max(0, min(self.height - view_h, center_y - half_h))
        right = min(left + view_w, self.width)
        bottom = min(top + view_h, self.height)

        view_chars = []
        view_colors = []

        # 遍历视口范围
        for y in range(top, bottom):
            row_chars = []
            row_colors = []
            for x in range(left, right):
                # 将字符的 Unicode 数值转换为字符
                c = chr(self.tiles[y, x, 0])
                r, g, b = self.tiles[y, x, 3:6]
                if cursor_pos and (y, x) == cursor_pos:
                    c = "@"  # 玩家光标标记
                    r, g, b = 255, 0, 0
                row_chars.append(c)
                row_colors.append((r, g, b))
            view_chars.append(row_chars)
            view_colors.append(row_colors)

        return view_chars, view_colors
