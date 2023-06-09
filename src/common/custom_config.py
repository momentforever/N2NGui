import os

from src.common.custom_exception import CustomException
from src.common.custom_json_config import CustomJSONConfig


# 单例模式
class CustomConfig(CustomJSONConfig):
    WORKER_DIR = None
    EXE_SUB_PATH = "N2NGui.exe"
    EXE_PATH = None
    EDGE_SUB_PATH = "n2n\\edge.exe"
    EDGE_PATH = None
    NIC_SUB_PATH = "tools\\tap-windows\\9.21.2.exe"
    NIC_PATH = None
    CONFIG_SUB_PATH = "config.json"
    CONFIG_PATH = None
    LOG_SUB_PATH = "N2NGui.log"
    LOG_PATH = None

    def __init__(self, path):
        self.WORKER_DIR = path
        self.EXE_PATH = os.path.join(self.WORKER_DIR, self.EXE_SUB_PATH)
        self.EDGE_PATH = os.path.join(self.WORKER_DIR, self.EDGE_SUB_PATH)
        self.CONFIG_PATH = os.path.join(self.WORKER_DIR, self.CONFIG_SUB_PATH)
        self.LOG_PATH = os.path.join(self.WORKER_DIR, self.LOG_SUB_PATH)
        self.NIC_PATH = os.path.join(self.WORKER_DIR, self.NIC_SUB_PATH)
        super().__init__(self.CONFIG_PATH)

    def read_from_config(self):
        self._read_from_config(self.CONFIG_PATH)

    def write_to_config(self):
        self._write_to_config(self.CONFIG_PATH)


global_config = None


def init_config(path) -> CustomConfig:
    global global_config
    if not global_config:
        global_config = CustomConfig(path)
    else:
        global_config.__init__(path)
    return global_config


def get_config() -> CustomConfig:
    global global_config
    if not global_config:
        raise CustomException("未生成配置文件")
    return global_config
