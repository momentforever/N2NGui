"""
配置文件
"""
from datetime import datetime

import yaml
from typing import List, Dict

from src.common.singleton import Singleton
from src.common.const import Path


class N2NEdgeConfig:
    def __init__(self, **kwargs):
        # self.name: str = kwargs.get('name', "")
        self.supernode: str = kwargs.get("supernode", "")
        self.edge_ip: str = kwargs.get("edge_ip", "")
        self.edge_community: str = kwargs.get("edge_community", "")
        self.edge_community_password: str = kwargs.get("edge_community_password", "")

        self.enable_accept_multi_mac: bool = kwargs.get("enable_accept_multi_mac", False)
        self.enable_package_forwarding: bool = kwargs.get("enable_package_forwarding", False)
        self.edge_package_size: int = kwargs.get("edge_package_size", 1386)
        self.edge_description: str = kwargs.get("edge_description", "")
        # self.encryption_method: int = kwargs.get("encryption_method", 0)
        # self.encryption_key: str = kwargs.get("encryption_key", "")
        self.edge_etc_args: List[str] = kwargs.get("edge_etc_args", [])

    def to_dict(self):
        return self.__dict__


class Config(metaclass=Singleton):
    def __init__(self):
        self.is_first_start = True
        self.is_auto_startup = False
        self.is_force_quit = True

        self.auto_restart_num = 5

        self.cur_n2n_edge_config_index: int = 0
        self.n2n_edge_configs: List[N2NEdgeConfig] = []

        self.load()


    def save(self):
        yaml_cfg = dict()
        yaml_cfg["is_first_start"] = self.is_first_start
        yaml_cfg["is_auto_startup"] = self.is_auto_startup
        yaml_cfg["is_force_quit"] = self.is_force_quit

        yaml_cfg["cur_n2n_edge_config_index"] = self.cur_n2n_edge_config_index
        yaml_cfg["n2n_edge_configs"] = []
        for n2n_edge_config in self.n2n_edge_configs:
            yaml_cfg["n2n_edge_configs"].append(n2n_edge_config.to_dict())

        with open(Path.CONFIG_PATH, 'w', encoding='utf-8') as yaml_file:
            yaml.safe_dump(yaml_cfg, yaml_file)

    def load(self):
        try:
            with open(Path.CONFIG_PATH, 'r', encoding='utf-8') as yaml_file:
                config_dict: Dict = yaml.safe_load(yaml_file)
            if not isinstance(config_dict, Dict):
                raise IOError("config empty")
        except Exception as e:
            # 创建默认配置文件
            self.save()
            with open(Path.CONFIG_PATH, 'r', encoding='utf-8') as yaml_file:
                config_dict: Dict = yaml.safe_load(yaml_file)

        self.is_first_start = config_dict.get("is_first_start", self.is_first_start)
        self.is_auto_startup = config_dict.get("is_auto_startup", self.is_auto_startup)
        self.is_force_quit = config_dict.get("is_force_quit", self.is_force_quit)

        self.cur_n2n_edge_config_index = config_dict.get("cur_n2n_edge_config_index", self.cur_n2n_edge_config_index)
        for n2n_edge_config_dic in config_dict.get("n2n_edge_configs", []):
            self.n2n_edge_configs.append(N2NEdgeConfig(**n2n_edge_config_dic))

    def get_cur_n2n_edge_config(self) -> N2NEdgeConfig:
        try:
            return self.n2n_edge_configs[self.cur_n2n_edge_config_index]
        except Exception as e:
            self.n2n_edge_configs.append(N2NEdgeConfig())
            return self.n2n_edge_configs[self.cur_n2n_edge_config_index]