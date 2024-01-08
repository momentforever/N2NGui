import ctypes
import winreg

from src.common.const import *
from src.common.exception import *
from src.common.logger import Logger
from src.common.singleton import Singleton


class StartupTool(metaclass=Singleton):
    REG_NAME = "N2NGui"
    START_KEY = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            Logger().error(e)
            return False

    def is_exist(self):
        try:
            # 打开注册表项
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 self.START_KEY,
                                 0,
                                 winreg.KEY_READ)

            # 获取注册表项中的所有值名称
            value_names = []
            try:
                i = 0
                while True:
                    value_name = winreg.EnumValue(key, i)[0]
                    value_names.append(value_name)
                    i += 1
            except OSError:
                pass

            # 检查是否存在与您的软件相关的值名称
            if self.REG_NAME in value_names:
                return False
            else:
                return False
        except FileNotFoundError:
            return False

    def add_to(self):
        if not self.is_admin():
            raise N2NGuiException("请以管理员身份运行")

        if self.is_exist():
            return

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 self.START_KEY,
                                 0,
                                 winreg.KEY_ALL_ACCESS)
            Logger().info(f"Add {Path.EXE_PATH} to start up!")
            cmd_str = f'"{Path.EXE_PATH}"'
            winreg.SetValueEx(key, self.REG_NAME, 0, winreg.REG_SZ, cmd_str)  # 将应用程序的路径添加到注册表中
            winreg.CloseKey(key)
        except Exception as e:
            Logger().error(e)
            raise N2NGuiException("注册失败") from e

    def delete_from(self):
        if not self.is_exist():
            return

        try:
            # 打开注册表项
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 self.START_KEY,
                                 0,
                                 winreg.KEY_ALL_ACCESS)

            # 删除与您的软件相关的注册表项
            winreg.DeleteValue(key, self.REG_NAME)
        except FileNotFoundError as e:
            Logger().error(e)