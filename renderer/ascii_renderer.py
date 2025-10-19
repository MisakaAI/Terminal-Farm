# renderer/ascii_renderer.py
from blessed import Terminal

class AsciiRenderer:
    def __init__(self, term=None, view_w=50, view_h=20):
        # 支持外部传入 Terminal，或自己创建
        self.term = term if term is not None else Terminal()
        self.view_w = int(view_w)
        self.view_h = int(view_h)

    def draw(self, world, player, debug_lines=None):
        """
        world: World 实例
        player: Player 实例
        debug_lines: 可选 list[str] ，会在底部逐行打印
        """
        # 清屏并回到 home（替代缓冲区请在外层 with term.fullscreen()）
        print(self.term.home + self.term.clear, end="")

        # 获取视口内容
        lines, left, top = world.get_viewport(player.x, player.y, self.view_w, self.view_h)

        # 在视口中替换玩家字符（在适当位置）
        px_in_view = player.x - left
        py_in_view = player.y - top
        if 0 <= py_in_view < len(lines) and 0 <= px_in_view < len(lines[0]):
            row = lines[py_in_view]
            # replace char at px_in_view with '@'
            lines[py_in_view] = row[:px_in_view] + "@" + row[px_in_view+1:]

        # 打印视口（先打印一个标题行，便于观察）
        print(f"Map view ({world.width}x{world.height}), center @ ({player.x},{player.y})")
        for line in lines:
            print(line)

        # 打印 debug 区（如果有）
        if debug_lines:
            print()  # 空行分隔
            for dl in debug_lines:
                print(dl)

        # 底部提示
        print("\nUse arrow keys to move, S to save, Q to quit.")
