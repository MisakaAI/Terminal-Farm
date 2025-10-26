# core/save.py
# 存档管理模块
# 提供游戏存档的加载、保存及访问接口

import json
from pathlib import Path


class SaveData:
    # 默认存档数据
    DEFAULT_SAVE = {
        "world": "pasture",
        "player": {"x": 10, "y": 10},
        "time": {"time": 1, "day": 1, "month": 0, "year": 1, "weekday": 0},
        "settings": {"language": "zh-CN", "fps": 30},
    }

    def __init__(self, data=None):
        """初始化存档数据"""
        self.data = data if data else self.DEFAULT_SAVE.copy()

    @classmethod
    def load(cls, path: str | Path):
        """
        从文件加载存档，如果文件不存在或 JSON 解析错误，使用默认存档
        :param path: 存档文件路径
        :return: SaveData 实例
        """
        path = Path(path)
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    return cls(data)
            except json.JSONDecodeError:
                # 文件损坏，使用默认
                return cls()
        else:
            # 文件不存在，创建默认
            save = cls()
            save.save(path)
            return save

    def save(self, path: str | Path):
        """
        保存存档到指定文件
        :param path: 存档文件路径
        """
        path = Path(path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # 方便访问存档数据的属性
    @property
    def player(self):
        """玩家数据，返回字典 {'x': int, 'y': int}"""
        return self.data.get("player", {"x": 10, "y": 10})

    @player.setter
    def player(self, value):
        """设置玩家数据"""
        self.data["player"] = value

    @property
    def world(self):
        """地图名称，如果存档里没有则返回默认地图 'pasture'"""
        return self.data.get("world") or "pasture"

    @world.setter
    def world(self, value):
        """设置地图名称"""
        self.data["world"] = value

    @property
    def settings(self):
        """游戏设置，例如语言等"""
        return self.data.get("settings", {"language": "zh-CN", "fps": 30})

    @settings.setter
    def settings(self, value):
        """修改游戏设置"""
        self.data["settings"] = value

    @property
    def time(self):
        """游戏时间数据，返回字典 {'time', 'day', 'month', 'year', 'weekday'}"""
        return self.data.get("time", self.DEFAULT_SAVE["time"])

    @time.setter
    def time(self, value):
        """设置游戏时间数据"""
        self.data["time"] = value
