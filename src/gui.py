import sys
from PyQt5.QtWidgets import QApplication

from src.view.main_window import MainWindow

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

class MyApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = MainWindow()
        self.aboutToQuit.connect(self.onAboutToQuit)

    def onAboutToQuit(self):
        self.window.close_handler()


class GUI:
    def run(self):
        app = MyApplication(sys.argv)
        sys.exit(app.exec_())
