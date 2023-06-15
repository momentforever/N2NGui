import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, \
    QWidget, QHBoxLayout, QGridLayout, QTextEdit, QSizePolicy
from qt_material import apply_stylesheet

from src.common.custom_config import get_config
from src.common.custom_exception import CustomException


class AdvancedSettingWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

        config = get_config()

        self.setWindowTitle("高级设置")
        self.icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_32.ico"))
        self.setWindowIcon(self.icon)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # 设置窗口置顶属性
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout(self)

        setting_layout = QGridLayout()

        package_size_label = QLabel("包大小(MTU)：")
        self.package_size_entry = QLineEdit()
        self.package_size_entry.setValidator(QIntValidator())
        if config.EDGE_PACKAGE_SIZE:
            self.package_size_entry.setText(config.EDGE_PACKAGE_SIZE)
        setting_layout.addWidget(package_size_label, 0, 0)
        setting_layout.addWidget(self.package_size_entry, 0, 1)

        edge_description_label = QLabel("设备描述：")
        self.edge_description_entry = QLineEdit()
        if config.EDGE_DESCRIPTION:
            self.package_size_entry.setText(config.EDGE_DESCRIPTION)
        setting_layout.addWidget(edge_description_label, 1, 0)
        setting_layout.addWidget(self.edge_description_entry, 1, 1)

        edge_etc_args_label = QLabel("其他参数\n(支持#注释)：")
        self.edge_etc_args_entry = QTextEdit()
        if config.EDGE_ETC_ARGS:
            self.edge_etc_args_entry.setText(config.EDGE_ETC_ARGS)
        setting_layout.addWidget(edge_etc_args_label, 2, 0)
        setting_layout.addWidget(self.edge_etc_args_entry, 2, 1)

        # 添加布局
        layout.addLayout(setting_layout)

        # 添加保存
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_event)
        layout.addWidget(self.save_button)

    def save_event(self):
        try:
            config = get_config()
            config.EDGE_PACKAGE_SIZE = self.package_size_entry.text()
            config.EDGE_DESCRIPTION = self.edge_description_entry.text()
            config.EDGE_ETC_ARGS = self.edge_etc_args_entry.toPlainText()
            # 先写入配置文件
            config.write_to_config()

            self.close()
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")
