# core/player.py


class GameTime:
    def __init__(self, save_data=None, translator=None):
        self.translator = translator
        self.time = 0 if save_data is None else save_data.get("time", 0)
        self.day = 1 if save_data is None else save_data.get("day", 1)
        self.month = 0 if save_data is None else save_data.get("season", 0)
        self.year = 1 if save_data is None else save_data.get("year", 1)
        self.weekday = 0 if save_data is None else save_data.get("weekday", 0)
        self.debug_message = ""  # 存储新一天信息，用于debug显示

    def tick(self, minutes=1):

        previous_time = self.time
        self.time += minutes
        if self.time >= 1440:
            self.time %= 1440
            self.next_day()

        # 检查是否到达 AM 12:00（360 分钟），并且刚刚跨过
        if previous_time < 1080 <= self.time:
            self.new_day()

    def new_day(self):
        self.day += 1
        self.weekday = (self.weekday + 1) % 7
        if self.day > 30:
            self.day = 1
            self.month = (self.month + 1) % 4
            if self.month == 0:
                self.year += 1

    def next_day(self):
        self.debug_message = "新的一天"

    def get_time_text(self):
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
        return {
            "time": self.time,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "weekday": self.weekday,
        }
