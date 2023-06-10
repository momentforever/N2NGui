import logging
import sys
import tkinter as tk
import subprocess
import os
from tkinter import messagebox

from src.common.custom_config import get_config
from src.common.custom_const import Status
from src.common.custom_exception import CustomException
from src.gui.log_window import LogWindow
from src.tool.startup_tool import add_to_startup, delete_from_startup
from src.tool.n2n_tool import get_n2n_edge


class GUI:
    window = None
    supernode_entry = None
    edge_ip_entry = None
    edge_community_entry = None
    edge_community_password_entry = None
    is_boot_up_switch_var = None
    log_window = None

    def run(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("N2NGui")

        config = get_config()
        # 超级节点地址和端口
        supernode_label = tk.Label(self.window, text="*超级节点地址和端口：")
        supernode_label.pack()
        self.supernode_entry = tk.Entry(self.window)
        if config.SUPERNODE:
            self.supernode_entry.insert(0, config.SUPERNODE)
        self.supernode_entry.pack()

        # Edge Community
        edge_community_label = tk.Label(self.window, text="*小组名称：")
        edge_community_label.pack()
        self.edge_community_entry = tk.Entry(self.window)
        if config.EDGE_COMMUNITY:
            self.edge_community_entry.insert(0, config.EDGE_COMMUNITY)
        self.edge_community_entry.pack()

        # Edge Community Password
        edge_community_password_lab = tk.Label(self.window, text="小组密码：")
        edge_community_password_lab.pack()
        self.edge_community_password_entry = tk.Entry(self.window, show="*")
        if config.EDGE_COMMUNITY_PASSWORD:
            self.edge_community_password_entry.insert(0, config.EDGE_COMMUNITY_PASSWORD)
        self.edge_community_password_entry.pack()

        # Edge IP 地址
        edge_ip_label = tk.Label(self.window, text="Edge IP 地址：")
        edge_ip_label.pack()
        self.edge_ip_entry = tk.Entry(self.window)
        if config.EDGE_IP:
            self.edge_ip_entry.insert(0, config.EDGE_IP)
        self.edge_ip_entry.pack()

        # 创建一个变量来保存开关的状态
        self.is_boot_up_switch_var = tk.BooleanVar()
        self.is_boot_up_switch_var.set(config.IS_BOOT_UP)
        is_boot_up_switch = tk.Checkbutton(self.window, text="开机自启动：",
                                           variable=self.is_boot_up_switch_var,
                                           command=self.is_boot_up_event)
        is_boot_up_switch.pack()

        start_button = tk.Button(self.window, text="启动", command=self.start_edge_event)
        start_button.pack()

        # 日志窗口
        self.log_window = LogWindow(self.window)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        # 启动主循环
        self.window.mainloop()

    def on_close(self):
        self.log_window.close()
        self.window.destroy()
        sys.exit(0)

    def start_edge_event(self):
        try:
            n2n_edge = get_n2n_edge()
            config = get_config()
            if n2n_edge.status in Status.ENABLE_START:
                config.SUPERNODE = self.supernode_entry.get()
                config.EDGE_IP = self.edge_ip_entry.get()
                config.EDGE_COMMUNITY = self.edge_community_entry.get()
                config.EDGE_COMMUNITY_PASSWORD = self.edge_community_entry.get()

                n2n_edge.start_thread()
                config.write_to_config()
            else:
                n2n_edge.stop_thread()
        except CustomException as e:
            messagebox.showinfo("错误", e.args[0])
        except Exception as e:
            logging.error(e)

    def is_boot_up_event(self):
        is_success = False
        try:
            if self.is_boot_up_switch_var.get():
                add_to_startup()
            else:
                delete_from_startup()
            # 写入配置文件
            config = get_config()
            config.IS_BOOT_UP = self.is_boot_up_switch_var.get()
            config.write_to_config()
            is_success = True
        except CustomException as e:
            messagebox.showinfo("错误", e.args[0])
        except Exception as e:
            logging.error(e)

        if not is_success:
            self.is_boot_up_switch_var.set(not self.is_boot_up_switch_var.get())
