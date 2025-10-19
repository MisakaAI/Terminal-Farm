import json
from pathlib import Path

class Translator:
    def __init__(self, lang="zh-CN"):
        self.lang = lang
        self.translations = {}
        self.load_translation_files()

    def load_translation_files(self):
        """自动加载 translation 目录下的所有 .json 文件"""
        translation_dir = Path("translation")
        if not translation_dir.exists():
            print("翻译文件目录不存在")
            return

        for json_file in translation_dir.glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    key = json_file.stem  # 文件名（不含扩展名）
                    self.translations[key] = data
            except json.JSONDecodeError:
                print(f"无法解析 {json_file.name}，不是有效的 JSON")

        time_path = Path("translation/time.json")
        if time_path.exists():
            self.translations["time"] = json.loads(time_path.read_text(encoding="utf-8"))
        else:
            self.translations["time"] = {}

        # 加载 setting.json
        setting_path = Path("translation/setting.json")
        if setting_path.exists():
            self.translations["setting"] = json.loads(setting_path.read_text(encoding="utf-8"))
        else:
            self.translations["setting"] = {}

    def get_list(self, category, key):
        """获取数组类型的翻译，例如 seasons 或 weekdays"""
        return self.translations.get(category, {}).get(self.lang, {}).get(key, [])

    def t(self, category, key, **kwargs):
        """
        category: "time_manager" 或 "setting"
        key: day / label 等
        """
        template = self.translations.get(category, {}).get(self.lang, {}).get(key, "")
        return template.format(**kwargs) if template else f"{key}: {kwargs}"
