import sys
from PyQt5.QtWidgets import QApplication

from src.controller.main_window import MainWindowController
from src.view.main_window import MainWindowView

class GUI:
    def run(self):
        app = QApplication(sys.argv)
        window = MainWindowView()
        controller = MainWindowController(window)
        sys.exit(app.exec_())
