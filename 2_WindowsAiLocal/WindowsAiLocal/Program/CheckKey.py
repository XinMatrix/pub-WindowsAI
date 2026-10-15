import os
import configparser
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import random
import string
import pandas as pd

from config import get_language

# 隐藏目录路径
HIDDEN_DIR = os.path.expanduser("~/.config")
CONFIG_FILE = os.path.join(HIDDEN_DIR, 'settings.ini')


def initialize_config():
    """初始化配置文件"""
    if not os.path.exists(HIDDEN_DIR):
        os.makedirs(HIDDEN_DIR)
    if not os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config['Settings'] = {'Activated': 'True'}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)


def get_activated_status():
    """获取激活状态"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.getboolean('Settings', 'Activated')


def set_activated_status(status):
    """设置激活状态"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config.set('Settings', 'Activated', str(status))
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def check_key(key, current_date_str):
    def date_to_key(date_str):
        random.seed(date_str)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def key_to_date(key):
        for date in pd.date_range(start="20030403", end="20990403"):
            if date_to_key(date.strftime("%Y%m%d")) == key:
                return date.strftime("%Y%m%d")
        return None

    date_str = key_to_date(key)
    if date_str is None:
        return True, get_language('无效的密钥')

    key_date = datetime.strptime(date_str, "%Y%m%d")
    current_date = datetime.strptime(current_date_str, "%Y%m%d")
    expiration_date = key_date + timedelta(days=3)

    if key_date <= current_date <= expiration_date:
        return False, get_language('密钥有效')
    else:
        return True, get_language('密钥过期')


class KeyCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(get_language('WindowsAi产品验证'))

        # 设置窗口大小和居中显示
        self.root.geometry('400x200')

        # 创建主框架
        main_frame = tk.Frame(root, bg='#2c2c2c', padx=20, pady=20, relief=tk.RIDGE, bd=2)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 创建和放置标签
        self.key_label = tk.Label(main_frame, text=get_language('请输入密钥'), bg='#2c2c2c', fg='white', font=('Arial', 12))
        self.key_label.pack(pady=10)

        # 创建和放置输入框
        self.key_entry = tk.Entry(main_frame, width=30, font=('Arial', 12), bd=2, relief=tk.GROOVE, justify='center',
                                  bg='#BCBCBC')
        self.key_entry.pack(pady=10)

        # 在布局中将输入框中的文本和框架对齐
        self.key_entry.config(justify='center')

        # 创建按钮框架
        button_frame = tk.Frame(main_frame, bg='#ffffff')
        button_frame.pack(pady=10)

        # 创建和放置“粘贴”按钮
        self.paste_button = tk.Button(button_frame, text=get_language('粘贴'), command=self.paste_key, width=12, bg='#4CAF50',
                                      fg='#2c2c2c', font=('Arial', 10))
        # self.paste_button.pack(side=tk.LEFT, padx=5)
        self.paste_button.pack(side=tk.LEFT)

        # 创建和放置“验证”按钮
        self.check_button = tk.Button(button_frame, text=get_language('验证'), command=self.check_key, width=12, bg='#008CBA',
                                      fg='#2c2c2c', font=('Arial', 10))
        self.check_button.pack(side=tk.LEFT)

    def paste_key(self):
        clipboard = self.root.clipboard_get()
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, clipboard)

    def check_key(self):
        key = self.key_entry.get().strip()
        current_date_str = datetime.now().strftime("%Y%m%d")
        is_valid, message = check_key(key, current_date_str)

        if not is_valid:
            set_activated_status(False)  # 设置全局变量为已激活
            messagebox.showinfo(get_language('成功'), get_language('激活成功，请重启软件'))
            self.root.destroy()  # 关闭窗口
        else:
            messagebox.showwarning(get_language('警告'), message)


if __name__ == "__main__":
    initialize_config()  # 初始化配置文件
    check = get_activated_status()  # 如果是True说明已激活，激活返回False，不执行代码
    if check:  # C:\Users\USER/.my_app\settings.ini
        root = tk.Tk()
        KeyCheckerApp(root)
        root.mainloop()

# 27 TQVO7D0hHMernyCNxKxl
# 28 NKlM4FagA1ywyPpXLSeX
