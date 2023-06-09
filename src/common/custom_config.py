import configparser
import os

from src.common.custom_exception import CustomException


class CustomConfig:

    _WORKER_DIR = None
    _EXE_SUB_PATH = "N2NGui.exe"
    _EXE_PATH = None
    _EDGE_SUB_PATH = "n2n\\edge.exe"
    _EDGE_PATH = None
    _CONFIG_SUB_PATH = "config.ini"
    _CONFIG_PATH = None
    _LOG_SUB_PATH = "n2n_gui.log"
    _LOG_PATH = None

    DEBUG_LEVEL = "ERROR"
    IS_BOOT_UP = False

    SUPERNODE = None
    EDGE_IP = None
    EDGE_COMMUNITY = None
    EDGE_COMMUNITY_PASSWORD = None
    EDGE_PACKAGE_SIZE = "1386"

    def __init__(self, path):
        self._WORKER_DIR = path
        self._EXE_PATH = os.path.join(self._WORKER_DIR, self._EXE_SUB_PATH)
        self._EDGE_PATH = os.path.join(self._WORKER_DIR, self._EDGE_SUB_PATH)
        self._CONFIG_PATH = os.path.join(self._WORKER_DIR, self._CONFIG_SUB_PATH)
        self._LOG_PATH = os.path.join(self._WORKER_DIR, self._LOG_SUB_PATH)

        if not os.path.exists(self._CONFIG_PATH):
            self.write_to_config()
        self.read_from_config()

    def read_from_config(self):
        self._read_from_config(self._CONFIG_PATH)

    @classmethod
    def _read_from_config(cls, path):
        config = configparser.ConfigParser()
        config.read(path)

        if 'CustomConfig' in config:
            config_section = config['CustomConfig']
            for attr in cls.__dict__:
                if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                    if attr.startswith("IS_"):
                        setattr(cls, attr, config_section.getboolean(attr, getattr(cls, attr)))
                    else:
                        setattr(cls, attr, config_section.get(attr, getattr(cls, attr)))

    def write_to_config(self):
        self._write_to_config(self._CONFIG_PATH)

    @classmethod
    def _write_to_config(cls, path):
        config = configparser.ConfigParser()
        config['CustomConfig'] = {}
        config_section = config['CustomConfig']

        for attr in cls.__dict__:
            if attr.isupper() and not attr.startswith('__') and not attr.startswith('_'):
                config_section[attr] = str(getattr(cls, attr))

        with open(path, 'w') as config_file:
            config.write(config_file)


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
