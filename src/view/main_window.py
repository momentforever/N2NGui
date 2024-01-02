import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, \
    QWidget, QAction, QMenu, QSystemTrayIcon, QApplication, QSizePolicy, QHBoxLayout
from qt_material import apply_stylesheet

from src.common.const import *
from src.view.log_monitor import LogMonitorView
from src.view.n2n_edge import N2NEdgeView


class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

        self.setWindowTitle("N2NGui")
        self.icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_32.ico"))
        self.normal_icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_normal_48.ico"))
        self.running_icon = QIcon(os.path.join(Path.WORKER_DIR, "statics\\icon_running_48.ico"))
        # 设置窗口图标
        self.setWindowIcon(self.icon)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._init_top_bar()
        self._init_system_bar()
        self._init_center()

        # 设置窗口默认大小
        screen_resolution = QApplication.desktop().screenGeometry()
        width, height = screen_resolution.width() * 0.4, screen_resolution.height() * 0.3
        self.resize(int(width), int(height))

    def _init_top_bar(self):
        # 初始化 主菜单
        self.menu_bar = self.menuBar()
        # 初始化 选项
        self.options_menu = QMenu("选项", self)
        # 初始化 开启自启动
        self.startup_action = QAction("开机自启动", self)
        # 设置 开启自启动
        self.startup_action.setCheckable(True)

        # 初始化 开启自启动
        self.auto_restart_action = QAction("自动异常重启", self)
        # 设置 开启自启动
        self.auto_restart_action.setCheckable(True)

        # 初始化 安装网卡
        self.install_nic_action = QAction("安装网卡驱动", self)

        # 初始化 退出
        self.close_action = QAction("退出", self)

        # 绑定设置
        self.menu_bar.addMenu(self.options_menu)

    def _init_system_bar(self):
        # 创建系统托盘菜单
        self.tray_icon = QSystemTrayIcon(self)

        self.tray_icon.setIcon(self.normal_icon)

        # 创建菜单项
        self.show_action = QAction("显示", self)
        self.quit_action = QAction("退出", self)

        # 将菜单项添加到菜单中
        self.menu = QMenu()
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.quit_action)

        # 设置系统托盘菜单
        self.tray_icon.setContextMenu(self.menu)

        # 显示系统托盘图标
        self.tray_icon.show()

    def _init_center(self):
        central_widget = QWidget(self)

        self.setCentralWidget(central_widget)
        self.center_layout = QHBoxLayout(central_widget)
        self.n2n_edge_window = None
        self.log_monitor_window = None

