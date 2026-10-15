# 此文件用于测试基本操作函数是否正常运行
import logging

import pyautogui
import requests
from PIL import ImageGrab

from Dir_New.Program.MyFunClass import MyFun
from Dir_New.Program.config import last_img, ocr_url, ocr_acc
from Dir_New.Program.main import start_action

# 定义日志格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='main_output.log',  # 日志输出到的文件
                    filemode='w')  # 发布时日志应该是连续的 'a' 表示追加模式，'w' 表示覆盖模式


def start_item(op):
    ImageGrab.grab().save(last_img, format='JPEG')
    ocr_text, ocr_position = [], []
    ocr_outputs = requests.post(ocr_url, files={'image': open(last_img, 'rb')}, data={'uuid': 'my_uuid'}).json()
    print(ocr_outputs)
    # ocr_outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
    for item in ocr_outputs:
        # ocr_text.append(MyFunction.Input.format_text(item['text'].lower()))  # 一律使用小写，怎么方便怎么来 注意文本过滤
        ocr_text.append(item['text'].lower())  # 一律使用小写，怎么方便怎么来 注意文本过滤
        ocr_position.append(MyFun.Input.average_position(item['position']))
    ocr_accuracy_outputs = requests.post(ocr_acc, files={'image': open(last_img, 'rb')}).json()
    start_action(op, ocr_text, ocr_position, ocr_accuracy_outputs, logging)


if __name__ == '__main__':
    pass
    # MyFun.Input._smooth_move_win32(1000, 500)  # 直接这样测试就好了
    # print(MyFunction.System.set_focus_on_windows('Microsoft Edge')) # Failed
    # start_item('KEY(WIN)')
    # start_item('HOTKEY(WIN+Q)')
    # start_item('CLICK_TEXT(%PASSWORD%)')  # 注意仅能识别完整块文字
    # start_item('CLICK_TEXT_ACCURACY(仅能识别)')  # 注意识别过滤问题
    # start_item('WEB_BROWSER(https://www.google.cn/chrome/index.html)')
    # start_item('OPEN(UserAccountControlSettings.exe)')
    # start_item('CHECK_EXE_EXIST(Google Chrome)')
    # print('A')
    # start_item('SLEEP(3)')
    # print('B')
    # start_item('FUN(GET_WIFI_PASSWORD)')
