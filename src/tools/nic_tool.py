import subprocess
import zipfile

from src.common.const import *
from src.common.exception import *
from src.common.logger import Logger
from src.common.singleton import Singleton


class NicTool(metaclass=Singleton):
    def _unzip_nic(self):
        if os.path.exists(Path.NIC_PATH):
            return

        if not os.path.exists(Path.NIC_ZIP_PATH):
            raise N2NGuiException("未找到网卡驱动压缩包")

        Logger().info(f"Zip Nic Path: {Path.NIC_ZIP_PATH}")
        with zipfile.ZipFile(Path.NIC_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(Path.NIC_UNZIP_DIR)

    def install(self):
        self._unzip_nic()
        try:
            Logger().info(f"Install Nic Path: {Path.NIC_PATH}")
            process = subprocess.Popen([Path.NIC_PATH],
                                       stderr=subprocess.DEVNULL,
                                       stdout=subprocess.DEVNULL,
                                       shell=True)
        except (PermissionError, WindowsError) as e:
            raise N2NGuiException("请以管理员身份运行") from e
        except Exception as e:
            Logger().error(e)
