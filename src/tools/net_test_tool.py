import subprocess
import socket
from typing import List

from src.common.exception import N2NGuiException
from src.common.logger import Logger
from src.common.singleton import Singleton


class NetConfig:
    def __init__(self):
        self.edge_ip = ""
        self.ip_port = ""
        self.mac = ""

class NetTestTool(metaclass=Singleton):
    def _get_udp_package(self) -> str:
        result = ""
        try:
            # 创建UDP套接字
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            # 目标主机和端口
            target_host = 'localhost'
            target_port = 5644
            # 要发送的数据
            send_data = b'\n'
            # 发送数据包
            sock.sendto(send_data, (target_host, target_port))
            # 循环接收数据
            num_packets = 10  # 要接收的数据包数量
            for _ in range(num_packets):
                data, addr = sock.recvfrom(1024)
                result += data.decode()
            # 关闭套接字
            sock.close()
        except Exception as e:
            pass
        finally:
            return result

    def get_edges(self) -> List[NetConfig]:
        data = self._get_udp_package()
        if not data:
            raise N2NGuiException("无法访问监听端口")
        Logger().info(f"Recv data: {data}")
        data = data.split("\n")
        is_find_edge = False
        edges = []
        for line in data:
            if line.find("PEER TO PEER"):
                is_find_edge = True
            elif is_find_edge is True and line.find("---"):
                is_find_edge = False
            elif is_find_edge is True:
                tags = line.split("|")
                nc = NetConfig()
                nc.edge_ip = tags[1].strip()
                nc.mac = tags[2].strip()
                nc.ip_port = tags[3].strip()
                edges.append(nc)

        return edges
