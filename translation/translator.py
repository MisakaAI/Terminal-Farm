# translation/translator.py
# 翻译

import json
from pathlib import Path


class Translator:
    """
    翻译器
    - 自动加载 translation 目录下的 JSON 文件
    - 提供 get_list() 获取数组类型翻译
    - 提供 t() 获取字符串模板翻译并可格式化
    """

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

    def get_list(self, category, key):
        """
        获取数组类型的翻译
        :param category: JSON 文件分类
        :param key: 对应键
        :return: 数组，如果不存在返回空列表
        """
        return self.translations.get(category, {}).get(self.lang, {}).get(key, [])

    def t(self, category, key, **kwargs):
        """
        获取字符串类型翻译并可格式化
        :param category: JSON 文件分类
        :param key: 对应键
        :param kwargs: 用于格式化字符串的参数
        :return: 翻译后的字符串，找不到返回 key 和参数信息
        """
        template = self.translations.get(category, {}).get(self.lang, {}).get(key, "")
        return template.format(**kwargs) if template else f"{key}: {kwargs}"
