import logging
import os
import sys

from src.common.custom_config import init_config
from src.common.custom_logging import init_logging
from src.tool.n2n_tool import init_n2n_edge
from src.gui.gui import GUI

# TODO 2.优化参数校验
# TODO 4.优化UI
# TODO 5.单元测试
# TODO 8.高级参数

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # 返回打包后可执行文件的路径
        return os.path.realpath(sys.executable)
    else:
        # 返回原始脚本文件的路径
        return os.path.realpath(__file__)


if __name__ == '__main__':
    current_dir = os.path.dirname(get_executable_path())
    # 初始化config
    config = init_config(current_dir)

    log = init_logging()

    n2n = init_n2n_edge()
    if config.IS_STARTUP:
        logging.info("Start in STARTUP!")
        n2n.start_thread()

    # 初始化GUI
    gui = GUI()
    gui.run()


