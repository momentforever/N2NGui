import logging
import subprocess
import threading
import time

from src.common.custom_config import get_config, CustomConfig
from src.common.custom_const import Status
from src.common.custom_exception import CustomException
from src.common.custom_logging import get_logging


class N2NEdge:
    status: Status = Status.OFF

    _config: CustomConfig = None
    _thread = None
    _process = None
    _log_fd = None

    def __init__(self):
        if self.status not in Status.ENABLE_START:
            raise CustomException("已经启动")

        self.status = Status.OFF
        self._config = get_config()
        if not self._log_fd:
            self._log_fd = get_logging().write_fd
        self._thread = None
        self._process = None


    def _generate_cmd(self):
        cmd = []
        if not self._config.EDGE_PATH:
            raise CustomException("缺少脚本路径")
        cmd.append(self._config.EDGE_PATH)

        if not self._config.SUPERNODE:
            raise CustomException("缺少服务器节点")
        cmd.append("-l")
        cmd.append(self._config.SUPERNODE)

        if not self._config.EDGE_COMMUNITY:
            raise CustomException("缺少服务器群组名")
        cmd.append("-c")
        cmd.append(self._config.EDGE_COMMUNITY)

        if self._config.EDGE_COMMUNITY_PASSWORD:
            cmd.append("-k")
            cmd.append(self._config.EDGE_COMMUNITY_PASSWORD)

        if self._config.EDGE_IP:
            cmd.append("-a")
            cmd.append(self._config.EDGE_IP)

        if self._config.EDGE_PACKAGE_SIZE:
            cmd.append("-M")
            cmd.append(self._config.EDGE_PACKAGE_SIZE)

        logging.debug("Start n2n edge command is {0}".format(" ".join(cmd)))
        return cmd


    def _run(self):
        if self.status not in Status.ENABLE_START:
            return

        # 构建 n2n Edge 程序的命令行参数
        edge_cmd = self._generate_cmd()
        logging.info("Starting n2n edge...")
        self.status = Status.STARTING
        self._process = subprocess.Popen(edge_cmd,
                                         stdout=self._log_fd,
                                         stderr=self._log_fd,
                                         creationflags=subprocess.CREATE_NO_WINDOW)

        self.status = Status.ON
        logging.info("Start n2n edge!")
        # TODO 日志监听
        # 监听日志输出
        while self.status == Status.ON:
            # 监控进程异常是否挂掉
            if self._process.poll() is not None:
                self.status = Status.STOPPING
                break
            time.sleep(0.1)  # Wait for some time before reading the file

        self._stop()
        return

    def _stop(self):
        try:
            logging.info("Closing n2n edge...")
            self._process.terminate()  # 终止进程
            self.status = Status.OFF
            logging.info("Close n2n edge!")
        except Exception as e:
            logging.error(e)
            raise CustomException("停止进程失败")

    def start_thread(self):
        try:
            self._thread = threading.Thread(target=self._run)
            self._thread.start()
        except Exception as e:
            logging.error(e)
            raise CustomException("创建线程失败")

    def stop_thread(self):
        if not self._thread.is_alive():
            raise CustomException("线程已被关闭")
        if self.status == Status.STOPPING:
            self._stop()
            return

        self.status = Status.STOPPING


global_n2n_edge = None


def get_n2n_edge() -> N2NEdge:
    global global_n2n_edge
    if not global_n2n_edge:
        raise CustomException("未初始化N2N EDGE")
    return global_n2n_edge


def init_n2n_edge() -> N2NEdge:
    global global_n2n_edge
    if not global_n2n_edge:
        global_n2n_edge = N2NEdge()
    else:
        global_n2n_edge.__init__()
    return global_n2n_edge
