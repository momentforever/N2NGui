import tkinter as tk
import threading
import time

from src.common.custom_config import get_config


class LogWindow:
    root = None

    def __init__(self, window):
        self.root = window

        self.text_box = tk.Text(self.root, state=tk.DISABLED)
        self.text_box.pack(fill=tk.BOTH, expand=True)
        config = get_config()
        self.log_file = config.LOG_PATH
        self.is_running = True
        self.worker_thread = threading.Thread(target=self.log_worker)
        self.worker_thread.start()

    def append_log(self, log):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, log + "\n")
        self.text_box.config(state=tk.DISABLED)
        self.text_box.see(tk.END)

    def log_worker(self):
        while self.is_running:
            try:
                with open(self.log_file, "r") as file:
                    file.seek(0, 2)  # 将文件指针移到文件末尾
                    while self.is_running:
                        line = file.readline().strip()
                        if line:
                            self.append_log(line)
                        time.sleep(0.1)  # 等待一段时间再读取文件
            except FileNotFoundError:
                time.sleep(1)  # 如果文件不存在，则等待一段时间再尝试打开文件

    def close(self):
        self.is_running = False
        self.worker_thread.join()
