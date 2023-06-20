import logging
import subprocess
import threading
import time

from src.common.custom_config import get_config, CustomConfig
from src.common.custom_const import Status
from src.common.custom_exception import CustomException
from src.common.custom_handler import CustomHandlers
from src.common.custom_logging import get_logging

MAX_RESTART_CNT = 255

# 单例模式
class N2NEdge:
    start_handlers: CustomHandlers = None
    stop_handlers: CustomHandlers = None
    status: Status = Status.OFF
    _config: CustomConfig = None
    _thread = None
    _process = None
    _log_fd = None
    restart_cnt = 0

    def __init__(self):
        if self.status not in Status.ENABLE_START:
            raise CustomException("已经启动")

        self.start_handlers = CustomHandlers()
        self.stop_handlers = CustomHandlers()

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

        if self._config.EDGE_DESCRIPTION:
            cmd.append("-I")
            cmd.append(self._config.EDGE_DESCRIPTION)

        if self._config.EDGE_ETC_ARGS:
            edge_etc_args = self._config.EDGE_ETC_ARGS.split("\n")
            for edge_etc_arg in edge_etc_args:
                edge_etc_arg = edge_etc_arg.split("#")[0]
                if not edge_etc_arg:
                    continue
                cmd += edge_etc_arg.split(" ")

        logging.debug("Start n2n edge command is {0}".format(" ".join(cmd)))
        return cmd

    def _run_process(self):
        if self.status not in Status.ENABLE_START:
            return

        # 构建 n2n Edge 程序的命令行参数
        edge_cmd = self._generate_cmd()
        logging.info("Starting n2n edge...")
        self.status = Status.STARTING
        self.start_handlers.exec()

        while True:
            self._process = subprocess.Popen(edge_cmd,
                                             stdout=self._log_fd,
                                             stderr=self._log_fd,
                                             creationflags=subprocess.CREATE_NO_WINDOW)
            self.status = Status.ON
            logging.info("Start n2n edge!")

            while True:
                # 监控进程异常是否挂掉
                if self._process.poll() is not None:
                    break
                time.sleep(0.1)  # 等待

            if not self._config.IS_UNLESS_STOP:
                self.restart_cnt = 0
                break

            if self.status == Status.KILLED:
                self.restart_cnt = 0
                break

            logging.error(f"Abnormal termination, restart count: {self.restart_cnt}!")

            if self.restart_cnt > MAX_RESTART_CNT:
                logging.critical("Restart error, reaching the upper limit!")
                self.restart_cnt = 0
                break

            self.restart_cnt += 1

        self.stop_handlers.exec()
        self.status = Status.OFF

    def _kill_process(self):
        try:
            logging.info("Killing n2n edge process...")
            self._process.terminate()  # 终止进程
            logging.info("Kill n2n edge process!")
        except Exception as e:
            logging.error(e)
            raise CustomException("停止进程失败")

    def start_thread(self):
        try:
            if self._thread and self._thread.is_alive():
                return

            self._thread = threading.Thread(target=self._run_process)
            self._thread.start()
        except Exception as e:
            logging.error(e)
            raise CustomException("创建线程失败")

    def stop_thread(self):
        if not self._thread or not self._thread.is_alive():
            return

        self.status = Status.KILLED

        if self._process and self._process.poll() is None:
            self._kill_process()

        self._thread.join()


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
