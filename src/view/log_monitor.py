from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QSizePolicy


class LogMonitorView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.text_box = QTextEdit(self)
        self.text_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.resize(self.sizeHint())
