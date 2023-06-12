import os.path
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.common.custom_config import get_config
from src.gui.main_window import MainWindow


class GUI:
    def run(self):
        config = get_config()
        app = QApplication(sys.argv)
        mw = MainWindow()
        # 设置图标
        icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_32.ico"))
        mw.setWindowIcon(icon)
        mw.show()

        sys.exit(app.exec_())

