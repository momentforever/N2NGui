from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QMenu, QSystemTrayIcon, QApplication, QSizePolicy, \
    QHBoxLayout

from src.common.const import *
from src.view.log_monitor import LogMonitorView
from src.view.n2n_edge import N2NEdgeView


class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.startup_action.setCheckable(True)
        self.options_menu.addAction(self.startup_action)

        # 初始化 安装网卡
        self.install_nic_action = QAction("安装网卡驱动", self)
        self.options_menu.addAction(self.install_nic_action)

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

        self.n2n_edge_view = N2NEdgeView()
        self.center_layout.addWidget(self.n2n_edge_view, 2)
        self.log_monitor_view = LogMonitorView()
        self.center_layout.addWidget(self.log_monitor_view, 5)
