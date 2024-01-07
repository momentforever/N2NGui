from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QMessageBox, QCompleter, QHBoxLayout, QSizePolicy
from qfluentwidgets import LineEdit, PushButton, MessageBox, TextEdit

from src.common.const import Status
from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.model.log_monitor_thread import LogMonitorThread
from src.model.n2n_edge_thread import N2NEdgeThread
from src.tools.config import Config


class HomeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Home")

        self.layout = QHBoxLayout(self)
        self.n2n_edge_view = N2NEdgeWidget(parent=self.parent())
        self.layout.addWidget(self.n2n_edge_view, 2)
        self.log_monitor_view = LogMonitorWidget(parent=self.parent())
        self.layout.addWidget(self.log_monitor_view, 5)


class N2NEdgeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font = QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.layout = QVBoxLayout(self)

        self.supernode_label = QLabel("超级节点地址和端口：")
        self.supernode_label.setFont(self.font)
        self.supernode_entry = LineEdit()
        self.supernode_entry.setPlaceholderText("必填")
        self.layout.addWidget(self.supernode_label)
        self.layout.addWidget(self.supernode_entry)

        self.edge_community_label = QLabel("小组名称：")
        self.edge_community_entry = LineEdit()
        self.edge_community_entry.setPlaceholderText("必填")
        self.layout.addWidget(self.edge_community_label)
        self.layout.addWidget(self.edge_community_entry)

        self.edge_community_password_label = QLabel("小组密码：")
        self.edge_community_password_entry = LineEdit()
        self.edge_community_password_entry.setPlaceholderText("必填")
        self.edge_community_password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.edge_community_password_label)
        self.layout.addWidget(self.edge_community_password_entry)

        self.edge_ip_label = QLabel("Edge IP 地址：")
        self.edge_ip_entry = LineEdit()
        self.layout.addWidget(self.edge_ip_label)
        self.layout.addWidget(self.edge_ip_entry)

        self.run_button = PushButton("运行")
        self.layout.addWidget(self.run_button)

        self.config = Config()
        self.n2n_edge = N2NEdgeThread()

        self.n2n_edge.status_signal.connect(self.update_status)

        # bind
        self.run_button.clicked.connect(self.run_n2n_edge_event)

        self.supernode_entry.setText(self.config.supernode)
        self.edge_community_password_entry.setText(self.config.edge_community_password)
        self.edge_community_entry.setText(self.config.edge_community)
        self.edge_ip_entry.setText(self.config.edge_ip)
        MessageBox("错误", "test", parent=self.parent())
        if self.config.is_auto_startup:
            self.run_n2n_edge_event()

    def update_status(self, status):
        if status == Status.ON:
            self.supernode_entry.setEnabled(False)
            self.edge_community_password_entry.setEnabled(False)
            self.edge_community_entry.setEnabled(False)
            self.edge_ip_entry.setEnabled(False)
            self.run_button.setText("终止")
        elif status == Status.OFF:
            self.supernode_entry.setEnabled(True)
            self.edge_community_password_entry.setEnabled(True)
            self.edge_community_entry.setEnabled(True)
            self.edge_ip_entry.setEnabled(True)
            self.run_button.setText("运行")

    def run_n2n_edge_event(self):
        Logger().debug("run n2n edge event")
        try:
            if self.n2n_edge.get_status() in Status.ENABLE_START:
                self.config.supernode = self.supernode_entry.text()
                self.config.edge_ip = self.edge_ip_entry.text()
                self.config.edge_community = self.edge_community_entry.text()
                self.config.edge_community_password = self.edge_community_password_entry.text()
                # 运行程序
                self.n2n_edge.start()
            elif self.n2n_edge.get_status() in Status.ENABLE_STOP:
                self.n2n_edge.stop()
            else:
                Logger().warning(f"couldn't operate N2N edge, "
                                 f"current status: {Status.to_str(self.n2n_edge.get_status())}")

        except N2NGuiException as e:
            MessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            MessageBox.warning(self, "错误", "未知错误")


class LogMonitorWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout(self)

        self.text_box = TextEdit(self)
        self.text_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        self.resize(self.sizeHint())

        self.log_monitor_thread = LogMonitorThread()
        self.log_monitor_thread.update_signal.connect(self.append_log)
        self.log_monitor_thread.start()

    def append_log(self, log: str):
        self.text_box.append(log)
        self.text_box.moveCursor(self.text_box.textCursor().End)
