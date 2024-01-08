from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QMenu, QSystemTrayIcon, QApplication, QSizePolicy, \
    QHBoxLayout

from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from src.common.const import *
from src.tools.config import Config
from src.view.advanced_setting import AdvancedSettingWidget
from src.view.home import HomeWidget
from src.view.sundry import SundryWidget


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_center()
        self._init_system_bar()

        self.show()

    def _init_center(self):
        self.home_interface = HomeWidget(parent=self)
        self.advanced_setting_interface = AdvancedSettingWidget(parent=self)
        self.sundry_interface = SundryWidget(parent=self)
        self.addSubInterface(self.home_interface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.advanced_setting_interface, FIF.DEVELOPER_TOOLS, '高级')
        self.addSubInterface(self.sundry_interface, FIF.SETTING, '设置')

    def _init_window(self):
        self.font = QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.setWindowTitle("N2NGui")
        self.icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_32.ico"))
        self.normal_icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_normal_48.ico"))
        self.running_icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_running_48.ico"))
        # 设置窗口图标
        self.setWindowIcon(self.icon)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 设置窗口默认大小
        screen_resolution = QApplication.desktop().screenGeometry()
        width, height = screen_resolution.width() * 0.4, screen_resolution.height() * 0.3
        self.resize(int(width), int(height))

    def _init_system_bar(self):
        # 创建系统托盘菜单
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.normal_icon)

        self.menu = RoundMenu(parent=self)

        # add actions
        self.show_action = Action(FIF.HOME, '显示')
        self.hide_action = Action(FIF.HIDE, '隐藏')
        self.close_action = Action(FIF.CLOSE, '退出')

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addAction(self.close_action)

        self.show_action.triggered.connect(self.show_event)
        self.hide_action.triggered.connect(self.hide_event)
        self.close_action.triggered.connect(self.close_event)

        # 设置系统托盘菜单
        self.tray_icon.setContextMenu(self.menu)

        # 显示系统托盘图标
        self.tray_icon.show()

    def show_event(self):
        if not (self.windowFlags() | Qt.WindowStaysOnTopHint) == self.windowFlags():
            self.setWindowFlags(Qt.WindowStaysOnTopHint | self.windowFlags())
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()

    def hide_event(self):
        self.hide()

    def close_event(self):
        self.close()

    def closeEvent(self, event):
        Config().save()
