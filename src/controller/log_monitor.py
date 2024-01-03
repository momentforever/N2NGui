import time

from PyQt5.QtCore import QThread, pyqtSignal

from src.common.const import *
from src.view.log_monitor import LogMonitorView


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


class LoggerMonitorController:
    def __init__(self, view: LogMonitorView):
        # view
        self.view = view

        # bind
        self.log_monitor_thread = LogMonitorThread()
        self.log_monitor_thread.update_signal.connect(self.append_log)
        self.log_monitor_thread.start()

    def append_log(self, log):
        self.view.text_box.append(log)
        self.view.text_box.moveCursor(self.view.text_box.textCursor().End)
