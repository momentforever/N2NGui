import sys
from PyQt5.QtWidgets import QApplication

from src.view.main_window import MainWindow


class GUI:
    def run(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
