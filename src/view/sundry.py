import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, \
    QWidget, QHBoxLayout
from qfluentwidgets import PushButton, MessageBox, CheckBox, StrongBodyLabel, BodyLabel, TitleLabel, SubtitleLabel, \
    TransparentToolButton, CaptionLabel, IconWidget, CardWidget, SwitchButton, HyperlinkButton
from qfluentwidgets import FluentIcon as FIF

from src.common.const import *
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

        self.system_setting_label = SubtitleLabel(self)
        self.system_setting_label.setText("系统设置")
        self.layout.addWidget(self.system_setting_label)

        self.startup_card = StartUpCard()
        self.layout.addWidget(self.startup_card, alignment=Qt.AlignTop)

        self.system_setting_label = SubtitleLabel(self)
        self.system_setting_label.setText("其他")
        self.layout.addWidget(self.system_setting_label)

        self.install_nic_card = InstallNicCard()
        self.layout.addWidget(self.install_nic_card, alignment=Qt.AlignTop)

        self.install_broadcast_card = InstallBroadcastCard()
        self.layout.addWidget(self.install_broadcast_card, alignment=Qt.AlignTop)

        self.system_setting_label = SubtitleLabel(self)
        self.system_setting_label.setText("关于")
        self.layout.addWidget(self.system_setting_label)

        self.about_card = AboutCard()
        self.layout.addWidget(self.about_card, alignment=Qt.AlignTop)



class AboutCard(CardWidget):
    """ App card """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FIF.GITHUB)
        self.titleLabel = BodyLabel("关于", self)
        self.contentLabel = CaptionLabel(f"{N2NGUI_COPYRIGHT}, {N2NGUI_AUTHOR}. 当前版本 {N2NGUI_VERSION}", self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(16, 16)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)

        self.hyperlinkButton = HyperlinkButton(
            url='https://github.com/momentforever/N2NGui/releases',
            text='查看最新版',
            parent=self,
            icon=FIF.LINK
        )
        self.hBoxLayout.addWidget(self.hyperlinkButton)



class InstallNicCard(CardWidget):
    """ App card """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FIF.DEVELOPER_TOOLS)
        self.titleLabel = BodyLabel("安装网卡驱动", self)
        self.contentLabel = CaptionLabel("首次安装软件必须安装", self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(16, 16)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)

        self.installButton = PushButton('安装', self)
        self.installButton.setFixedWidth(120)

        self.installButton.clicked.connect(self.install_nic_event)
        self.hBoxLayout.addWidget(self.installButton, 0, Qt.AlignRight)


    def install_nic_event(self):
        Logger().debug("Install Nic Event")
        try:
            InstallTool().install_nic()
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()


class InstallBroadcastCard(CardWidget):
    """ App card """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FIF.DEVELOPER_TOOLS)
        self.titleLabel = BodyLabel("安装广播插件", self)
        self.contentLabel = CaptionLabel("推荐游戏局域网玩家安装", self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(16, 16)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)

        self.installButton = PushButton('安装', self)
        self.installButton.setFixedWidth(120)

        self.installButton.clicked.connect(self.install_broadcast_event)
        self.hBoxLayout.addWidget(self.installButton, 0, Qt.AlignRight)

    def install_broadcast_event(self):
        Logger().debug("Install Broadcast Event")
        try:
            InstallTool().install_broadcast()
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()


class StartUpCard(CardWidget):
    """ App card """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FIF.POWER_BUTTON)
        self.titleLabel = BodyLabel("开机自启动", self)
        self.contentLabel = CaptionLabel("请以管理员身份运行，并确保配置正确！", self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(16, 16)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)

        self.switchButton = SwitchButton(self)
        self.switchButton.setOnText('开')
        self.switchButton.setOffText('关')
        self.switchButton.setChecked(Config().is_auto_startup)

        self.switchButton.move(48, 24)
        self.switchButton.checkedChanged.connect(self.auto_startup_event)

        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)

    def auto_startup_event(self):
        Logger().debug("Auto Startup Event")
        try:
            if self.switchButton.isChecked():
                Logger().info("Open auto startup")
                StartupTool().add_to()
                Config().is_auto_startup = True
            else:
                Logger().info("Close auto startup")
                StartupTool().delete_from()
                Config().is_auto_startup = False
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()
        finally:
            self.switchButton.setChecked(Config().is_auto_startup)
