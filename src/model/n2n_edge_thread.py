import time

from PyQt5.QtCore import QThread, pyqtSignal

from src.common.const import *
from src.tools.n2n_edge_tool import N2NEdgeTool


class N2NEdgeThread(QThread):
    status_signal = pyqtSignal(int)
    n2n_edge = N2NEdgeTool()

    def run(self):
        self._set_status_signal(Status.ON)
        self.n2n_edge.run_process()

    def stop(self):
        self.n2n_edge.terminate_process()
        self.wait()
        self.n2n_edge.process_status = Status.OFF
        self._set_status_signal(Status.OFF)

    def get_status(self):
        return self.n2n_edge.process_status

    def _set_status_signal(self, status):
        self.status_signal.emit(status)
