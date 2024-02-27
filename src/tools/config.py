"""
配置文件
"""
import os
import yaml
from typing import List, Dict

from src.common.singleton import Singleton
from src.common.const import Path


class N2NEdgeConfig:
    def __init__(self, supernode: str = "", edge_ip: str = "",
                 edge_community: str = "", edge_community_password: str = ""
                 ):
        self.supernode: str = supernode
        self.edge_ip: str = edge_ip
        self.edge_community: str = edge_community
        self.edge_community_password: str = edge_community_password

    def to_dict(self):
        return self.__dict__


class Config(metaclass=Singleton):
    def __init__(self):

        self.supernode: str = ""
        self.edge_ip: str = ""
        self.edge_community: str = ""
        self.edge_community_password: str = ""

        self.enable_accept_multi_mac = False
        self.enable_package_forwarding = False
        self.edge_package_size = 1386
        self.edge_description = ""
        self.edge_etc_args = []
        self.is_first_start = True
        self.is_auto_startup = False
        # TODO
        # self.is_auto_restart = False
        # self.max_auto_restart_num = 3

        self.n2n_edge_configs: List[N2NEdgeConfig] = []

        self.load()


    def save(self):
        yaml_cfg = dict()

        yaml_cfg["supernode"] = self.supernode
        yaml_cfg["edge_ip"] = self.edge_ip
        yaml_cfg["edge_community"] = self.edge_community
        yaml_cfg["edge_community_password"] = self.edge_community_password

        yaml_cfg["edge_package_size"] = self.edge_package_size
        yaml_cfg["edge_description"] = self.edge_description
        yaml_cfg["enable_package_forwarding"] = self.enable_package_forwarding
        yaml_cfg["enable_accept_multi_mac"] = self.enable_accept_multi_mac
        yaml_cfg["edge_etc_args"] = self.edge_etc_args
        yaml_cfg["is_first_start"] = self.is_first_start
        yaml_cfg["is_auto_startup"] = self.is_auto_startup

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

        self.supernode = config_dict.get("supernode", self.supernode)
        self.edge_ip = config_dict.get("edge_ip", self.edge_ip)
        self.edge_community = config_dict.get("edge_community", self.edge_community)
        self.edge_community_password = config_dict.get("edge_community_password", self.edge_community_password)

        self.enable_package_forwarding = config_dict.get("enable_package_forwarding", self.enable_package_forwarding)
        self.enable_accept_multi_mac = config_dict.get("enable_accept_multi_mac", self.enable_accept_multi_mac)
        self.edge_package_size = config_dict.get("edge_package_size", self.edge_package_size)
        self.edge_description = config_dict.get("edge_description", self.edge_description)
        self.edge_etc_args = config_dict.get("edge_etc_args", self.edge_etc_args)
        self.is_first_start = config_dict.get("is_first_start", self.is_first_start)
        self.is_auto_startup = config_dict.get("is_auto_startup", self.is_auto_startup)

        for n2n_edge_config_dic in config_dict.get("n2n_edge_configs", []):
            self.n2n_edge_configs.append(N2NEdgeConfig(**n2n_edge_config_dic))
