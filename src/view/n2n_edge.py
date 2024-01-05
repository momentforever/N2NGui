from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QMessageBox

from src.common.const import Status
from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.model.n2n_edge_thread import N2NEdgeThread
from src.tools.config import Config
from src.view.advanced_setting import AdvancedSettingView


class N2NEdgeView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.supernode_label = QLabel("超级节点地址和端口*：")
        self.supernode_entry = QLineEdit()
        self.layout.addWidget(self.supernode_label)
        self.layout.addWidget(self.supernode_entry)

        self.edge_community_label = QLabel("小组名称*：")
        self.edge_community_entry = QLineEdit()
        self.layout.addWidget(self.edge_community_label)
        self.layout.addWidget(self.edge_community_entry)

        self.edge_community_password_label = QLabel("小组密码：")
        self.edge_community_password_entry = QLineEdit()
        self.edge_community_password_entry.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.edge_community_password_label)
        self.layout.addWidget(self.edge_community_password_entry)

        self.edge_ip_label = QLabel("Edge IP 地址：")
        self.edge_ip_entry = QLineEdit()
        self.layout.addWidget(self.edge_ip_label)
        self.layout.addWidget(self.edge_ip_entry)

        self.run_button = QPushButton("运行")
        self.layout.addWidget(self.run_button)

        self.config_model = Config()
        self.n2n_edge_model = N2NEdgeThread()
        self.n2n_edge_model.status_signal.connect(self.update_status)

        # bind
        self.run_button.clicked.connect(self.run_n2n_edge_event)

        self.edge_ip_entry.setText(self.config_model.edge_ip)
        self.supernode_entry.setText(self.config_model.supernode)
        self.edge_community_password_entry.setText(self.config_model.edge_community_password)
        self.edge_community_entry.setText(self.config_model.edge_community)


    def update_status(self, status):
        if status == Status.ON:
            # TODO 设置遮罩
            self.run_button.setText("终止")
        elif status == Status.OFF:
            self.run_button.setText("运行")

    def run_n2n_edge_event(self):
        Logger().debug("run n2n edge event")
        try:
            if self.n2n_edge_model.get_status() in Status.ENABLE_START:
                self.config_model.supernode = self.supernode_entry.text()
                self.config_model.edge_ip = self.edge_ip_entry.text()
                self.config_model.edge_community = self.edge_community_entry.text()
                self.config_model.edge_community_password = self.edge_community_password_entry.text()
                # 运行程序
                self.n2n_edge_model.start()
            elif self.n2n_edge_model.get_status() in Status.ENABLE_STOP:
                self.n2n_edge_model.stop()
            else:
                Logger().warning(f"couldn't operate N2N edge, "
                                 f"current status: {Status.to_str(self.n2n_edge_model.get_status())}")

        except N2NGuiException as e:
            QMessageBox.warning(self, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self, "错误", "未知错误")

