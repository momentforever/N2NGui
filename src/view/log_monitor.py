from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QSizePolicy

from src.model.log_monitor_thread import LogMonitorThread


class LogMonitorView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.text_box = QTextEdit(self)
        self.text_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.resize(self.sizeHint())

        self.log_monitor_thread = LogMonitorThread()
        self.log_monitor_thread.update_signal.connect(self.append_log)
        self.log_monitor_thread.start()

    def append_log(self, log):
        self.text_box.append(log)
        self.text_box.moveCursor(self.text_box.textCursor().End)
