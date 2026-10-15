# 我需要OCR从启动时就开始 并不断输出结果
import os
import subprocess

import requests
from PIL import ImageGrab
from datetime import datetime

ocr_host = '10.103.130.63'
ocr_url = f'http://{ocr_host}:5000/ocr'  # 注意，两个服务应该使用不同的端口


def get_system_id():
    result = subprocess.check_output("wmic csproduct get uuid", shell=True)
    result = result.decode().split('\n')[1].strip()
    return result


def start_ocr(temp_exe_name):
    screen_path = f'log_download_{temp_exe_name}'
    if not os.path.exists(screen_path):
        os.mkdir(screen_path)
    now_time = datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒%f')[:-5]  # 使用毫秒(一位)
    temp_save_path = f'log_download_{temp_exe_name}/{now_time}.jpg'
    # width, height = get_screen_width_height()
    # ImageGrab.grab(bbox=(0, 0, width, height)).save(temp_save_path, format='JPEG')
    ImageGrab.grab(bbox=(0, 0, 1920, 1080)).save(temp_save_path, format='JPEG')
    # return requests.post(global_ocr_url, files={'image': open(temp_save_path, 'rb')}).json()
    return requests.post(ocr_url, files={'image': open(temp_save_path, 'rb')}, data={'uuid': get_system_id()}).json()


if __name__ == '__main__':
    while True:
        temp = start_ocr('test')
        print(temp)
