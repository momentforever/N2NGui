"""
记录日志
"""

import logging

from src.common.const import Path
from src.common.singleton import Singleton


class Logger(metaclass=Singleton):
    """
    日志模块
    """

    def __init__(self):
        self.logger = logging.getLogger("N2NGui")

        self.logger.setLevel(level=logging.DEBUG)
        format_str = "[%(asctime)s] [%(levelname)s] - %(message)s"
        format_datefmt = '%Y-%m-%d %H:%M:%S'

        handler = logging.FileHandler(Path.LOG_PATH, mode='w', encoding='utf-8')
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(format_str, datefmt=format_datefmt))
        self.logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(format_str, datefmt=format_datefmt))
        self.logger.addHandler(console)

    def get_logger(self):
        """
        获取句柄
        """
        return self.logger

    def debug(self, *args, **kwargs):
        """
        debug
        """
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        """
        info
        """
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """
        warning
        """
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """
        error
        """
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """
        critical
        """
        self.logger.critical(*args, **kwargs)
