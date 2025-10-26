# Terminal-Farm

A farm running on a terminal
一个运行在终端中的农场

## 项目结构

```txt
 ├── core/
 │    ├── player.py         # 玩家
 │    ├── world.py          # 世界地图
 │    ├── map_edit.py       @ 地图编辑器
 │    ├── time.py           # 时间日期
 │    ├── save.py           # 存档
 │    ├── setting.py        @ 设置
 │    └── __init__.py
 │
 ├── renderer/
 │    ├── ascii_renderer.py # blessed 渲染器
 │    ├── interface.py      # 抽象渲染接口 (SDL 可替换)
 │    └── __init__.py
 │
 ├── translation/
 │    ├── *.json            # 翻译文件
 │    ├── translator.py     # 翻译
 │    └── __init__.py
 │
 ├── map/
 │    └── *.npy             # 地图文件
 │
 ├── main.py                # 游戏主循环入口
 └── requirements.txt
```

使用 `@` 注释的，为独立运行组件。
例如：使用 `python core/map_edit.py` 打开地图编辑器。

## Install && Depend

```sh
python3 -m venv .venv
pip install -r requirements.txt
source .venv/bin/activate
python3 main.py
```

- [Python](https://www.python.org/)
- [numpy](https://numpy.org/)
- [blessed](https://github.com/jquast/blessed)
