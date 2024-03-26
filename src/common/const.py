"""
常量
"""
import os
import sys


class Status:
    """
    运行状态
    """
    STARTING = 1
    ON = 2
    STOPPING = 3
    OFF = 4
    KILLED = 5
    FAILED = 6

    ENABLE_STOP = [ON]
    ENABLE_START = [OFF, KILLED, FAILED]
    _strs = [
        "off",
        "starting",
        "on",
        "stopping",
        "stopped",
        "killed",
        "failed"
    ]

    @staticmethod
    def to_str(status):
        """
        返回字符串
        """
        return Status._strs[status]


class Path:
    """
    文件路径
    """
    if getattr(sys, 'frozen', False):
        # 返回打包后可执行文件的路径
        EXE_PATH = os.path.realpath(sys.executable)
        WORKER_DIR = os.path.dirname(EXE_PATH)
    else:
        # 返回原始脚本文件的路径
        EXE_PATH = os.path.realpath(__file__)
        WORKER_DIR = os.path.dirname(os.path.dirname(os.path.dirname(EXE_PATH)))
    EDGE_PATH = os.path.join(WORKER_DIR, "tools\\n2n\\edge.exe")
    CONFIG_PATH = os.path.join(WORKER_DIR, "config.yaml")
    LOG_PATH = os.path.join(WORKER_DIR, "N2NGui.log")
    NIC_ZIP_PATH = os.path.join(WORKER_DIR, "tools\\tap-windows.zip")
    NIC_UNZIP_DIR = os.path.join(WORKER_DIR, "tools")
    NIC_PATH = os.path.join(WORKER_DIR, "tools\\tap-windows\\9.21.2.exe")
    BROADCAST_PATH = os.path.join(WORKER_DIR, "tools\\WinIPBroadcast-1.6.exe")

N2NGUI_COPYRIGHT = "Copyright@2023"
N2NGUI_AUTHOR = "moment_forever"
N2NGUI_VERSION = "1.2.0"