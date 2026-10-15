import os
import re

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

ocr_url = 'http://127.0.0.1:5000/ocr'  # 注意，两个服务应该使用不同的端口
img_src = 'img/sample_6.jpg'
tmp_save_path = 'tmp_result.jpg'


def draw_img_and_save():
    # 打开原始图像
    image = Image.open(img_src)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # 转换为OpenCV格式
    # 使用 PIL 库绘制中文文本
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    # font_path = r'C:\Users\USER\AppData\Local\Microsoft\Windows\Fonts\alimama_dongfangdakai_regular.ttf'
    font_path = r'C:\Users\USER\PycharmProjects\myOCR\src\PaddleOCR_Main\doc\fonts\chinese_cht.ttf'
    font = ImageFont.truetype(font_path, size=16)  # 指定中文字体和大小
    # 遍历识别结果并在图像上绘制文本和识别框
    for tmp_item in outputs:
        tmp_text = tmp_item['text'].lower()
        tmp_text = remove_punctuation(tmp_text)
        position = tmp_item['position']
        # 计算文本位置（取识别框左上角）
        text_offset = 20
        x, y = position[0][0], position[0][1] + text_offset
        # 在图像上绘制文本
        draw.text((x, y), tmp_text, fill=(0, 0, 0), font=font)
    # 转换回OpenCV格式图像
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    # 保存图像到本地
    cv2.imwrite(tmp_save_path, image)
    # 使用系统默认的图像查看器打开保存的图像
    os.system(tmp_save_path)


def remove_punctuation(string):  # 标准统一即可
    # 使用正则表达式去除标点符号
    # 标点符号包括：英文标点符号、中文标点符号、空白字符
    # 注意：中文标点符号并不是所有的都在 \pP 中，可能需要根据需要添加
    # 如果需要保留空格，可以将 \s 去掉
    pattern = re.compile("[^\u4e00-\u9fa5^a-zA-Z0-9]")
    return pattern.sub('', string)


if __name__ == '__main__':
    text_list = []
    outputs = requests.post(ocr_url, files={'image': open(img_src, 'rb')}).json()
    for item in outputs:
        text = item['text'].lower()
        new_text = remove_punctuation(text)
        text_list.append(f'{new_text}_')
    without_last_character = ''.join(text_list)[:-1]  # 连接字符串
    print(without_last_character)
    draw_img_and_save()
