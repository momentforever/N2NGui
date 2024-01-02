from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, \
    QWidget
from qt_material import apply_stylesheet

from src.model.config import Config
from src.model.n2n_edge import N2NEdge
from src.common.logger import Logger
from src.common.const import *
from src.common.exception import *

class N2NEdgeView(QWidget):
    def __init__(self):
        super().__init__()

        # 应用 Qt-Material 主题
        apply_stylesheet(self, theme='light_cyan_500.xml')

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

        self.advanced_settings_button = QPushButton("高级设置")
        self.layout.addWidget(self.advanced_settings_button)
