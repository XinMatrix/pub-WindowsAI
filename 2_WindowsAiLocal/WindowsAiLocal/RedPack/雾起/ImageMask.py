import os
import time

import keyboard
import pyautogui
from PIL import Image, ImageGrab
import numpy as np
from scipy.ndimage import label


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


def capture_screen(region=None):
    """
    截取屏幕的特定区域。

    :param region: 包含左上和右下角坐标的四元组 (left, top, right, bottom)
    :return: 截图的 PIL.Image 对象
    """
    screenshot = ImageGrab.grab(bbox=region)
    return screenshot


def find_quarter_point_from_screen(target_rgb, tolerance=0.1, region=None):
    """
    查找与目标RGB值接近的区域，计算最大区域下方两点之间从左到右四分之一处的点（基于截屏）。

    :param target_rgb: 目标 RGB 值 (R, G, B)
    :param tolerance: 容差范围（默认10%）
    :param region: 可选，截屏的区域 (left, top, right, bottom)
    :return: bottom_left 和 bottom_right 之间四分之一处的点坐标
    """
    # 获取屏幕截图（可选指定区域）
    screenshot = capture_screen(region=region)

    # 转换图像为像素数组，忽略透明通道 (只使用 RGB)
    img_np = np.array(screenshot)[..., :3]

    # 计算 RGB 的误差范围
    lower_bound = [int(c * (1 - tolerance)) for c in target_rgb]
    upper_bound = [int(c * (1 + tolerance)) for c in target_rgb]

    # 创建二值掩模，忽略透明度通道
    mask = np.all((img_np >= lower_bound) & (img_np <= upper_bound), axis=-1)

    # 寻找连通区域并计算最大连通区域
    labeled_array, num_features = label(mask)
    if num_features == 0:
        return None
    largest_area_index = np.argmax(np.bincount(labeled_array.ravel())[1:]) + 1

    # 获取最大区域的边界框
    largest_region_coords = np.argwhere(labeled_array == largest_area_index)
    top_left = np.min(largest_region_coords, axis=0)  # 最小 y, x
    bottom_right = np.max(largest_region_coords, axis=0)  # 最大 y, x
    bottom_left = (top_left[1], bottom_right[0])  # 左下角

    # 计算 bottom_left 和 bottom_right 之间的四分之一点
    quarter_x = bottom_left[0] + (bottom_right[1] - bottom_left[0]) * 0.25
    quarter_point = (int(quarter_x), bottom_right[0] + 20)

    return quarter_point


def find_quarter_point(image_path, target_rgb, tolerance=0.1):
    """
    查找与目标RGB值接近的区域，计算最大区域下方两点之间从左到右四分之一处的点。

    :param image_path: 本地图像文件路径
    :param target_rgb: 目标 RGB 值 (R, G, B)
    :param tolerance: 容差范围（默认10%）
    :return: bottom_left 和 bottom_right 之间四分之一处的点坐标
    """
    # 读取并转换图像为像素数组，忽略透明通道 (只使用 RGB)
    img_np = np.array(Image.open(image_path))[..., :3]

    # 计算 RGB 的误差范围
    lower_bound = [int(c * (1 - tolerance)) for c in target_rgb]
    upper_bound = [int(c * (1 + tolerance)) for c in target_rgb]

    # 创建二值掩模，忽略透明度通道
    mask = np.all((img_np >= lower_bound) & (img_np <= upper_bound), axis=-1)

    # 寻找连通区域并计算最大连通区域
    labeled_array, num_features = label(mask)
    largest_area_index = np.argmax(np.bincount(labeled_array.ravel())[1:]) + 1

    # 获取最大区域的边界框
    largest_region_coords = np.argwhere(labeled_array == largest_area_index)
    top_left = np.min(largest_region_coords, axis=0)  # 最小 y, x
    bottom_right = np.max(largest_region_coords, axis=0)  # 最大 y, x
    bottom_left = (top_left[1], bottom_right[0])  # 左下角

    # 计算 bottom_left 和 bottom_right 之间的四分之一点
    quarter_x = bottom_left[0] + (bottom_right[1] - bottom_left[0]) * 0.25
    quarter_point = (int(quarter_x), bottom_right[0] + 20)  # 20是阈值

    return quarter_point


