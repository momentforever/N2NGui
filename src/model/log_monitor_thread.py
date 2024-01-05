import time

from PyQt5.QtCore import QThread, pyqtSignal

from src.common.const import *


class LogMonitorThread(QThread):
    update_signal = pyqtSignal(str)

    def run(self):
        with open(Path.LOG_PATH, 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self.update_signal.emit(line.strip())
