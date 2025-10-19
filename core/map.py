# core/world.py
class World:
    def __init__(self, width=1000, height=1000, fill_char="."):
        self.width = int(width)
        self.height = int(height)
        # 简单实现：全部填充 '.'（占用约 1M 字符，通常可接受）
        self._fill = fill_char
        self.tiles = [[self._fill for _ in range(self.width)] for _ in range(self.height)]

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
