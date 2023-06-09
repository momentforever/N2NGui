import logging

from src.common.custom_config import get_config


def init_logging():
    config = get_config()
    file = open(config._LOG_PATH, encoding="utf-8", mode="a")
    logging.basicConfig(level=logging.DEBUG,
                        stream=file,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
