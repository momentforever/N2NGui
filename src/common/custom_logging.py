import logging
import os.path

from src.common.custom_config import get_config


class CustomLogging:
    path = None
    level = None
    write_fd = None

    def __init__(self):
        config = get_config()
        self.path = config.LOG_PATH
        self.level = config.LOG_LEVEL

        # 重新生成Log
        if self.write_fd:
            self.write_fd.close()

        if os.path.exists(self.path):
            os.remove(self.path)

        self.write_fd = open(self.path, mode='a', encoding='utf8')

        logging.basicConfig(level=logging.getLevelName(config.LOG_LEVEL),
                            stream=self.write_fd,
                            format='[%(asctime)s][%(levelname)s]%(message)s')


global_logging = None


def init_logging() -> CustomLogging:
    global global_logging
    if not global_logging:
        global_logging = CustomLogging()
    else:
        global_logging.__init__()
    return global_logging


def get_logging() -> CustomLogging:
    global global_logging
    return global_logging
