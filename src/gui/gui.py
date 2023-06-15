import sys
from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow


class GUI:
    def run(self):
        app = QApplication(sys.argv)
        MainWindow()
        sys.exit(app.exec_())

