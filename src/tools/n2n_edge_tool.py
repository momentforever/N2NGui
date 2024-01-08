import signal
import socket
import subprocess
import time

from src.common.singleton import Singleton
from src.common.const import *
from src.tools.config import Config
from src.common.logger import Logger
from src.common.exception import *


# 单例模式
class N2NEdgeTool(metaclass=Singleton):
    def __init__(self):
        self.process_status: Status = Status.OFF
        self._process: subprocess.Popen = None
        self._config: Config = Config()

    def _generate_cmd(self):
        cmd = []
        cmd.append(Path.EDGE_PATH)

        if not self._config.supernode:
            raise N2NGuiException("缺少服务器节点")
        cmd.append("-l")
        cmd.append(str(self._config.supernode))

        if not self._config.edge_community:
            raise N2NGuiException("缺少服务器群组名")
        cmd.append("-c")
        cmd.append(str(self._config.edge_community))

        if self._config.edge_community_password:
            cmd.append("-k")
            cmd.append(str(self._config.edge_community_password))

        if self._config.edge_ip:
            cmd.append("-a")
            cmd.append(str(self._config.edge_ip))

        if self._config.edge_package_size:
            cmd.append("-M")
            cmd.append(str(self._config.edge_package_size))

        if self._config.edge_description:
            cmd.append("-I")
            cmd.append(str(self._config.edge_description))

        if self._config.edge_etc_args:
            for edge_etc_arg in self._config.edge_etc_args:
                if edge_etc_arg.startswith("#"):
                    continue
                cmd += edge_etc_arg

        Logger().info(f'Start n2n edge command is {" ".join(cmd)}')

        return cmd

    @staticmethod
    def _log(msg, *args, **kwargs):
        if len(msg) == 0:
            return
        Logger().info(f"[N2N] {msg}", *args, **kwargs)

    def run_process(self):
        if self.process_status not in Status.ENABLE_START:
            Logger().warning(f"couldn't start n2n edg2, \
                             current status is {Status.to_str(self.process_status)}")
            return

        # 构建 n2n Edge 程序的命令行参数
        edge_cmd = self._generate_cmd()
        Logger().info("Starting n2n edge...")
        self.process_status = Status.STARTING

        self._process = subprocess.Popen(edge_cmd,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         creationflags=subprocess.CREATE_NO_WINDOW)
        self.process_status = Status.ON
        Logger().info("Start n2n edge!")

        while True:
            # 进程终止
            output = self._process.stdout.readline()
            if output == b'' and self._process.poll() is not None:
                break
            self._log(output.decode(encoding='gbk').strip())

            time.sleep(0.1)  # 等待

        self._process.wait()
        Logger().info("Terminate n2n edge process!")
        self._process = None
        self.process_status = Status.STOPPED

    def terminate_process(self):
        # 未启动
        if not self._process:
            return
        # 已经终止
        if self._process.poll() is not None:
            return

        try:
            Logger().info("Terminate n2n edge process...")
            self.process_status = Status.STOPPING
            self._send_stop_package()
            # self._process.terminate()  # 终止进程
        except Exception as e:
            Logger().error(e)
            raise N2NGuiException("停止进程失败") from e

    def terminate_process_wait(self):
        self.terminate_process()
        while True:
            if not self._process:
                break
            if self._process.poll() is not None:
                break
        Logger().info("Process stopped")

    def _send_stop_package(self) -> str:
        result = ""
        try:
            # 创建UDP套接字
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            # 目标主机和端口
            target_host = 'localhost'
            target_port = 5644
            # 要发送的数据
            send_data = b'stop\n'
            # 发送数据包
            sock.sendto(send_data, (target_host, target_port))

            sock.close()
        except Exception as e:
            pass
        finally:
            return result