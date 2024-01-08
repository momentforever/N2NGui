from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon, QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QGridLayout, QTextEdit, QSizePolicy
from qfluentwidgets import LineEdit, TextEdit, PushButton, StrongBodyLabel, BodyLabel

from src.common.const import *
from src.tools.config import Config


class AdvancedSettingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # model
        self.config = Config()

        self.setObjectName("Advanced Setting")

        self.font = QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.layout = QVBoxLayout(self)
        setting_layout = QGridLayout()

        package_size_label = BodyLabel("包大小(MTU)")
        self.package_size_entry = LineEdit()
        self.package_size_entry.setValidator(QIntValidator())
        setting_layout.addWidget(package_size_label, 0, 0)
        setting_layout.addWidget(self.package_size_entry, 0, 1)

        edge_description_label = BodyLabel("设备描述：")
        self.edge_description_entry = LineEdit()
        setting_layout.addWidget(edge_description_label, 1, 0)
        setting_layout.addWidget(self.edge_description_entry, 1, 1)

        edge_etc_args_label = BodyLabel("其他参数(支持#注释)：")
        self.edge_etc_args_entry = TextEdit()
        setting_layout.addWidget(edge_etc_args_label, 2, 0)
        setting_layout.addWidget(self.edge_etc_args_entry, 2, 1)

        # 添加布局
        self.layout.addLayout(setting_layout)

        # 添加保存
        self.save_button = PushButton()
        self.save_button.setText("保存")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.load_settings()

    def load_settings(self):
        self.package_size_entry.setText(str(self.config.edge_package_size))
        self.edge_description_entry.setText(self.config.edge_description)
        self.edge_etc_args_entry.setText("\n".join(self.config.edge_etc_args))

    def save_settings(self):
        self.config.edge_package_size = int(self.package_size_entry.text())
        self.config.edge_description = self.edge_description_entry.text()
        self.config.edge_etc_args = self.edge_etc_args_entry.toPlainText().split("\n")

    def showEvent(self, a0):
        self.load_settings()
