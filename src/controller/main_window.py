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
    def __init__(self):
        self.config = Config()
        self.startup_tool = StartupTool()
        self.nic_tool = NicTool()
        self.view = MainWindowView()

        self.log_monitor = LoggerMonitorController()
        self.n2n_edge = N2NEdgeController()

        self.view.n2n_edge_window = self.n2n_edge.view
        self.view.log_monitor_window = self.log_monitor.view

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
        self.view.show()

    def hang_up_event(self):
        # 隐藏主窗口
        self.view.hide()

    def quit_event(self):
        # 退出应用程序
        self.view.tray_icon.hide()
        try:
            self.n2n_edge.config_model.save()
            self.n2n_edge.n2n_edge_model.stop_thread()
        except:
            pass
        self.view.log_window.close()
        QApplication.exit()

    def tray_icon_activated_event(self, reason):
        # 处理系统托盘图标的双击事件
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_event()

    def closeEvent(self, event):
        event.ignore()
        self.hang_up_event()

    def stop_n2n_handler(self):
        self.view.tray_icon.setIcon(self.view.normal_icon)

    def start_n2n_handler(self):
        self.view.tray_icon.setIcon(self.view.running_icon)
