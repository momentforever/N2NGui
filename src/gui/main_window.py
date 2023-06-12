import logging
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, \
    QWidget, QAction, QMenu, QSystemTrayIcon, QApplication
from src.common.custom_config import get_config
from src.common.custom_const import Status
from src.common.custom_exception import CustomException
from src.gui.log_window import LogWindow
from src.tool.nic_tool import install_nic
from src.tool.startup_tool import add_to_startup, delete_from_startup
from src.tool.n2n_tool import get_n2n_edge


class MainWindow(QMainWindow):
    n2n_edge = None

    def __init__(self):
        super().__init__()
        config = get_config()

        self.setWindowTitle("N2NGui")
        self.setFixedSize(800, 600)
        self.icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_32.ico"))
        # 设置窗口图标
        self.setWindowIcon(self.icon)

        self.normal_icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_normal_48.ico"))
        self.running_icon = QIcon(os.path.join(config.WORKER_DIR, "statics\\icon_running_48.ico"))

        self._init_top_bar()
        self._init_system_bar()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        supernode_label = QLabel("超级节点地址和端口*：")
        self.supernode_entry = QLineEdit()
        if config.SUPERNODE:
            self.supernode_entry.setText(config.SUPERNODE)
        layout.addWidget(supernode_label)
        layout.addWidget(self.supernode_entry)

        edge_community_label = QLabel("小组名称*：")
        self.edge_community_entry = QLineEdit()
        if config.EDGE_COMMUNITY:
            self.edge_community_entry.setText(config.EDGE_COMMUNITY)
        layout.addWidget(edge_community_label)
        layout.addWidget(self.edge_community_entry)

        edge_community_password_label = QLabel("小组密码：")
        self.edge_community_password_entry = QLineEdit()
        self.edge_community_password_entry.setEchoMode(QLineEdit.Password)
        if config.EDGE_COMMUNITY_PASSWORD:
            self.edge_community_password_entry.setText(config.EDGE_COMMUNITY_PASSWORD)
        layout.addWidget(edge_community_password_label)
        layout.addWidget(self.edge_community_password_entry)

        edge_ip_label = QLabel("Edge IP 地址：")
        self.edge_ip_entry = QLineEdit()
        if config.EDGE_IP:
            self.edge_ip_entry.setText(config.EDGE_IP)
        layout.addWidget(edge_ip_label)
        layout.addWidget(self.edge_ip_entry)

        self.start_button = QPushButton("启动")
        self.start_button.clicked.connect(self.start_edge_event)
        layout.addWidget(self.start_button)

        self.log_window = LogWindow()
        layout.addWidget(self.log_window)

        # # 创建 QTimer 对象
        # self.timer = QTimer(self)
        # # 设置定时器触发间隔，单位为毫秒
        # self.timer.setInterval(1000)
        # # 将定时器的 timeout 信号与更新事件的槽函数连接
        # self.timer.timeout.connect(self.update_event)
        # # 启动定时器
        # self.timer.start()

    def start_edge_event(self):
        try:
            self.n2n_edge = get_n2n_edge()
            config = get_config()
            if self.n2n_edge.status in Status.ENABLE_START:
                config.SUPERNODE = self.supernode_entry.text()
                config.EDGE_IP = self.edge_ip_entry.text()
                config.EDGE_COMMUNITY = self.edge_community_entry.text()
                config.EDGE_COMMUNITY_PASSWORD = self.edge_community_password_entry.text()

                self.n2n_edge.start_thread()
                config.write_to_config()
                self.start_button.setText("停止")
                self.tray_icon.setIcon(self.running_icon)
            else:
                self.n2n_edge.stop_thread()
                self.start_button.setText("启动")
                self.tray_icon.setIcon(self.normal_icon)
        except CustomException as e:
            QMessageBox.information(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.information(self, "错误", "未知错误")

    def add_startup_event(self):
        try:
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

        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

    def install_nic_event(self):
        try:
            install_nic()
        except CustomException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.warning(self, "错误", "未知错误")

    def update_event(self):
        if self.n2n_edge and self.n2n_edge.status in Status.ENABLE_START and self.start_button.text() == "停止":
            self.start_button.setText("启动")

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

        # 初始化 安装网卡
        self.install_nic_action = QAction("安装网卡驱动", self)
        # 设置 安装网卡
        self.install_nic_action.triggered.connect(self.install_nic_event)
        # 绑定 安装网卡
        self.options_menu.addAction(self.install_nic_action)

        # 绑定设置
        self.menu_bar.addMenu(self.options_menu)

    def _init_system_bar(self):
        config = get_config()

        # 创建系统托盘菜单
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.normal_icon)

        # 创建菜单项
        show_action = QAction("显示", self)
        hang_up_action = QAction("挂起", self)
        quit_action = QAction("退出", self)

        # 将菜单项添加到菜单中
        menu = QMenu()
        menu.addAction(show_action)
        menu.addAction(hang_up_action)
        menu.addAction(quit_action)

        # 设置系统托盘菜单
        self.tray_icon.setContextMenu(menu)

        # 显示系统托盘图标
        self.tray_icon.show()

        # 连接菜单项的信号和槽函数
        show_action.triggered.connect(self.show_event)
        hang_up_action.triggered.connect(self.hang_up_event)
        quit_action.triggered.connect(self.quit_event)

        # 连接双击系统托盘图标的信号和槽函数
        self.tray_icon.activated.connect(self.tray_icon_activated_event)

    def show_event(self):
        # 显示主窗口
        self.show()

    def hang_up_event(self):
        # 隐藏主窗口
        self.hide()

    def quit_event(self):
        # 退出应用程序
        self.tray_icon.hide()
        if self.n2n_edge:
            self.n2n_edge.stop_thread()
        self.log_window.close()
        QApplication.exit()

    def tray_icon_activated_event(self, reason):
        # 处理系统托盘图标的双击事件
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_event()

    def closeEvent(self, event):
        event.ignore()
        self.hang_up_event()
