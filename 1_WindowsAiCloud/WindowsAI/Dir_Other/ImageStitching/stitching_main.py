# 尝试编写网页自动截屏工具
# 用户输入一个鼠标坐标，即可开始滚动并截取
import glob
import os
from pathlib import Path

import numpy as np
import pyautogui
from PIL import Image
from natsort import natsorted
from sklearn.metrics.pairwise import cosine_similarity


def get_image_files_in_folder(folder_path):
    return glob.glob(os.path.join(folder_path, '*.jpg')) + \
        glob.glob(os.path.join(folder_path, '*.jpeg')) + \
        glob.glob(os.path.join(folder_path, '*.png'))


def _get_img_rows(img):
    image = Image.open(img)
    data = np.array(image)
    return [row.tolist() for row in data]


def mix_images(images):
    # TODO 操作应该是 先拿到一张图片，拿到它的数据，再拿到第二张图片，拿到它的数据，找到匹配的一行，仅保留第二张图中匹配行下面的行，覆盖内容
    # TODO 现在先尝试匹配
    # TODO 应该是原图片下面裁剪吧

    # 很明显，按行匹配不太行，因为它一行中有匹配的也有不匹配的，需要框出一个整体，这才是难点所在

    # sorted_list = natsorted(images)  # 使用 natsorted 进行自然排序
    # for image in sorted_list:
    #     print(image)
    # exit()

    rows = _get_img_rows(images[1])
    rows_new = _get_img_rows(images[2])

    # TODO 连续内容匹配问题
    # 内置OCR？
    # 动态按行记录匹配？
    # 复杂的原因是有且内容是移动的，有些内容是固定的，而且我不确定他们在哪

    for j in rows:
        for index, k in enumerate(rows_new):
            array1 = np.array(j).reshape(1, -1)
            array2 = np.array(k).reshape(1, -1)
            similarity = cosine_similarity(array1, array2)
            print("余弦相似度：", similarity[0][0])  # 相似阈值也不太行呀，这个问题还比较麻烦
            # if j == k:  # 行确实不匹配，部分匹配也行说实话
            #     print(f'Matched in {index} !')
            #     return


def init_dir(directory):
    dir_path = Path(directory)
    for item in dir_path.iterdir():
        item.unlink()


def shot(tmp_i, tmp_y):
    """
       a：截图区域左上角的 x 坐标（水平方向，从屏幕左侧开始计算）
       b：截图区域左上角的 y 坐标（垂直方向，从屏幕顶部开始计算）
       c：截图区域的宽度
       d：截图区域的高度
   """
    a, b, c, d = 0, tmp_y, 1920, 300  # 起点0，终点Y值，宽度1920，高度300
    tmp_screenshot = pyautogui.screenshot(region=(a, b, c, d))
    tmp_screenshot.save(f'outputs/screenshot_{tmp_i}.png')


if __name__ == '__main__':
    image_files = get_image_files_in_folder('outputs')
    mix_images(image_files)
    exit()
    # TODO 滚动画面并横向定域截取，如果两次均相同则认为结束
    # TODO 开始和结束的地方先截整张屏，随后再滑动处理，然后拼合优化导出
    # 用户点击按钮，选定指针位置——估计得使用PyQt
    # 如何监听指针位置
    init_dir('outputs')  # 还是有用的
    # y = 540  # 中间位置
    x, y = 500, 200  # 中间位置
    pyautogui.moveTo(x, y)  # 先指定滑动位置
    # Y应该是不变的吧，变得应该是scroll
    # 初始化第一次完整截屏
    screenshot = pyautogui.screenshot()
    screenshot.save(f'outputs/screenshot_0.png')
    i = 1
    _flag = True
    while _flag:
        time.sleep(0.5)
        pyautogui.scroll(-200)  # -300
        shot(i, y)  # 截图
        # 滑动滚轮
        if i > 1:  # 第二次截图
            last_two_name = f'outputs/screenshot_{i - 1}.png'
            last_name = f'outputs/screenshot_{i}.png'
            image1 = Image.open(last_two_name)
            image2 = Image.open(last_name)
            hash1 = imagehash.average_hash(image1)
            hash2 = imagehash.average_hash(image2)
            if hash1 == hash2:
                _flag = False  # 两次图片完全相同时才置False
        i = i + 1
    # 结束完整截屏
    screenshot.save(f'outputs/screenshot_{i + 1}.png')

    # TODO 导出图片
    image_files = get_image_files_in_folder('outputs')
    mix_images(image_files)
