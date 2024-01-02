import sys
from PyQt5.QtWidgets import QApplication

from src.controller.main_window import MainWindowController

class GUI:
    def run(self):
        app = QApplication(sys.argv)
        MainWindowController()
        sys.exit(app.exec_())
