import logging
import threading
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QSizePolicy
from qt_material import apply_stylesheet

from src.common.const import *
from src.view.log_monitor import LogMointorView

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
    def __init__(self):
        self.view = LogMointorView()
        self.file_monitor_thread = LogMonitorThread()
        self.file_monitor_thread.update_signal.connect(self.append_log)
        self.file_monitor_thread.start()

    def append_log(self, log):
        self.view.text_box.append(log)
        self.view.text_box.moveCursor(self.view.text_box.textCursor().End)
