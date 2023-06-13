import logging
import threading
import time
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout
from src.common.custom_config import get_config


class LogWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log Window")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.text_box = QTextEdit(self)
        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        config = get_config()
        self.log_file = config.LOG_PATH

        self.is_running = True
        self.worker_thread = threading.Thread(target=self.log_worker)
        self.worker_thread.start()

    def append_log(self, log):
        self.text_box.append(log)
        self.text_box.moveCursor(self.text_box.textCursor().End)

    def log_worker(self):
        while self.is_running:
            try:
                with open(self.log_file, "r", encoding='gbk') as file:
                    # file.seek(0, 2)  # Move the file pointer to the end
                    while self.is_running:
                        line = file.readline().strip()
                        if line:
                            self.append_log(line)
                        time.sleep(0.1)  # Wait for some time before reading the file
            except FileNotFoundError:
                time.sleep(1)  # If the file doesn't exist, wait for some time before trying to open it
            except Exception as e:
                logging.error(e)

    def closeEvent(self, event):
        self.is_running = False
        self.worker_thread.join()
        super().closeEvent(event)
