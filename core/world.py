# core/world.py
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
0      字符        str      显示字符，如 " " 或 "#"
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
    - 提供基本的读取与视口（viewport）功能
    """

    def __init__(self, map_path: str):
        f = Path(map_path)
        if not f.exists():
            raise FileNotFoundError(f"地图文件不存在: {f}")

        self.tiles = np.load(f, allow_pickle=True)
        self.height, self.width = self.tiles.shape[:2]
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

    def get_viewport(self, center_x: int, center_y: int, view_w: int, view_h: int):
        """
        获取以 (center_x, center_y) 为中心的地图视口数据。

        返回：
            lines: list[str] —— 每行的字符拼接成字符串
            left, top: int —— 视口左上角在地图中的坐标
        """
        half_w = view_w // 2
        half_h = view_h // 2

        left = max(0, min(self.width - view_w, center_x - half_w))
        top = max(0, min(self.height - view_h, center_y - half_h))

        lines = []
        for y in range(top, top + view_h):
            chars = self.tiles[y, left : left + view_w, 0]
            lines.append("".join(chars))
        return lines, left, top
