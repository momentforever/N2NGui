import logging
import os.path

from src.common.custom_config import get_config


def init_logging():
    config = get_config()
    if os.path.exists(config.LOG_PATH):

        os.remove(config.LOG_PATH)
    file = open(config.LOG_PATH, mode='a', encoding='utf8')
    logging.basicConfig(level=logging.DEBUG,
                        stream=file,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        encoding='utf8')
