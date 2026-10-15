import os
import sys
import time
import cv2
import numpy as np
from PIL import ImageGrab


def resource_path(relative_path):
    """获取打包后资源文件的正确路径"""
    try:
        # PyInstaller创建临时文件夹，并将路径存储在_MEIPASS中
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


print('三秒后开始')
time.sleep(3)
print('开始识别')

# while True:
for i in range(10):
    # 尝试不同的缩放比例
    timer = Timer()
    timer.start()
    ImageGrab.grab(bbox=(0, 130, 281, 495)).save('screenshot.png')
    large_image = cv2.imread('screenshot.png')

    # 使用resource_path获取正确的模板路径
    template = cv2.imread(resource_path('3.jpg'))

    h, w = template.shape[:2]
    for scale in np.linspace(0.5, 2.0, 20)[::-1]:
        resized_template = cv2.resize(template, (int(w * scale), int(h * scale)))
        res = cv2.matchTemplate(large_image, resized_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        # 如果找到匹配，则终止循环
        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                cv2.rectangle(large_image, pt, (pt[0] + int(w * scale), pt[1] + int(h * scale)), (0, 255, 0), 2)
            break
    cv2.imwrite(f'result_multi_scale_{i}.png', large_image)
    print(f"多尺度匹配完成，结果已保存为 'result_multi_scale_{i}.png'")
    timer.stop()
    print(f"{i} 耗时：", timer.elapsed())

# pyinstaller --onefile --add-data "3.jpg;." Mix.py
# 浅色系
