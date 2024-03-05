import time

from PyQt5.QtCore import QThread, pyqtSignal

from src.common.const import *


class LogMonitorThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(LogMonitorThread, self).__init__(*args, **kwargs)
        self.stop_flag = False

    def run(self):
        with open(Path.LOG_PATH, 'r', encoding='utf-8') as file:
            while True:
                if self.stop_flag:
                    break
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self.update_signal.emit(line.strip())

    def stop(self):
        self.stop_flag = True

    def stop_wait(self):
        self.stop()
        self.wait()
