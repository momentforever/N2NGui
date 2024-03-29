import traceback

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, \
    QWidget, QHBoxLayout, QSizePolicy
from qfluentwidgets import LineEdit, PushButton, MessageBox, TextEdit, StrongBodyLabel, BodyLabel, InfoBar, InfoBarIcon, \
    InfoBarPosition

from src.common.const import Status
from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.model.log_monitor_thread import LogMonitorThread
from src.model.n2n_edge_thread import N2NEdgeThread
from src.tools.config import Config
from src.view.tool import Info


class HomeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Home")

        self.layout = QHBoxLayout(self)
        self.n2n_edge_widget = N2NEdgeWidget(parent=self.parent())
        self.layout.addWidget(self.n2n_edge_widget, 1)
        self.log_monitor_widget = LogMonitorWidget(parent=self.parent())
        self.layout.addWidget(self.log_monitor_widget, 2)


class N2NEdgeWidget(QWidget):
    n2n_edge_status_signal = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config()
        self.n2n_edge_config = self.config.get_cur_n2n_edge_config()

        self.font = QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.layout = QVBoxLayout(self)

        self.supernode_label = StrongBodyLabel(self)
        self.supernode_label.setText("Supernode地址和端口：")
        self.supernode_entry = LineEdit(self)
        self.supernode_entry.setPlaceholderText("必填")
        self.supernode_entry.setText(self.n2n_edge_config.supernode)
        self.layout.addWidget(self.supernode_label)
        self.layout.addWidget(self.supernode_entry)

        self.edge_community_label = StrongBodyLabel(self)
        self.edge_community_label.setText("小组名称：")
        self.edge_community_entry = LineEdit(self)
        self.edge_community_entry.setPlaceholderText("必填")
        self.edge_community_entry.setText(self.n2n_edge_config.edge_community)
        self.layout.addWidget(self.edge_community_label)
        self.layout.addWidget(self.edge_community_entry)

        self.edge_community_password_label = BodyLabel(self)
        self.edge_community_password_label.setText("小组密码：")
        self.edge_community_password_entry = LineEdit(self)
        self.edge_community_password_entry.setEchoMode(QLineEdit.Password)
        self.edge_community_password_entry.setText(self.n2n_edge_config.edge_community_password)
        self.layout.addWidget(self.edge_community_password_label)
        self.layout.addWidget(self.edge_community_password_entry)

        self.edge_ip_label = BodyLabel(self)
        self.edge_ip_label.setText("Edge地址：")
        self.edge_ip_entry = LineEdit(self)
        self.edge_ip_entry.setText(self.n2n_edge_config.edge_ip)
        self.layout.addWidget(self.edge_ip_label)
        self.layout.addWidget(self.edge_ip_entry)

        self.run_button = PushButton(self)
        self.run_button.setText("运行")
        self.run_button.clicked.connect(self.run_n2n_edge_event)
        self.layout.addWidget(self.run_button)

        self.n2n_edge_thread = N2NEdgeThread(self)
        # self.n2n_edge_thread = N2NEdgeThread()
        self.n2n_edge_thread.status_signal.connect(self.update_status_handler)
        self.n2n_edge_thread.exception_signal.connect(self.edge_exception_handler)
        if self.config.is_auto_startup:
            self.run_n2n_edge_event()

    def edge_exception_handler(self, e):
        try:
            raise e
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()

    def update_status_handler(self, status):
        self.n2n_edge_status_signal.emit(status)
        if status == Status.ON:
            self.supernode_entry.setEnabled(False)
            self.edge_community_password_entry.setEnabled(False)
            self.edge_community_entry.setEnabled(False)
            self.edge_ip_entry.setEnabled(False)
            self.run_button.setEnabled(True)
            self.run_button.setText("终止")
        elif status == Status.OFF:
            self.supernode_entry.setEnabled(True)
            self.edge_community_password_entry.setEnabled(True)
            self.edge_community_entry.setEnabled(True)
            self.edge_ip_entry.setEnabled(True)
            self.run_button.setEnabled(True)
            self.run_button.setText("运行")

    def save_config(self):
        self.n2n_edge_config.supernode = self.supernode_entry.text()
        self.n2n_edge_config.edge_ip = self.edge_ip_entry.text()
        self.n2n_edge_config.edge_community = self.edge_community_entry.text()
        self.n2n_edge_config.edge_community_password = self.edge_community_password_entry.text()
        self.config.save()

    def run_n2n_edge_event(self):
        Logger().debug("Run N2N Edge Event")
        if self.n2n_edge_thread.get_status() in Status.ENABLE_START:
            self.save_config()
            self.run_button.setEnabled(False)
            # 非阻塞运行程序
            self.n2n_edge_thread.start()
        elif self.n2n_edge_thread.get_status() in Status.ENABLE_STOP:
            # 阻止用户多次操作
            self.run_button.setEnabled(False)
            # 非阻塞终止程序
            self.n2n_edge_thread.stop()

    def leaveEvent(self, a0):
        self.save_config()


class LogMonitorWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout(self)

        self.text_box = TextEdit(self)
        self.text_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.resize(self.sizeHint())

        self.log_monitor_thread = LogMonitorThread(self)
        # self.log_monitor_thread = LogMonitorThread()
        self.log_monitor_thread.update_signal.connect(self.append_log)
        self.log_monitor_thread.start()

    def append_log(self, log: str):
        self.text_box.append(log)
        self.text_box.moveCursor(self.text_box.textCursor().End)
