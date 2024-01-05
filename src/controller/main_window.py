from PyQt5.QtWidgets import QMessageBox, QApplication, QSystemTrayIcon

from src.common.const import Status
from src.common.exception import *
from src.common.logger import Logger
from src.controller.log_monitor import LoggerMonitorController
from src.controller.n2n_edge import N2NEdgeController
from src.tools.config import Config
from src.tools.nic_tool import NicTool
from src.tools.startup_tool import StartupTool
from src.view.main_window import MainWindowView


class MainWindowController:
    def __init__(self, view: MainWindowView):
        # model
        self.config = Config()
        self.startup_tool = StartupTool()
        self.nic_tool = NicTool()
        # view
        self.view = view

        # bind
        self.log_monitor = LoggerMonitorController(self.view.home_interface.log_monitor_view)
        self.n2n_edge = N2NEdgeController(self.view.home_interface.n2n_edge_view)
        self.view.home_interface.n2n_edge_view.status_signal.connect(self.update_tray_icon)

        # self.view.startup_action.setChecked(self.config.is_auto_startup)
        # self.view.startup_action.triggered.connect(self.set_startup_event)
        #
        # self.view.install_nic_action.triggered.connect(self.install_nic_event)
        #
        # self.view.show_action.triggered.connect(self.show_event)
        # self.view.quit_action.triggered.connect(self.quit_event)
        # self.view.tray_icon.activated.connect(self.tray_icon_activated_event)

        self.view.closeEvent = self.closeEvent

        self.view.show()

    def closeEvent(self, event):
        event.ignore()
        self.hang_up_event()

    def set_startup_event(self):
        Logger().debug("set startup event")
        is_success = False
        try:
            if self.view.startup_action.isChecked():
                self.startup_tool.add_to()
            else:
                self.startup_tool.delete_from()
            # 写入配置文件
            self.config.is_auto_startup = self.view.startup_action.isChecked()
            is_success = True
        except N2NGuiException as e:
            QMessageBox.warning(self.view, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self.view, "错误", "未知错误")

        if not is_success:
            self.view.startup_action.setChecked(not self.view.startup_action.isChecked())

    def install_nic_event(self):
        Logger().debug("install nic event")
        try:
            self.nic_tool.install()
        except N2NGuiException as e:
            QMessageBox.warning(self.view, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self.view, "错误", "未知错误")

    def update_tray_icon(self, status):
        if status == Status.OFF:
            self.view.tray_icon.setIcon(self.view.normal_icon)
        else:
            self.view.tray_icon.setIcon(self.view.running_icon)

    def tray_icon_activated_event(self, reason):
        # 处理系统托盘图标的双击事件
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_event()

    def show_event(self):
        # 显示主窗口
        self.view.show()

    def hang_up_event(self):
        # 隐藏主窗口
        self.view.hide()

    def quit_event(self):
        self.view.tray_icon.hide()
        self.view.close()
        try:
            self.n2n_edge.n2n_edge_model.stop_thread()
            self.n2n_edge.config_model.save()
        except Exception as e:
            Logger().error(e)
        QApplication.exit()
