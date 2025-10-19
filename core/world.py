# core/world.py
import numpy as np

"""
[地图系统]
每个场景地图是 独立的 numpy 文件 (.npy)，存储整个地图数据。
地图文件路径可自定义，加载时通过 World(map_path) 指定。
如果指定地图文件不存在，则抛出 FileNotFoundError。
在存档中记录玩家位置 (x, y) 和地图名称。

[数据结构]
每个地图是一个 三维 numpy 数组 (height, width, 6)，每个格子包含如下信息：

索引    内容        类型     说明
0      字符        str      显示字符，如 " " 或 "#"
1      是否可通行   int      0=不可通行，1=可通行
2      地形类型    int       1=路面，2=田地，后续可扩展
3      R          int       颜色值 0-255，-1 表示透明
4      G          int       颜色值 0-255，-1 表示透明
5      B          int       颜色值 0-255，-1 表示透明
"""

class World:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.name = ""
        self.tiles = None

    def is_walkable(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_viewport(self, center_x, center_y, view_w, view_h):
        """
        返回 viewport 字符列表（每行字符串），以 (center_x,center_y) 为中心。
        当玩家靠近边界时，视口贴边。
        """
        half_w = view_w // 2
        half_h = view_h // 2

        left = center_x - half_w
        top = center_y - half_h

        # clamp to world bounds
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        if left + view_w > self.width:
            left = max(0, self.width - view_w)
        if top + view_h > self.height:
            top = max(0, self.height - view_h)

        lines = []
        for y in range(top, top + view_h):
            # join slice for speed
            lines.append("".join(self.tiles[y][left:left + view_w]))
        return lines, left, top
