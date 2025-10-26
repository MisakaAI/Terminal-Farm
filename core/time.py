# core/player.py
# 时间日期

class GameTime:
    """
    游戏时间管理类
    用于记录游戏中的分钟、日、月、年、星期，并提供文本显示方法。
    """

    def __init__(self, save_data=None, translator=None):
        """
        初始化游戏时间
        :param save_data: dict 或 None，包含已有时间数据
        :param translator: Translator 对象，用于文本显示和本地化
        """
        self.translator = translator
        self.time = 0 if save_data is None else save_data.get("time", 0)
        self.day = 1 if save_data is None else save_data.get("day", 1)
        self.month = 0 if save_data is None else save_data.get("month", 0)
        self.year = 1 if save_data is None else save_data.get("year", 1)
        self.weekday = 0 if save_data is None else save_data.get("weekday", 0)
        self.debug_message = ""  # 用于显示调试信息

    def tick(self, minutes=1):
        """
        推进游戏时间
        :param minutes: int，每次推进的分钟数
        """
        previous_time = self.time
        self.time += minutes

        # 先判断是否跨过午夜 AM 0:00 / 1080
        if previous_time < 1080 <= self.time:
            self.new_day()

        # 再判断是否正式跨天 AM 6:00 / 1440
        elif self.time >= 1440:
            self.time %= 1440
            self.next_day()

    def new_day(self):
        """
        处理新的一天逻辑
        """
        # 日期
        self.day += 1
        # 星期
        self.weekday = (self.weekday + 1) % 7
        # 日期超过30，为下个月1日
        if self.day > 30:
            self.day = 1
            # 月份
            self.month = (self.month + 1) % 4
            # 如果月份超过冬天，为新一年春天
            if self.month == 0:
                self.year += 1

    def next_day(self):
        """
        新的一天发生时触发的事件
        """
        self.debug_message = "新的一天"

    def get_time_text(self):
        """
        获取游戏时间文本
        - AM/PM 制式
        - 小时：分钟格式
        :return: str，例如 "AM 6:00"
        """

        # 游戏时间从 AM 6:00 开始，所以加 360 分钟偏移
        total_minutes = (self.time + 360) % 1440
        hour = total_minutes // 60
        minute = total_minutes % 60

        # AM / PM
        am_pm = "AM" if hour < 12 else "PM"

        # 将小时转换为 0-11
        display_hour = hour % 12

        return f"{am_pm} {display_hour}:{minute:02d}"

    def get_date_text(self):
        """
        获取游戏日期文本
        使用 Translator 翻译季节和日数
        :return: str，例如 "冬 1日"
        """

        # 获取季节数组
        seasons = self.translator.get_list("time", "seasons") or [
            "春",
            "夏",
            "秋",
            "冬",
        ]
        season_name = seasons[self.month]

        # 使用 day 模板
        day_template = self.translator.t(
            "time", "day", season=season_name, day=self.day
        )
        return day_template

    def get_week_text(self):
        """
        获取星期文本
        :return: str，例如 "一"
        """
        weekdays = self.translator.get_list("time", "weekdays") or [
            "一",
            "二",
            "三",
            "四",
            "五",
            "六",
            "日",
        ]
        week_name = weekdays[self.weekday]
        return week_name

    def to_dict(self):
        """
        转为存档字典
        :return: dict，包含 time/day/month/year/weekday
        """
        return {
            "time": self.time,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "weekday": self.weekday,
        }
