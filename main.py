from src.common.logger import Logger
from src.tools.config import Config
from src.tools.n2n_edge_tool import N2NEdge
from src.gui import GUI



if __name__ == '__main__':
    # 初始化
    Logger()
    Config()
    N2NEdge()
    # 初始化GUI
    gui = GUI()
    gui.run()
