from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QGridLayout, QTextEdit, QSizePolicy

from src.common.const import *


class AdvancedSettingView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("高级设置")
        self.icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_32.ico"))
        self.setWindowIcon(self.icon)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # 设置窗口置顶属性
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        setting_layout = QGridLayout()

        package_size_label = QLabel("包大小(MTU)：")
        self.package_size_entry = QLineEdit()
        self.package_size_entry.setValidator(QIntValidator())
        setting_layout.addWidget(package_size_label, 0, 0)
        setting_layout.addWidget(self.package_size_entry, 0, 1)

        edge_description_label = QLabel("设备描述：")
        self.edge_description_entry = QLineEdit()
        setting_layout.addWidget(edge_description_label, 1, 0)
        setting_layout.addWidget(self.edge_description_entry, 1, 1)

        edge_etc_args_label = QLabel("其他参数\n(支持#注释)：")
        self.edge_etc_args_entry = QTextEdit()
        setting_layout.addWidget(edge_etc_args_label, 2, 0)
        setting_layout.addWidget(self.edge_etc_args_entry, 2, 1)

        # 添加布局
        layout.addLayout(setting_layout)

        # 添加保存
        self.save_button = QPushButton("保存")
        layout.addWidget(self.save_button)

        # 添加取消
        self.close_button = QPushButton("取消")
        layout.addWidget(self.close_button)
