from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QGridLayout, QTextEdit, QSizePolicy
from qfluentwidgets import LineEdit, TextEdit

from src.common.const import *
from src.tools.config import Config


class AdvancedSettingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Advanced Setting")

        self.is_changed = False

        layout = QVBoxLayout(self)

        setting_layout = QGridLayout()

        package_size_label = QLabel("包大小(MTU)")
        self.package_size_entry = LineEdit()
        self.package_size_entry.setValidator(QIntValidator())
        setting_layout.addWidget(package_size_label, 0, 0)
        setting_layout.addWidget(self.package_size_entry, 0, 1)

        edge_description_label = QLabel("设备描述：")
        self.edge_description_entry = LineEdit()
        setting_layout.addWidget(edge_description_label, 1, 0)
        setting_layout.addWidget(self.edge_description_entry, 1, 1)

        edge_etc_args_label = QLabel("其他参数\n(支持#注释)：")
        self.edge_etc_args_entry = TextEdit()
        setting_layout.addWidget(edge_etc_args_label, 2, 0)
        setting_layout.addWidget(self.edge_etc_args_entry, 2, 1)

        # 添加布局
        layout.addLayout(setting_layout)

        # 添加保存
        self.save_button = QPushButton("保存")
        layout.addWidget(self.save_button)

        # bind
        self.save_button.clicked.connect(self.save_settings)

        # model
        self.config = Config()

        # self.load_settings()

    def load_settings(self):
        if self.config.edge_package_size:
            self.view.package_size_entry.setText(str(self.config.edge_package_size))

        if self.config.edge_description:
            self.view.package_size_entry.setText(self.config.edge_description)

        if self.config.edge_etc_args:
            self.view.edge_etc_args_entry.setText("\n".join(self.config.edge_etc_args))

    def save_settings(self):
        self.config.edge_package_size = self.view.package_size_entry.text()
        self.config.edge_description = self.view.edge_description_entry.text()
        self.config.edge_etc_args = self.view.edge_etc_args_entry.toPlainText().split("\n")
