import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, \
    QWidget
from src.common.custom_config import get_config
from src.common.custom_const import Status
from src.common.custom_exception import CustomException
from src.tool.n2n_tool import get_n2n_edge


class N2NWindow(QWidget):
    def __init__(self):
        super().__init__()

        n2n_edge = get_n2n_edge()
        config = get_config()

        layout = QVBoxLayout(self)

        supernode_label = QLabel("超级节点地址和端口*：")
        self.supernode_entry = QLineEdit()
        if config.SUPERNODE:
            self.supernode_entry.setText(config.SUPERNODE)
        layout.addWidget(supernode_label)
        layout.addWidget(self.supernode_entry)

        edge_community_label = QLabel("小组名称*：")
        self.edge_community_entry = QLineEdit()
        if config.EDGE_COMMUNITY:
            self.edge_community_entry.setText(config.EDGE_COMMUNITY)
        layout.addWidget(edge_community_label)
        layout.addWidget(self.edge_community_entry)

        edge_community_password_label = QLabel("小组密码：")
        self.edge_community_password_entry = QLineEdit()
        self.edge_community_password_entry.setEchoMode(QLineEdit.Password)
        if config.EDGE_COMMUNITY_PASSWORD:
            self.edge_community_password_entry.setText(config.EDGE_COMMUNITY_PASSWORD)
        layout.addWidget(edge_community_password_label)
        layout.addWidget(self.edge_community_password_entry)

        edge_ip_label = QLabel("Edge IP 地址：")
        self.edge_ip_entry = QLineEdit()
        if config.EDGE_IP:
            self.edge_ip_entry.setText(config.EDGE_IP)
        layout.addWidget(edge_ip_label)
        layout.addWidget(self.edge_ip_entry)

        if n2n_edge.status in Status.ENABLE_START:
            self.start_button = QPushButton("启动")
        else:
            self.start_button = QPushButton("停止")
        n2n_edge.start_handlers.register(self.start_n2n_handler)
        print(len(n2n_edge.start_handlers._handlers))
        n2n_edge.stop_handlers.register(self.stop_n2n_handler)
        print(len(n2n_edge.start_handlers._handlers))

        self.start_button.clicked.connect(self.start_edge_event)
        layout.addWidget(self.start_button)

        self.advanced_settings_button = QPushButton("高级设置")
        self.advanced_settings_button.clicked.connect(self.show_advanced_setting)
        layout.addWidget(self.advanced_settings_button)

    def start_edge_event(self):
        try:
            n2n_edge = get_n2n_edge()
            config = get_config()
            if n2n_edge.status in Status.ENABLE_START:
                config.SUPERNODE = self.supernode_entry.text()
                config.EDGE_IP = self.edge_ip_entry.text()
                config.EDGE_COMMUNITY = self.edge_community_entry.text()
                config.EDGE_COMMUNITY_PASSWORD = self.edge_community_password_entry.text()
                # 先写入配置文件
                config.write_to_config()
                # 在运行程序
                n2n_edge.start_thread()
            else:
                n2n_edge.stop_thread()
        except CustomException as e:
            QMessageBox.information(self, "错误", e.args[0])
        except Exception as e:
            logging.error(e)
            QMessageBox.information(self, "错误", "未知错误")

    def show_advanced_setting(self):
        pass

    def start_n2n_handler(self):
        self.start_button.setText("停止")

    def stop_n2n_handler(self):
        self.start_button.setText("启动")
