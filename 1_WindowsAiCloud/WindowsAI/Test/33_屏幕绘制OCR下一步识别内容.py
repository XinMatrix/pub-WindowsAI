import tkinter as tk


# 算了，还是不用全局边框了，直接在目标点绘制一个彩色实矩形，半透明就好了，现在的问题是确定位置
# TODO 编写函数测试实际效果，需要Pos[0],Pos[2]
# FIXME 点不到下面可以给个延迟，延迟后直接消失，再点击
class TransparentWindowWithRectangle(tk.Toplevel):  # 好像必须在画布里才行
    def __init__(self, parent, tmp_box):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)  # 移除窗口边框
        self.attributes('-alpha', 0.6)  # 设置窗口透明度
        width = round(tmp_box[1][0] - tmp_box[0][0])
        height = round(tmp_box[1][1] - tmp_box[0][1])
        self.canvas = tk.Canvas(self, bg='blue', highlightthickness=0, width=width, height=height)  # 创建Canvas，背景设为黑色，无边框
        self.canvas.pack(expand=True, fill='both')
        ave_x = round((tmp_box[0][0] + tmp_box[1][0]) / 2)
        ave_y = round((tmp_box[0][1] + tmp_box[1][1]) / 2)
        self.geometry('+{}+{}'.format(ave_x, ave_y))  # 左上角，这个仅仅是未知


if __name__ == '__main__':
    box = [(100, 120), (300, 200)]  # 左上角到右下角 0 2

    root = tk.Tk()
    root.attributes('-alpha', 0)  # 隐藏主窗口
    rect_window = TransparentWindowWithRectangle(root, box)
    rect_window.attributes('-topmost', True)  # 设置窗口置顶
    root.mainloop()
