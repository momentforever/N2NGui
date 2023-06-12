import sys
from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow


class GUI:
    def run(self):
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.show()
        sys.exit(app.exec_())

