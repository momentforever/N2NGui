import time

from PyQt5.QtCore import QThread, pyqtSignal

from src.common.const import *
from src.tools.n2n_edge_tool import N2NEdgeTool


class N2NEdgeThread(QThread):
    status_signal = pyqtSignal(int)
    exception_signal = pyqtSignal(Exception)
    n2n_edge = N2NEdgeTool()

    def run(self):
        self._set_status_signal(Status.ON)
        try:
            self.n2n_edge.run_process()
        except Exception as e:
            self.exception_signal.emit(e)
        self._set_status_signal(Status.OFF)

    def stop(self):
        self.n2n_edge.terminate_process()

    def stop_wait(self):
        self.n2n_edge.terminate_process()
        self.wait(60 * 1000)

    def get_status(self):
        return self.n2n_edge.process_status

    def _set_status_signal(self, status):
        self.status_signal.emit(status)
