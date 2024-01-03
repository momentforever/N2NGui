from PyQt5.QtWidgets import QMessageBox, QApplication, QSystemTrayIcon, QWidget, QHBoxLayout

from src.common.exception import *
from src.view.main_window import MainWindowView
from src.common.logger import Logger

from src.model.config import Config
from src.model.startup_tool import StartupTool
from src.model.nic_tool import NicTool

from src.controller.advance_setting import AdvancedSettingController
from src.controller.log_monitor import LoggerMonitorController
from src.controller.n2n_edge import N2NEdgeController

class MainWindowController:
    def __init__(self, view: MainWindowView):
        # model
        self.config = Config()
        self.startup_tool = StartupTool()
        self.nic_tool = NicTool()
        # view
        self.view = view

        # bind
        self.log_monitor = LoggerMonitorController(self.view.log_monitor_window)
        self.n2n_edge = N2NEdgeController(self.view.n2n_edge_window)

        self.view.show()

    def add_startup_event(self):
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
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self, "错误", "未知错误")

        if not is_success:
            self.view.startup_action.setChecked(not self.view.startup_action.isChecked())

    def install_nic_event(self):
        try:
            self.nic_tool.install()
        except N2NGuiException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self, "错误", "未知错误")


    def show_event(self):
        # 显示主窗口
        self.view.show()

    def hang_up_event(self):
        # 隐藏主窗口
        self.view.hide()

    def quit_event(self):
        # 退出应用程序
        self.view.tray_icon.hide()
        try:
            self.n2n_edge.n2n_edge_model.stop_thread()
            self.n2n_edge.config_model.save()
        except:
            pass
        self.view.close()
        QApplication.exit()