def on_hotkey():
    os._exit(0)


def find_quarter_point_from_screen_new(target_rgb, tolerance=0.1, region=None):
    """
    查找与目标RGB值接近的区域，计算第一个匹配区域下方两点之间从左到右四分之一处的点（基于截屏）。

    :param target_rgb: 目标 RGB 值 (R, G, B)
    :param tolerance: 容差范围（默认10%）
    :param region: 可选，截屏的区域 (left, top, right, bottom)
    :return: bottom_left 和 bottom_right 之间四分之一处的点坐标
    """
    # 获取屏幕截图（可选指定区域）
    screenshot = capture_screen(region=region)

    # 转换图像为像素数组，忽略透明通道 (只使用 RGB)
    img_np = np.array(screenshot)[..., :3]

    # 计算 RGB 的误差范围
    lower_bound = [int(c * (1 - tolerance)) for c in target_rgb]
    upper_bound = [int(c * (1 + tolerance)) for c in target_rgb]

    # 创建二值掩模，忽略透明度通道
    mask = np.all((img_np >= lower_bound) & (img_np <= upper_bound), axis=-1)

    # 从下往上逐行扫描，找到第一个匹配的区域
    for y in range(mask.shape[0] - 1, -1, -1):
        row = mask[y, :]
        if np.any(row):
            # 找到第一个匹配区域
            x_coords = np.where(row)[0]
            bottom_left = (x_coords[0], y)
            bottom_right = (x_coords[-1], y)

            # 计算 bottom_left 和 bottom_right 之间的四分之一点
            quarter_x = bottom_left[0] + (bottom_right[0] - bottom_left[0]) * 0.25
            quarter_point = (int(quarter_x), y + 20)  # 20 是阈值

            return quarter_point

    # 如果没有找到匹配的区域，返回 None
    return None


if __name__ == '__main__':
    '''
    # while True:
    # 感觉需要输入标准0,0定位点，然后再进行加减
    rec_timer = Timer()
    rec_timer.start()
    image_path = '1.png'  # 替换为本地图像文件的路径
    # image_path = '2.png'  # 替换为本地图像文件的路径
    target_rgb = (239, 253, 222)  # 输入的目标 RGB 值 —— 金色RGB
    # target_rgb = (35, 46, 59)  # 深色模式
    quarter_point = find_quarter_point(image_path, target_rgb, tolerance=0.1)
    # X从左到右，Y从上到下
    print("bottom_left 和 bottom_right 之间四分之一处的点：", quarter_point)
    # pyautogui.click(quarter_point)
    rec_timer.stop()
    print("运行时间：", rec_timer.elapsed())
    # time.sleep(0.1)  # 等待0.1秒
    '''

    time.sleep(3)

    # 强行停止快捷键 Ctrl+Alt+K
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)

    while True:
        # 感觉需要输入标准0,0定位点，然后再进行加减
        rec_timer = Timer()
        rec_timer.start()
        # target_rgb = (239, 253, 222)  # 输入的目标 RGB 值 —— 金色RGB
        target_rgb = (255, 255, 255)  # 输入的目标 RGB 值 —— 金色RGB
        # target_rgb = (35, 46, 59)  # 深色模式
        # 可选截屏区域，格式为 (left, top, right, bottom)，如果不指定则截全屏
        # quarter_point = find_quarter_point_from_screen(target_rgb, tolerance=0.1, region=(281, 281, 501, 501))
        # 从下往上第一个区域
        quarter_point = find_quarter_point_from_screen_new(target_rgb, tolerance=0.1, region=(281, 281, 501, 501))
        # X从左到右，Y从上到下
        print("bottom_left 和 bottom_right 之间四分之一处20像素下的点：", quarter_point)
        pyautogui.click(quarter_point)
        rec_timer.stop()
        print("运行时间：", rec_timer.elapsed())
        time.sleep(0.1)  # 等待0.1秒
