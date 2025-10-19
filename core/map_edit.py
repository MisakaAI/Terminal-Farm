from core.map import create_map, edit_map_region, save_map
from pathlib import Path
import numpy as np

MAP_FILE = Path("map/pasture.npy")

def init_map():
    """创建初始地图"""
    tiles = create_map(1000, 1000)
    edit_map_region(tiles, 50, 50, 100, 100, char=".", color=(0, 0, 255), tile_type=2)
    save_map(tiles, MAP_FILE)
    print("地图初始化完成")

def view_map_summary():
    """简单查看地图信息"""
    tiles = np.load(MAP_FILE, allow_pickle=True)
    print(f"地图大小: {tiles.shape}")
    print(f"样例字符: {np.unique(tiles[:, :, 0])}")

if __name__ == "__main__":
    if not MAP_FILE.exists():
        init_map()
    else:
        view_map_summary()
