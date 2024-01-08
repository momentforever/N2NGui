from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QMessageBox, QCompleter, QHBoxLayout, QSizePolicy
from qfluentwidgets import LineEdit, PushButton, MessageBox, TextEdit

from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.tools.config import Config
from src.tools.nic_tool import NicTool
from src.tools.startup_tool import StartupTool


class SundryWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nic_tool = NicTool()
        self.startup_tool = StartupTool()
        self.config = Config()

        self.setObjectName("Sundry")

        self.layout = QHBoxLayout(self)

        self.install_nic_button = PushButton()
        self.install_nic_button.setText("安装网卡驱动")
        self.install_nic_button.clicked.connect(self.install_nic_event)
        self.layout.addWidget(self.install_nic_button)

        self.auto_startup_button = PushButton()
        self.auto_startup_button.setText("开机自启动")
        self.auto_startup_button.clicked.connect(self.auto_startup_event)
        self.layout.addWidget(self.auto_startup_button)

    def install_nic_event(self):
        Logger().debug("install nic event")
        try:
            self.nic_tool.install()
        except N2NGuiException as e:
            MessageBox("错误", e.args[0], parent=self.parent())
        except Exception as e:
            Logger().error(e)
            MessageBox("错误", "未知错误，详情请见日志", parent=self.parent())

    def auto_startup_event(self):
        Logger().debug("auto startup event")
        try:
            self.startup_tool.add_to()
            self.config.is_auto_startup = True

        except N2NGuiException as e:
            MessageBox("错误", e.args[0], parent=self.parent())
        except Exception as e:
            Logger().error(e)
            MessageBox("错误", "未知错误，详情请见日志", parent=self.parent())