import io
import re
import time

import numpy as np
import pyautogui
from PIL import Image, ImageGrab
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='ch')

l1 = 'l1.jpg'


def average_position(points):
    sum_x = 0
    sum_y = 0
    for point in points:
        sum_x += point[0]
        sum_y += point[1]
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)
    return avg_x, avg_y


def fuzzy_search(string1, string2):  # str1 == %s%
    if string1.startswith('%') and string1.endswith('%'):  # %s% 表示模糊搜索
        regex_pattern = string1.replace('%', '.*')
    elif string1.startswith('%'):  # %s 表示前置模糊搜索
        regex_pattern = string1.replace('%', '.*') + '$'
    elif string1.endswith('%'):  # s% 表示后置模糊搜索
        regex_pattern = '^' + string1.replace('%', '.*')
    else:  # s 表示原文搜索
        regex_pattern = '^' + string1 + '$'
    return bool(re.search(regex_pattern, string2, re.IGNORECASE))  # 使用正则表达式进行搜索


def start_ocr(ratio=1, min_confidence=0.9):  # 不放大了
    # ImageGrab.grab().save(l1, format='JPEG')
    # 读取图像文件
    # with open(l1, 'rb') as image_file:
    with open('../New/本质.png', 'rb') as image_file:
        image = Image.open(io.BytesIO(image_file.read()))
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)
    temp_result = ocr.ocr(image_np)
    text_info_list = []
    text_list = []
    if not temp_result:  # 如果没有识别到内容
        return text_info_list
    for line in temp_result[0]:
        # 根据缩放比例调整位置
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]
        text = line[1][0]
        confidence = line[1][1]
        if confidence > min_confidence:
            text_list.append(text)
            text_info_list.append({"text": text, "confidence": confidence, "position": box})
    return text_info_list


# def ocr_text_and_click(search_str):
#     results = start_ocr()
#     for item in results:
#         if fuzzy_search(search_str, item['text']):
#             pyautogui.click(average_position(item['position']))
#             return True
#     return False

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


def ocr_text_and_click(search_str):
    results = start_ocr()
    clicked = False
    for item in results:
        if fuzzy_search(search_str, item['text']):
            pyautogui.click(average_position(item['position']))
            clicked = True
    return clicked


if __name__ == '__main__':
    while True:
        timer = Timer()
        timer.start()
        check = ocr_text_and_click('%领取红包%')
        timer.stop()
        if check:
            print(f'领取成功：普通红包，耗时：{timer.elapsed()}秒')

        # 1 - 2.0

    # while True:
    #     check = ocr_text_and_click('%发送了%')
    #     if check:
    #         second_check = ocr_text_and_click('%领取红包%')
    #         if second_check:
    #             print('领取成功：普通红包')

    # 领取红包                  领取红包                领取红包                领取红包                领取红包                领取红包
    # 领取红包                  领取红包                领取红包                领取红包                领取红包                领取红包
    # 领取红包                  领取红包                领取红包                领取红包                领取红包                领取红包

# pyinstaller --onefile --windowed 普通红包.py

# 很多时间耗在OCR上了
