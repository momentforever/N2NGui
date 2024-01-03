from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget
from src.view.advanced_setting import AdvancedSettingView


class N2NEdgeView(QWidget):
    status_signal = pyqtSignal(int)

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

        self.advanced_setting_button = QPushButton("高级设置")
        self.layout.addWidget(self.advanced_setting_button)

        self.advance_setting_view = AdvancedSettingView()
