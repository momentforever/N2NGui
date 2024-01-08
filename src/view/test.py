from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QMessageBox, QCompleter, QHBoxLayout, QSizePolicy
from qfluentwidgets import LineEdit, PushButton, MessageBox, TextEdit

from src.tools.net_test_tool import NetTestTool


class TestWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Test")

        self.layout = QHBoxLayout(self)

        self.search_edges_button = PushButton()
        self.search_edges_button.setText("保存")
        self.search_edges_button.clicked.connect(self.search_edge_event)
        self.layout.addWidget(self.search_edges_button)

        self.net_test_tool = NetTestTool()
    def search_edge_event(self):
        edges = self.net_test_tool.get_edges()
        for edge in edges:
            pass