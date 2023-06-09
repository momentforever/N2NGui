import logging
import winreg
import os
import ctypes

from src.common.custom_config import get_config
from src.common.custom_exception import CustomException

REG_NAME = "N2NGui"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(e)
        return False

def is_exist_in_boot_up():
    startup_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    try:
        # 打开注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_READ)

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
        if REG_NAME in value_names:
            return False
        else:
            return False
    except FileNotFoundError:
        return False

def add_to_boot_up():
    if not is_admin():
        raise CustomException("必须以管理员方式启动")
    startup_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    try:
        if is_exist_in_boot_up():
            raise Exception("无需注册")

        config = get_config()
        # 打开 "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" 注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             startup_key,
                             0,
                             winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_SZ, config.EXE_PATH)  # 将应用程序的路径添加到注册表中
        winreg.CloseKey(key)
    except CustomException as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise CustomException("注册失败")

def delete_from_boot_up():
    startup_key = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    try:
        # 打开注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_ALL_ACCESS)

        # 删除与您的软件相关的注册表项
        winreg.DeleteValue(key, REG_NAME)

    except FileNotFoundError as e:
        logging.error(e)
        return

