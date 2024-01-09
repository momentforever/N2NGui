import traceback

from PyQt5.QtWidgets import QVBoxLayout, \
    QWidget
from qfluentwidgets import PushButton, MessageBox, BodyLabel

from src.common.const import Status
from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.tools.n2n_edge_tool import N2NEdgeTool
from src.tools.net_test_tool import NetTestTool
from src.view.tool import Info


class NetTestWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Test")

        self.layout = QVBoxLayout(self)

        self.search_edges_button = PushButton(self)
        self.search_edges_button.setText("测试连接")
        self.search_edges_button.clicked.connect(self.search_edge_event)
        self.layout.addWidget(self.search_edges_button)

        self.info_label = BodyLabel(self)
        self.layout.addWidget(self.info_label)

        self.net_test_tool = NetTestTool()

    def search_edge_event(self):
        try:
            if N2NEdgeTool().process_status != Status.ON:
                info = "未启动服务"
            else:
                edges = self.net_test_tool.get_edges()
                if len(edges) > 0:
                    info = "查询到Edge IP：\n"
                    for edge in edges:
                        info += edge.edge_ip + "\n"
                else:
                    info = "未查询到其他Edge IP"
            self.info_label.setText(info)
        except N2NGuiException as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar(str(e.args[0]), parent=self.parent()).show()
        except Exception as e:
            Logger().error(traceback.format_exc())
            Info.createErrorInfoBar("未知错误，详情请见日志", parent=self.parent()).show()
