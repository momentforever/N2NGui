import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QSizePolicy, QHBoxLayout, QMessageBox, QPushButton, QApplication
from qt_material import apply_stylesheet

from src.common.custom_config import get_config
from src.common.custom_exception import CustomException
from src.tool.nic_tool import install_nic


class QuickStartWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

        config = get_config()

        self.setWindowTitle("快速开始")

        self.icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_32.ico"))
        self.setWindowIcon(self.icon)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # 设置窗口置顶属性
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 创建布局
        self.layout = QVBoxLayout(self)

        # 添加提示文本
        self.label = QLabel("是否安装网驱动？")
        # self.label.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.label, 0, Qt.AlignCenter)

        # 添加按钮
        self.button_install = QPushButton("安装")
        self.button_cancel = QPushButton("取消")

        # 连接按钮的信号与槽
        self.button_install.clicked.connect(self.install_nic_event)
        self.button_cancel.clicked.connect(self.close_event)

        self.button_layout = QHBoxLayout(self)
        # 将按钮添加到消息框
        self.button_layout.addWidget(self.button_install)
        self.button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(self.button_layout)

        # 设置窗口默认大小
        screen_resolution = QApplication.desktop().screenGeometry()
        width, height = screen_resolution.width() * 0.1, screen_resolution.height() * 0.15
        self.resize(int(width), int(height))

        self.show()

    def resizeEvent(self, event):
        width = self.width()
        height = self.height()
        # 计算边距
        left_margin = right_margin = int(width * 0.2)  # 设置左右边距为窗口宽度的10%
        top_margin = bottom_margin = int(height * 0.2)  # 设置上下边距为窗口高度的10%
        # 设置布局边距
        self.layout.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)

    def install_nic_event(self):
        try:
            install_nic()
            self.close_event()
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

    def close_event(self):
        self.set_is_qs_event()
        self.destroy()

    def closeEvent(self, event):
        self.close_event()

    def set_is_qs_event(self):
        try:
            config = get_config()
            config.IS_QS = True
            # 先写入配置文件
            config.write_to_config()
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")
