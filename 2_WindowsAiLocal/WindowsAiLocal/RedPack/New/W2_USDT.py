import os
import sys
import time
from datetime import datetime

import cv2
import keyboard
import numpy as np
import pyautogui  # 用于模拟点击
from PIL import ImageGrab

# 设定截止日期
expiry_date = datetime(2024, 9, 7)  # 先设置一周
# 获取当前日期
current_date = datetime.now()
# 检查是否超过截止日期
if current_date >= expiry_date:
    raise SystemExit()


def resource_path(relative_path):
    """获取打包后资源文件的正确路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed(self):
        if self.start_time is None or self.end_time is None:
            return "Timer has not been started or stopped."
        return self.end_time - self.start_time

    def reset(self):
        self.start_time = None
        self.end_time = None


def on_hotkey():
    os._exit(0)


# 注册快捷键
keyboard.add_hotkey('ctrl+alt+k', on_hotkey)

# 修改图片，使用延迟，点击之后就暂停点击，延迟三秒
img_1 = cv2.imread(resource_path('11.jpg'))
templates = [img_1]

# _flag = 0

while True:
    # 尝试不同的缩放比例
    timer = Timer()
    timer.start()
    ImageGrab.grab(bbox=(0, 130, 281, 495)).save('screenshot.png')
    large_image = cv2.imread('screenshot.png')

    for template in templates:
        h, w = template.shape[:2]
        for scale in np.linspace(0.5, 2.0, 20)[::-1]:
            resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
            res = cv2.matchTemplate(large_image, resized_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            if len(loc[0]) > 0:
                for pt in zip(*loc[::-1]):
                    # 画出矩形框
                    cv2.rectangle(large_image, pt, (pt[0] + int(w * scale), pt[1] + int(h * scale)), (0, 255, 0), 2)

                    # 计算矩形中心时，使用浮点数进行精确计算
                    center_x = pt[0] + (w * scale) / 2 + 0 - 30  # 加0是因为截图时，窗口的左上角坐标为(0, 130)，减30是因为要点击左侧
                    center_y = pt[1] + (h * scale) / 2 + 130  # 加上130是因为截图时，窗口的左上角坐标为(0, 130)
                    print(f"点击位置：({center_x}, {center_y})")

                    pyautogui.click(center_x, center_y)

                    time.sleep(5)  # 延迟5秒

                    # _flag += 1

                break

    timer.stop()
    print(f"耗时：", timer.elapsed())
    time.sleep(0.05)

    # if _flag == 4:
    #     _flag = 0

# pyinstaller --onefile --add-data "11.jpg;." W2_USDT.py
