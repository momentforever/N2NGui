import logging
import subprocess
import os
import threading

from src.common.custom_config import get_config, CustomConfig
from src.common.custom_const import Status
from src.common.custom_exception import CustomException


class N2NEdge:
    status: Status = Status.OFF

    _config: CustomConfig = None
    _thread = None
    _process = None

    def __init__(self):
        if self.status not in Status.ENABLE_START:
            raise CustomException("已经启动")

        self.status = Status.OFF
        self._config = get_config()
        self._thread = None
        self._process = None


    def _generate_cmd(self):
        cmd = []
        if not self._config._EDGE_PATH:
            raise CustomException("缺少脚本路径")
        cmd.append(self._config._EDGE_PATH)

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

        logging.debug(cmd)
        return cmd


    def _run(self):
        if self.status not in Status.ENABLE_START:
            raise CustomException("已经启动")

        # 构建 n2n Edge 程序的命令行参数
        edge_cmd = self._generate_cmd()

        self.status = Status.STARTING
        # 启动 n2n Edge 程序，并捕获标准输出
        self._process = subprocess.Popen(edge_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.status = Status.ON
        logging.info("start n2n edge.")
        # TODO 日志监听
        # 监听日志输出
        while self.status == Status.ON:
            # 监控进程异常是否挂掉
            if self._process.poll() is not None:
                self.status = Status.STOPPING
                break

            try:
                output = self._process.stdout.readline().decode("utf-8")  # 解码为字符串
                if output:
                    print(output.strip())  # 输出日志信息，可以根据需要进行处理
            except:
                print("null")

        self._stop()
        return

    def _stop(self):
        try:
            self._process.terminate()  # 终止进程
            self.status = Status.OFF
            logging.info("close n2n edge.")
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


n2n_edge = None


def get_n2n_edge() -> N2NEdge:
    global n2n_edge
    if not n2n_edge:
        raise CustomException("未初始化N2N EDGE")
    return n2n_edge


def init_n2n_edge() -> N2NEdge:
    global n2n_edge
    if not n2n_edge:
        n2n_edge = N2NEdge()
    else:
        n2n_edge.__init__()
    return n2n_edge
