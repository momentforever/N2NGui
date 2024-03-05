from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtWidgets import QVBoxLayout, \
    QWidget, QGridLayout
from qfluentwidgets import LineEdit, TextEdit, BodyLabel, CheckBox, PushButton

from src.tools.config import Config


class AdvancedSettingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config()
        self.n2n_edge_config = self.config.get_cur_n2n_edge_config()

        self.setObjectName("Advanced Setting")

        self.font = QFont()
        self.font.setFamily("微软雅黑")
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.layout = QVBoxLayout(self)
        self.setting_layout = QGridLayout()

        self.package_size_label = BodyLabel(self)
        self.package_size_label.setText("包大小(MTU)")
        self.setting_layout.addWidget(self.package_size_label, 0, 0)
        self.package_size_entry = LineEdit(self)
        self.package_size_entry.setValidator(QIntValidator())
        self.setting_layout.addWidget(self.package_size_entry, 0, 1)

        self.edge_description_label = BodyLabel(self)
        self.edge_description_label.setText("设备描述：")
        self.setting_layout.addWidget(self.edge_description_label, 1, 0)
        self.edge_description_entry = LineEdit(self)
        self.setting_layout.addWidget(self.edge_description_entry, 1, 1)

        self.enable_packet_forwarding_label = BodyLabel(self)
        self.enable_packet_forwarding_label.setText("开启包转发")
        self.setting_layout.addWidget(self.enable_packet_forwarding_label, 2, 0)
        self.enable_packet_forwarding_check_box = CheckBox(self)
        self.setting_layout.addWidget(self.enable_packet_forwarding_check_box, 2, 1)

        self.enable_accept_multi_mac_label = BodyLabel(self)
        self.enable_accept_multi_mac_label.setText("接受多播地址")
        self.setting_layout.addWidget(self.enable_accept_multi_mac_label, 3, 0)
        self.enable_accept_multi_mac_check_box = CheckBox(self)
        self.setting_layout.addWidget(self.enable_accept_multi_mac_check_box, 3, 1)

        self.edge_etc_args_label = BodyLabel(self)
        self.edge_etc_args_label.setText("其他参数(支持#注释)：")
        self.edge_etc_args_entry = TextEdit(self)
        self.setting_layout.addWidget(self.edge_etc_args_label, 4, 0)
        self.setting_layout.addWidget(self.edge_etc_args_entry, 4, 1)

        self.layout.addLayout(self.setting_layout)

        self.load_settings()

    def load_settings(self):
        self.package_size_entry.setText(str(self.n2n_edge_config.edge_package_size))
        self.edge_description_entry.setText(self.n2n_edge_config.edge_description)
        self.edge_etc_args_entry.setText("\n".join(self.n2n_edge_config.edge_etc_args))
        self.enable_packet_forwarding_check_box.setChecked(self.n2n_edge_config.enable_package_forwarding)
        self.enable_accept_multi_mac_check_box.setChecked(self.n2n_edge_config.enable_accept_multi_mac)

    def save_settings(self):
        self.n2n_edge_config.edge_package_size = int(self.package_size_entry.text())
        self.n2n_edge_config.edge_description = self.edge_description_entry.text()
        self.n2n_edge_config.edge_etc_args = self.edge_etc_args_entry.toPlainText().split("\n")
        self.n2n_edge_config.enable_package_forwarding = self.enable_packet_forwarding_check_box.isChecked()
        self.n2n_edge_config.enable_accept_multi_mac = self.enable_accept_multi_mac_check_box.isChecked()
        self.config.save()

    def showEvent(self, a0):
        self.load_settings()

    def leaveEvent(self, a0):
        self.save_settings()
