import os.path
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.common.custom_config import get_config
from src.gui.main_window import MainWindow


class GUI:
    def run(self):
        app = QApplication(sys.argv)
        mw = MainWindow()
        sys.exit(app.exec_())

