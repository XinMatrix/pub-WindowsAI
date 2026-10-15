import time
# import function_tkinter as tk
import tkinter as tk
global_root = None

canvas = None
progress = 0
max_progress = 164

x1 = 0
y1 = 0
y2 = 0
width = 0
height = 0


def __start_alpha(root, alpha):  # 持续一秒 更平滑
    root.attributes('-alpha', alpha)
    if alpha < 1:
        alpha += 0.001
        root.after(1, lambda: __start_alpha(root, alpha))


def __end_alpha(root, alpha):
    root.attributes('-alpha', alpha)
    if alpha > 0:
        alpha -= 0.001
        root.after(1, lambda: __end_alpha(root, alpha))


def destroyTK():
    global_root.after(0, lambda: __end_alpha(global_root, 1))
    global_root.after(2000, lambda: global_root.destroy())  # 原来忘记加括号了


# 更新进度条函数
# def __update_progress(value):
#     canvas.coords(progress, x1, y1, x1 + value * 4, y2)


# 平滑加载函数
# def smooth_load(current_value, target_value, step=1):
#     if current_value < target_value:
#         __update_progress(current_value)
#         global_root.after(10, lambda: smooth_load(current_value + step, target_value, step))


text_id = None


def update_text(text):
    time.sleep(1)  # 不给延迟顺序会乱
    global text_id
    global canvas
    if text_id is None:
        text_id = canvas.create_text(width, height + 50, text=text, fill="white", font=("Arial", 20))
    else:
        canvas.itemconfig(text_id, text=text)


def showTK():
    global global_root

    global canvas
    # global progress
    # global x1
    # global y1
    # global y2

    global height
    global width

    root = tk.Tk()
    global_root = root
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.title("WindowsAI")
    root.attributes("-fullscreen", True)  # 创建全屏窗口
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)
    canvas.config(bg='#1e1f22')  # 设置背景色为黑色
    canvas.pack()
    width = screen_width / 2
    height = screen_height / 2

    # 绘制文本——太帅了
    canvas.create_text(width, height - 150, text='WindowsAI', fill="white", font=("Arial", 100))

    # 绘制进度条
    # x1 = width - 325  # 长600
    # y1 = height - 100  # 高20
    # x2 = width + 325
    # y2 = height - 80
    # canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline='#1e1f22')
    # progress = canvas.create_rectangle(x1, y1, 443, y2, fill="green", outline='#1e1f22')  # 442 443 444

    # 这里显示进度信息
    # canvas.create_text(width, height + 50, text='下载QQ', fill="white", font=("Arial", 20))
    # 这里加载进度条
    # smooth_load(0, max_progress)

    # update_text('程序启动中')

    canvas.create_text(width, height + 300, text='请勿操作计算机', fill="white", font=("Arial", 15))

    root.after(0, lambda: __start_alpha(root, 0))  # 5000毫秒后开始透明度渐变

    root.mainloop()


if __name__ == '__main__':
    showTK()


