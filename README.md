# Terminal-Farm

A farm running on a terminal
一个运行在终端中的农场

## 项目结构

```csharp
 ├── core/
 │    ├── player.py         # 玩家移动与交互
 │    ├── map.py            # 地图与世界逻辑
 │    ├── time.py           # 时间流逝、天数控制
 │    ├── save.py           # 存档
 │    ├── setting.py        # 设置
 │    └── __init__.py
 │
 ├── renderer/
 │    ├── ascii_renderer.py # blessed 渲染器
 │    ├── interface.py      # 抽象渲染接口 (SDL 可替换)
 │    └── __init__.py
 │
 ├── translation/
 │    ├── world.json
 │    ├── tile.json
 │    ├── crop.json
 │    ├── player.json
 │    ├── time_manager.json
 │    └── translation.json
 │
 ├── main.py                # 游戏主循环入口
 └── requirements.txt
```

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
