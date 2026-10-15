import threading
import time
import tkinter as tk


class TransparentLabel(tk.Toplevel):
    def __init__(self, parent, text):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)
        self.attributes('-alpha', 0.6)  # 设置窗口透明度
        self.label = tk.Label(self, text=text, font=('Arial', 50), fg='white', bg='black')
        self.label.pack(expand=True, fill='both')
        self.update_idletasks()
        self.geometry('+{}+{}'.format(50, self.winfo_screenheight() - self.winfo_height() - 50))  # 屏幕左下角位置
        self.focus_force()  # 将焦点强制移到该窗口上
        self.update()

    def update_text(self, new_text):
        if new_text == "":  # 如果新文本为空，结束程序
            self.destroy()  # 销毁窗口
            return
        self.label.config(text=new_text)


windows_text: TransparentLabel  # 终于明白为什么要放在这里了


def display_data():
    global windows_text
    root = tk.Tk()
    root.attributes('-alpha', 0.0)  # 隐藏主窗口
    label_window = TransparentLabel(root, '初始化')
    label_window.attributes('-topmost', True)  # 设置窗口置顶
    label_window.grab_set()  # 禁止用户选择其他窗口
    root.mainloop()

if __name__ == '__main__':

    global windows_text

    threading.Thread(target=display_data).start()  # 子线程可以控制，不然会阻挡线程

    time.sleep(2)  # 预防未定义

    windows_text.update_text("Step 1")

    time.sleep(1)

    windows_text.update_text("Step 2")

    time.sleep(1)

    windows_text.update_text("Step 3")

    time.sleep(1)

    windows_text.update_text("")  # 这个只能结束显示，不能结束进程
