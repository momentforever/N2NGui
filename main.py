import os
import sys

from src.common.custom_config import init_config
from src.common.custom_logging import init_logging
from src.tool.n2n import init_n2n_edge
from src.gui.gui import GUI

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # 返回打包后可执行文件的路径
        return os.path.realpath(sys.executable)
    else:
        # 返回原始脚本文件的路径
        return os.path.realpath(__file__)

if __name__ == '__main__':

    current_dir = os.path.dirname(get_executable_path())
    print(current_dir)
    # 初始化config
    config = init_config(current_dir)

    init_logging()

    n2n = init_n2n_edge()
    if config.IS_BOOT_UP:
        n2n.start_thread()

    # 初始化GUI
    gui = GUI()
    gui.run()

    # print(config.EDGE_PATH)
    # config = get_config()
    # print(config.EDGE_PATH)
    # edge = N2NEdge()
    # edge.start_thread()

