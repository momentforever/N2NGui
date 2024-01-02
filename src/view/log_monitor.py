import logging
import threading
import time
from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QSizePolicy
from qt_material import apply_stylesheet


class LogMointorView(QWidget):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

        layout = QVBoxLayout(self)

        self.text_box = QTextEdit(self)
        self.text_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.resize(self.sizeHint())
