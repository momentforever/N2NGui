import ipaddress
import re
import shlex
import signal
import socket
import subprocess
import time
import traceback

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

    def is_valid_ipv4_address(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def _has_illegal_host(self, string):
        if not string:
            return True
        pattern = re.compile(r'[^a-zA-Z0-9:.]')
        match = pattern.search(string)
        if match:
            return True
        else:
            return False

    def _has_illegal_chars(self, string):
        if not string:
            return True
        pattern = re.compile(r'[^a-zA-Z0-9_]')
        match = pattern.search(string)
        if match:
            return True
        else:
            return False

    def _generate_cmd(self):
        cmd = []
        cmd.append(Path.EDGE_PATH)

        if self._has_illegal_host(self._config.supernode):
            raise N2NGuiException("Supernode参数异常")
        cmd.append("-l")
        cmd.append(str(self._config.supernode))

        if self._has_illegal_chars(self._config.edge_community):
            raise N2NGuiException("小组名称参数异常")
        cmd.append("-c")
        cmd.append(str(self._config.edge_community))

        if self._config.edge_community_password:
            if self._has_illegal_chars(self._config.edge_community_password):
                raise N2NGuiException("小组密码参数异常")
            cmd.append("-k")
            cmd.append(str(self._config.edge_community_password))

        if self._config.edge_ip:
            if not self.is_valid_ipv4_address(self._config.edge_ip):
                raise N2NGuiException("Edge地址参数异常")
            cmd.append("-a")
            cmd.append(str(self._config.edge_ip))

        if self._config.edge_package_size:
            if not isinstance(self._config.edge_package_size, int):
                raise N2NGuiException("包大小参数异常")
            cmd.append("-M")
            cmd.append(str(self._config.edge_package_size))

        if self._config.edge_description:
            if self._has_illegal_chars(self._config.edge_description):
                raise N2NGuiException("设备描述参数异常")
            cmd.append("-I")
            cmd.append(str(self._config.edge_description))

        if self._config.enable_package_forwarding:
            cmd.append("-r")

        if self._config.enable_accept_multi_mac:
            cmd.append("-E")

        if self._config.edge_etc_args:
            for edge_etc_arg in self._config.edge_etc_args:
                edge_etc_arg = edge_etc_arg.split("#")[0]
                if len(edge_etc_arg) == 0:
                    continue
                cmd += shlex.split(edge_etc_arg)

        Logger().info(f'Start n2n edge command is {" ".join(cmd)}')

        return cmd

    @staticmethod
    def _log(msg, *args, **kwargs):
        if len(msg) == 0:
            return
        Logger().info(f"[N2N] {msg}", *args, **kwargs)

    def run_process(self):
        if self.process_status not in Status.ENABLE_START:
            Logger().warning(f"Couldn't start n2n edg2, \
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

        self.process_status = Status.OFF
        Logger().info("Stopped n2n edge process!")

    def terminate_process(self):
        # 未启动
        if not self._process:
            return
        # 已经终止
        if self._process.poll() is not None:
            return

        try:
            Logger().info("Stopping n2n edge process...")
            self.process_status = Status.STOPPING
            self._send_stop_package()  # 终止进程
            # self._process.terminate()  # 终止进程
        except Exception as e:
            Logger().error(traceback.format_exc())
            raise N2NGuiException("停止进程失败") from e

    # def terminate_process_wait(self):
    #     # 未启动
    #     if not self._process:
    #         return
    #     # 已经终止
    #     if self._process.poll() is not None:
    #         return
    #     self.terminate_process()
    #     try:
    #         self._process.wait(3)
    #     except subprocess.TimeoutExpired:
    #         Logger().warning("Abnormal stop n2n edge!")
    #     Logger().info("Wait until stopping n2n edge process finish!")

    def _send_stop_package(self):
        # 创建UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 目标主机和端口
        target_host = 'localhost'
        target_port = 5644
        # 要发送的数据
        send_data = b'stop\n'
        # 发送数据包
        sock.sendto(send_data, (target_host, target_port))

        sock.close()
