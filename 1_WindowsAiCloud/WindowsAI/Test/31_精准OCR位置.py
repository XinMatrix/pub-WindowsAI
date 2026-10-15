# 从OCR得到的数据是一个整体，现在要解决的问题是获取不同文字的位置
import time

import requests
from PIL import ImageGrab

from Dir_Old.Function.MainClass import screenshot_save_path, ocra_url, BaseClass


def click_accuracy_text(t):
    ImageGrab.grab().save(screenshot_save_path, format='JPEG')
    outputs = requests.post(ocra_url, files={'image': open(screenshot_save_path, 'rb')}).json()
    for item in outputs:
        text = item['text']
        pos = item['position']  # 左上 右上 右下 左下
        # y = round(pos[2][1] - pos[0][1])  # 四舍五入
        x = round(pos[2][0] - pos[0][0])
        x_word = round(x / len(text))
        index = text.find(t)
        length = index * x_word
        # TODO 从左上，左下取平均后x向后length个单位
        start_pos = round(pos[0][0]), round((pos[0][1] + pos[3][1]) / 2)
        new_pos = start_pos[0] + length, start_pos[1]
        if index != -1:
            BaseClass.Input._click(new_pos[0], new_pos[1])
            break  # 只检测一个，不继续了


if __name__ == '__main__':
    time.sleep(2)
    click_accuracy_text('单字长度')

    # 原来大于号是能识别到的

    # 这一行是测试文本，我想点击其中的一个文字

    # 原文字
    # 您的下载任务将会自动开始。如果无法正常下载，手动下载Chrom

    # 寄，看来还得看是什么标点
    # 看来还得看大小写字母，统计它的大小，设X和Y吗
    # 看看比例，设x和x+5或x*1.5
    # 可以写个函数计算单字宽度，再做统计

    '''
    # 文本 - 左上 右上 右下 左下 - 高度 - 总长度 - 单字长度 
    这里是标准汉字 # [[512.0, 188.0], [630.0, 188.0], [630.0, 216.0], [512.0, 216.0]] 28 118 16.8
    这里是标准汉 # [[512.0, 216.0], [616.0, 216.0], [616.0, 244.0], [512.0, 244.0]] 28 104 17.3
    这里是标准 # [[512.0, 244.0], [602.0, 244.0], [602.0, 272.0], [512.0, 272.0]] 28 90 18
    这里是标 # [[510.0, 270.0], [584.0, 270.0], [584.0, 300.0], [510.0, 300.0]] 30 74 18.5
    这里是 # [[512.0, 298.0], [568.0, 298.0], [568.0, 327.0], [512.0, 327.0]] 29 56 18.6
    这里 # [[512.0, 327.0], [550.0, 327.0], [550.0, 353.0], [512.0, 353.0]] 26 38 19
    这 # [[510.0, 355.0], [536.0, 355.0], [536.0, 381.0], [510.0, 381.0]] 26 26 26
    '''

    # 先阅读一下官网文档，再看看
    # 尝试通用表格识别
    # 版面分析
    # 甚至自己训练屏幕OCR？——不需要了，有单字的
    # https://github.com/PaddlePaddle/PaddleOCR/blob/main/ppstructure/return_word_pos.md

    # 平均高度27.8

    # TODO 计算每一个字的大小，尽力计算出修正量

    # 为什么误差这么大——误差5点像素以内

    '''
      这里是标准汉字
      这里是标准汉
      这里是标准
      这里是标
      这里是
      这里
      这
      '''
