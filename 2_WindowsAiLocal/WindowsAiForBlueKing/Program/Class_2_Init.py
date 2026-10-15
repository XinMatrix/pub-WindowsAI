import os
import subprocess
import time
from pathlib import Path

import pyautogui
from PIL import Image, ImageDraw, ImageFont


def create_directories(base_dir, sub_dirs):  # 这里不使用log，因为还没有新建文件夹
    desktop_path = Path.home() / "Desktop"
    base_dir_path = desktop_path / base_dir
    if not os.path.exists(base_dir_path):  # 创建基础文件夹
        os.makedirs(base_dir_path)
    for sub_dir in sub_dirs:  # 创建子文件夹
        dir_path = base_dir_path / sub_dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


def _draw_bg_img(path):  # 绘制背景图片
    width, height = pyautogui.size()
    background_color = (64, 64, 64)  # 深灰色
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    text = "WindowsAi"
    font_size = 200
    font_color = (255, 255, 255)  # 白色
    font = ImageFont.truetype("arial.ttf", font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=font_color, font=font)
    image.save(path)


def show_bg():  # 打开背景图像
    img_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Configs\\BG_WindowsAi.png')  # 路径错误，所以打开不对
    time.sleep(1)
    subprocess.Popen(['explorer', img_path])  # 使用explorer打开图片
    time.sleep(3)  # 给几秒让他加载会——因为不确定打开时间——要不要写个程序专门监听——不行，尝试失败
    pyautogui.hotkey('F11')  # 虚拟机没有全屏快捷键，只在最右下角有
