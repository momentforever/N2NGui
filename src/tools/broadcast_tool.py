import subprocess
import time
import traceback

from src.common.singleton import Singleton
from src.common.const import *
from src.common.logger import Logger
from src.common.exception import *


# 单例模式
class BroadcastTool(metaclass=Singleton):
    def __init__(self):
        self._process: subprocess.Popen = None

    def run_process(self):
        Logger().info("Starting broadcast...")
        self._process = subprocess.Popen([Path.BROADCAST_PATH, 'run'],
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL,
                                         creationflags=subprocess.CREATE_NO_WINDOW)
        Logger().info("Start broadcast!")

    def terminate_process(self):
        # 未启动
        if not self._process:
            return
        # 已经终止
        if self._process.poll() is not None:
            return
        try:
            Logger().info("Stopping broadcast process...")
            self._process.terminate()
        except Exception as e:
            Logger().error(traceback.format_exc())
            raise N2NGuiException("停止进程失败") from e

    def terminate_process_wait(self):
        # 未启动
        if not self._process:
            return
        # 已经终止
        if self._process.poll() is not None:
            return
        self.terminate_process()
        try:
            self._process.wait(3)
        except subprocess.TimeoutExpired:
            Logger().warning("Abnormal stop broadcast process!")
        Logger().info("Wait until stopping broadcast process finish!")
