from src.common.logger import Logger
from src.model.config import Config
from src.model.n2n_edge import N2NEdge
from src.view.gui import GUI



if __name__ == '__main__':
    # 初始化
    Logger()
    Config()
    N2NEdge()
    # 初始化GUI
    gui = GUI()
    gui.run()
