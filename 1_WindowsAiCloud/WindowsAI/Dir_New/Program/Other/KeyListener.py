# 监听按键输出
import threading
import tkinter as tk
from pynput import keyboard


class KeyDisplay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # 去掉窗口装饰
        self.root.geometry("300x50+10+710")  # 窗口大小和位置
        self.root.attributes("-topmost", True)  # 窗口置顶
        self.label = tk.Label(root, text="", font=("Helvetica", 30))
        self.label.pack()

        self.current_keys = set()

        # 按键名称映射
        self.key_mapping = {
            'Key.alt_l': 'ALT',
            'Key.alt_r': 'ALT',
            'Key.ctrl_l': 'CTRL',
            'Key.ctrl_r': 'CTRL',
            'Key.shift': 'SHIFT',
            'Key.shift_l': 'SHIFT',
            'Key.shift_r': 'SHIFT',
            'Key.cmd': 'CMD',
            'Key.cmd_r': 'CMD',
            'Key.space': 'SPACE',
            'Key.enter': 'ENTER',
            'Key.backspace': 'BACKSPACE',
            'Key.tab': 'TAB',
            'Key.esc': 'ESC'
        }

        # 监听按键
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        key_name = self.get_key_name(key)
        self.current_keys.add(key_name)
        self.update_display()

    def on_release(self, key):
        key_name = self.get_key_name(key)
        self.current_keys.discard(key_name)
        self.update_display()

    def get_key_name(self, key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char.upper()
        else:
            return self.key_mapping.get(str(key), str(key))

    def update_display(self):
        # 创建显示的文本，按键之间用加号分隔
        keys_display = '+'.join(sorted(self.current_keys))
        self.label.config(text=keys_display)
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()  # 进入消息循环


def start_key_display():
    root = tk.Tk()
    app = KeyDisplay(root)
    app.run()


if __name__ == '__main__':
    # 调用函数来启动按键显示
    start_key_display()  # 测试时调用，单独进程
