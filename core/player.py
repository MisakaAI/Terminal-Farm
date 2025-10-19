# core/player.py


class Player:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if world.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
