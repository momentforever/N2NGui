import logging
import tkinter as tk
import subprocess
import os

from src.common.custom_config import get_config
from src.common.custom_const import Status
from src.tool.boot_up import add_to_boot_up, delete_from_boot_up
from src.tool.n2n import get_n2n_edge


class GUI:
    supernode_entry = None
    edge_ip_entry = None
    edge_community_entry = None
    edge_community_password_entry = None
    is_boot_up_switch_var = None

    def run(self):
        # 创建主窗口
        window = tk.Tk()
        config = get_config()
        # 超级节点地址和端口
        supernode_label = tk.Label(window, text="超级节点地址和端口：")
        supernode_label.pack()
        self.supernode_entry = tk.Entry(window)
        if config.SUPERNODE:
            self.supernode_entry.insert(0, config.SUPERNODE)
        self.supernode_entry.pack()

        # Edge IP 地址
        edge_ip_label = tk.Label(window, text="Edge IP 地址：")
        edge_ip_label.pack()
        self.edge_ip_entry = tk.Entry(window)
        if config.EDGE_IP:
            self.edge_ip_entry.insert(0, config.EDGE_IP)
        self.edge_ip_entry.pack()

        # Edge Community
        edge_community_label = tk.Label(window, text="小组名称")
        edge_community_label.pack()
        self.edge_community_entry = tk.Entry(window)
        if config.EDGE_COMMUNITY:
            self.edge_community_entry.insert(0, config.EDGE_COMMUNITY)
        self.edge_community_entry.pack()

        # Edge Community Password
        edge_community_password_lab = tk.Label(window, text="小组密码：")
        edge_community_password_lab.pack()
        self.edge_community_password_entry = tk.Entry(window)
        if config.EDGE_COMMUNITY_PASSWORD:
            self.edge_community_password_entry.insert(0, config.EDGE_COMMUNITY_PASSWORD)
        self.edge_community_password_entry.pack()

        # 创建一个变量来保存开关的状态
        self.is_boot_up_switch_var = tk.BooleanVar()
        is_boot_up_switch = tk.Checkbutton(window, text="开机自启动：",
                                           variable=self.is_boot_up_switch_var,
                                           command=self.is_boot_up_event)
        is_boot_up_switch.pack()

        start_button = tk.Button(window, text="启动", command=self.start_edge_event)
        start_button.pack()

        save_button = tk.Button(window, text="保存", command=self.save_config_event)
        save_button.pack()

        # 启动主循环
        window.mainloop()

    def start_edge_event(self):
        n2n_edge = get_n2n_edge()
        config = get_config()
        print("status = {0}".format(n2n_edge.status))
        if n2n_edge.status != Status.ON:
            config.SUPERNODE = self.supernode_entry.get()
            config.EDGE_IP = self.edge_ip_entry.get()
            config.EDGE_COMMUNITY = self.edge_community_entry.get()
            config.EDGE_COMMUNITY_PASSWORD = self.edge_community_entry.get()

            n2n_edge.start_thread()
            config.write_to_config()
        else:
            n2n_edge.stop_thread()

    def save_config_event(self):
        pass

    def is_boot_up_event(self):
        var = self.is_boot_up_switch_var.get()
        try:
            if var:
                add_to_boot_up()
            else:
                delete_from_boot_up()
            config = get_config()
            config.IS_BOOT_UP = var
            config.write_to_config()
        except Exception as e:
            self.is_boot_up_switch_var.set(not var)
