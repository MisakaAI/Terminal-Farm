# renderer/ascii_renderer.py
from blessed import Terminal


class AsciiRenderer:
    def __init__(self, term=None, view_w=50, view_h=20):
        # 支持外部传入 Terminal，或自己创建
        self.term = term or Terminal()
        self.view_w = int(view_w)
        self.view_h = int(view_h)

    def draw(self, world, player, debug_lines=None):
        """
        使用 World 数据渲染地图。
        world: core.world.World
        player: core.player.Player
        debug_lines: 可选 list[str]
        """

        # 清屏并回到 home
        print(self.term.home + self.term.clear, end="")

        # 获取视口内容
        lines, left, top = world.get_viewport(
            player.x, player.y, self.view_w, self.view_h
        )

        # 在视口中替换玩家字符（在适当位置）
        px_in_view = player.x - left
        py_in_view = player.y - top

        # 替换玩家字符
        if 0 <= py_in_view < len(lines) and 0 <= px_in_view < len(lines[0]):
            row = lines[py_in_view]
            lines[py_in_view] = (
                row[:px_in_view] + self.term.red("@") + row[px_in_view + 1 :]
            )

        # 打印标题
        print(f"地图: {world.name} ({world.width}x{world.height})  玩家位置: ({player.x},{player.y})")

        # 打印视口
        for line in lines:
            print(line)

        # 打印 debug 信息
        if debug_lines:
            print()
            for msg in debug_lines:
                print(self.term.yellow(msg))

        # 底部提示
        print("\n↑↓←→ 移动, S 保存, Q 退出")
