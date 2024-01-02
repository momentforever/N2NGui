"""
配置文件
"""
import os
import yaml

from src.common.singleton import Singleton
from src.common.const import Path

class Config(metaclass=Singleton):
    """
    配置文件
    """
    def __init__(self):
        self.is_first_start = False
        self.is_auto_startup = False
        self.is_auto_restart = False

        self.supernode = ""
        self.edge_ip = ""
        self.edge_community = ""
        self.edge_community_password = ""
        self.edge_package_size = 1386
        self.edge_description = ""
        self.edge_etc_args = []

        self.load()

    def to_dict(self):
        """
        返回字典类型
        """
        return self.__dict__

    def save(self):
        """
        保存
        """
        yaml_cfg = {}

        for attr_name, attr_value in self.to_dict().items():
            yaml_cfg[attr_name] = attr_value

        with open(Path.CONFIG_PATH, 'w', encoding='utf-8') as yaml_file:
            yaml.safe_dump(yaml_cfg, yaml_file)


    def load(self):
        """
        加载
        """
        if not os.path.exists(Path.CONFIG_PATH):
           # 创建默认配置文件
            self.save()

        with open(Path.CONFIG_PATH, 'r', encoding='utf-8') as yaml_file:
            config_dict = yaml.safe_load(yaml_file)

        for attr_name, attr_value in config_dict.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)
