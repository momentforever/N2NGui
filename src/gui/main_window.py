import logging
import os
import sys

from qt_material import apply_stylesheet
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, \
    QWidget, QAction, QMenu, QSystemTrayIcon, QApplication, QSizePolicy, QHBoxLayout
from src.common.custom_config import get_config
from src.common.custom_exception import CustomException
from src.gui.log_window import LogWindow
from src.gui.n2n_window import N2NWindow
from src.gui.quick_start_window import QuickStartWindow
from src.tool.nic_tool import install_nic
from src.tool.startup_tool import add_to_startup, delete_from_startup, is_admin
from src.tool.n2n_tool import get_n2n_edge


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

        config = get_config()
        n2n_edge = get_n2n_edge()

        self.setWindowTitle("N2NGui")
        self.icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_32.ico"))
        self.normal_icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_normal_48.ico"))
        self.running_icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_running_48.ico"))
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

        if config.IS_STARTUP:
            # 开机自启动
            n2n_edge.start_thread()
        else:
            if not config.IS_QS:
                if not is_admin():
                    self.box = QMessageBox()
                    result = self.box.critical(self, "错误", "首次请以管理员方式启动")
                    # 当用户点击“确定”按钮时，退出程序
                    if result == QMessageBox.Ok:
                        self.quit_event()
                        sys.exit()
                self.quick_start = QuickStartWindow()
            self.show()

    def _init_top_bar(self):
        config = get_config()
        # 初始化 主菜单
        self.menu_bar = self.menuBar()
        # 初始化 选项
        self.options_menu = QMenu("选项", self)
        # 初始化 开启自启动
        self.startup_action = QAction("开机自启动", self)
        # 设置 开启自启动
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(config.IS_STARTUP)
        self.startup_action.triggered.connect(self.add_startup_event)
        # 绑定 开机自启动
        self.options_menu.addAction(self.startup_action)

        # 初始化 开启自启动
        self.auto_restart_action = QAction("自动异常重启", self)
        # 设置 开启自启动
        self.auto_restart_action.setCheckable(True)
        self.auto_restart_action.setChecked(config.IS_UNLESS_STOP)
        self.auto_restart_action.triggered.connect(self.auto_restart_event)
        # 绑定 开机自启动
        self.options_menu.addAction(self.auto_restart_action)

        # 初始化 安装网卡
        self.install_nic_action = QAction("安装网卡驱动", self)
        # 设置 安装网卡
        self.install_nic_action.triggered.connect(self.install_nic_event)
        # 绑定 安装网卡
        self.options_menu.addAction(self.install_nic_action)

        # 初始化 退出
        self.close_action = QAction("退出", self)
        # 设置 退出
        self.close_action.triggered.connect(self.quit_event)
        # 绑定 退出
        self.options_menu.addAction(self.close_action)

        # 绑定设置
        self.menu_bar.addMenu(self.options_menu)

    def _init_system_bar(self):
        config = get_config()
        n2n_edge = get_n2n_edge()

        # 创建系统托盘菜单
        self.tray_icon = QSystemTrayIcon(self)

        self.tray_icon.setIcon(self.normal_icon)

        # 创建菜单项
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)

        # 将菜单项添加到菜单中
        menu = QMenu()
        menu.addAction(show_action)
        menu.addAction(quit_action)

        # 设置系统托盘菜单
        self.tray_icon.setContextMenu(menu)

        # 显示系统托盘图标
        self.tray_icon.show()

        # 连接菜单项的信号和槽函数
        show_action.triggered.connect(self.show_event)
        quit_action.triggered.connect(self.quit_event)

        # 连接双击系统托盘图标的信号和槽函数
        self.tray_icon.activated.connect(self.tray_icon_activated_event)

        n2n_edge.start_handlers.register(self.start_n2n_handler)
        n2n_edge.stop_handlers.register(self.stop_n2n_handler)

    def _init_center(self):
        central_widget = QWidget(self)

        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.n2n_window = N2NWindow()
        layout.addWidget(self.n2n_window, 2)
        self.log_window = LogWindow()
        layout.addWidget(self.log_window, 5)

    def add_startup_event(self):
        is_success = False
        try:
            if self.startup_action.isChecked():
                add_to_startup()
            else:
                delete_from_startup()
            # 写入配置文件
            config = get_config()
            config.IS_STARTUP = self.startup_action.isChecked()
            config.write_to_config()
            is_success = True
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

        if not is_success:
            self.startup_action.setChecked(not self.startup_action.isChecked())

    def install_nic_event(self):
        try:
            install_nic()
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

    def auto_restart_event(self):
        is_success = False
        try:
            config = get_config()
            config.IS_UNLESS_STOP = self.auto_restart_action.isChecked()
            config.write_to_config()
            is_success = True
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

        if not is_success:
            self.auto_restart_action.setChecked(not self.auto_restart_action.isChecked())

    def show_event(self):
        # 显示主窗口
        self.show()

    def hang_up_event(self):
        # 隐藏主窗口
        self.hide()

    def quit_event(self):
        # 退出应用程序
        self.tray_icon.hide()
        try:
            n2n_edge = get_n2n_edge()
            n2n_edge.stop_thread()
        except:
            pass
        self.log_window.close()
        QApplication.exit()

    def tray_icon_activated_event(self, reason):
        # 处理系统托盘图标的双击事件
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_event()

    def closeEvent(self, event):
        event.ignore()
        self.hang_up_event()

    def stop_n2n_handler(self):
        self.tray_icon.setIcon(self.normal_icon)

    def start_n2n_handler(self):
        self.tray_icon.setIcon(self.running_icon)
