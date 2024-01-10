import traceback

from PyQt5.QtWidgets import QVBoxLayout, \
    QWidget
from qfluentwidgets import PushButton, MessageBox, CheckBox

from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.tools.config import Config
from src.tools.install_tool import InstallTool
from src.tools.startup_tool import StartupTool
from src.view.tool import Info


class SundryWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.install_tool = InstallTool()
        self.startup_tool = StartupTool()
        self.config = Config()

        self.setObjectName("Sundry")

        self.layout = QVBoxLayout(self)

        self.install_nic_button = PushButton(self)
        self.install_nic_button.setText("安装网卡驱动(必须)")
        self.install_nic_button.clicked.connect(self.install_nic_event)
        self.layout.addWidget(self.install_nic_button)

        self.install_broadcast_button = PushButton(self)
        self.install_broadcast_button.setText("安装广播插件(推荐)")
        self.install_broadcast_button.clicked.connect(self.install_broadcast_event)
        self.layout.addWidget(self.install_broadcast_button)


        self.auto_startup_check_box = CheckBox(self)
        self.auto_startup_check_box.setText("开机自启动")
        self.auto_startup_check_box.clicked.connect(self.auto_startup_event)
        self.layout.addWidget(self.auto_startup_check_box)

        self.load_setting()

    def load_setting(self):
        self.auto_startup_check_box.setChecked(self.config.is_auto_startup)

    def install_broadcast_event(self):
        Logger().debug("Install Broadcast Event")
        try:
            self.install_tool.install_broadcast()
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()


    def install_nic_event(self):
        Logger().debug("Install Nic Event")
        try:
            self.install_tool.install_nic()
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()

    def auto_startup_event(self):
        Logger().debug("Auto Startup Event")
        try:
            if self.auto_startup_check_box.isChecked():
                Logger().info("Open auto startup")
                self.startup_tool.add_to()
                self.config.is_auto_startup = True
            else:
                Logger().info("Close auto startup")
                self.startup_tool.delete_from()
                self.config.is_auto_startup = False

        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()
        finally:
            self.auto_startup_check_box.setChecked(self.config.is_auto_startup)

    def showEvent(self, a0):
        self.load_setting()
