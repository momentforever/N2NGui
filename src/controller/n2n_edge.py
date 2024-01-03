from PyQt5.QtWidgets import QMessageBox

from src.common.const import *
from src.common.exception import *
from src.common.logger import Logger
from src.controller.advance_setting import AdvancedSettingController
from src.model.config import Config
from src.model.n2n_edge import N2NEdge
from src.view.n2n_edge import N2NEdgeView


class N2NEdgeController:
    def __init__(self, view: N2NEdgeView):
        # view
        self.view = view

        self.config_model = Config()
        self.n2n_edge_model = N2NEdge()

        # bind
        self.view.run_button.clicked.connect(self.run_n2n_edge_event)
        self.view.advanced_setting_button.clicked.connect(self.show_advance_setting_event)

        self.view.edge_ip_entry.setText(self.config_model.edge_ip)

        self.view.supernode_entry.setText(self.config_model.supernode)

        self.view.edge_community_password_entry.setText(self.config_model.edge_community_password)

        self.view.edge_community_entry.setText(self.config_model.edge_community)

        self.advance_setting_controller = AdvancedSettingController(self.view.advance_setting_view)

    def run_n2n_edge_event(self):
        Logger().debug("run n2n edge event")
        try:
            if self.n2n_edge_model.process_status in Status.ENABLE_START:
                self.config_model.supernode = self.view.supernode_entry.text()
                self.config_model.edge_ip = self.view.edge_ip_entry.text()
                self.config_model.edge_community = self.view.edge_community_entry.text()
                self.config_model.edge_community_password = self.view.edge_community_password_entry.text()
                # 运行程序
                self.n2n_edge_model.start_thread()
                # TODO 设置遮罩
                self.view.run_button.setText("终止")
                self.view.status_signal.emit(Status.ON)

            elif self.n2n_edge_model.process_status in Status.ENABLE_STOP:
                self.n2n_edge_model.stop_thread()
                # TODO 取消遮罩
                self.view.run_button.setText("运行")
                self.view.status_signal.emit(Status.OFF)
            else:
                return
        except N2NGuiException as e:
            QMessageBox.warning(self.view, "错误", e.args[0])
        except Exception as e:
            Logger().error(e)
            QMessageBox.warning(self.view, "错误", "未知错误")

    def show_advance_setting_event(self):
        Logger().debug("show advance setting event")
        self.advance_setting_controller.show_event()
