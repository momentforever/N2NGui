import logging
import subprocess

from src.common.custom_config import get_config
from src.common.custom_exception import CustomException


def install_nic():
    config = get_config()
    try:
        process = subprocess.Popen([config.NIC_PATH],
                                   stderr=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL)

        while True:
            if process.poll() is not None:
                break
    except (PermissionError, WindowsError) as e:
        raise CustomException("权限不足，需管理员权限！")
    except Exception as e:
        logging.error(e)
