# core/player.py
# 玩家类


class Player:
    def __init__(self, x=0, y=0):
        """
        初始化玩家对象
        :param x: 玩家初始横坐标，默认 0
        :param y: 玩家初始纵坐标，默认 0
        """
        self.x = int(x)  # 玩家当前横坐标（整数）
        self.y = int(y)  # 玩家当前纵坐标（整数）

    def move(self, dx, dy, world):
        """
        移动玩家
        :param dx: 横向移动量（正数向右，负数向左）
        :param dy: 纵向移动量（正数向下，负数向上）
        :param world: World 对象，用于判断目标位置是否可通行
        :return: bool，如果移动成功返回 True，否则返回 False
        """
        new_x = self.x + dx
        new_y = self.y + dy

        # 判断新位置是否可通行
        if world.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True

        # 不可通行时不移动
        return False
