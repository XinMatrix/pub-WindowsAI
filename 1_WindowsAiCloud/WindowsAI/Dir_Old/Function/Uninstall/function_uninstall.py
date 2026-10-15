# 卸载程序
import datetime
import os
import shutil
import subprocess
import time
import cv2
import numpy as np
import pyautogui
import pyperclip
import requests
import yaml
from PIL import ImageGrab
from ultralytics import YOLO

delay = 0.8
global_exe_name = ''
screen_path = 'log'

create_path = ''
yolo_model = YOLO(r'/TrainModel/model_uninstall/best.onnx', task='detect')  # 模型加载有点慢
yaml_data = []

last_img_path = ''  # 用于与上一张图片对比
last_img_data = ''  # OCR信息


class RecText:  # 1
    def __init__(self, text, operation, direction='center'):  # 必须传入文字与操作，方向可选
        self.text = text
        self.operation = operation
        self.direction = direction


class ClickImgStrong:  # 1
    def __init__(self, operation, args):  # 必须传入函数名称与参数
        self.operation = operation
        self.args = args


class ClickImgWeek:  # 1
    def __init__(self, operation, args):  # 必须传入函数名称与参数
        self.operation = operation
        self.args = args


# 计算两张图片差异，如输出10表示较为相似，仅有10%差异
# 主要针对YOLO与OCR，降低检测频率，提高效率
def cal_img_differ(old_img, new_img):
    image1 = cv2.imread(old_img)
    image2 = cv2.imread(new_img)
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray_image1, gray_image2)
    different_pixels = np.count_nonzero(diff)
    total_pixels = gray_image1.shape[0] * gray_image1.shape[1]
    return (different_pixels / total_pixels) * 100


def check_exe_exists():
    pyautogui.hotkey('Win', 'q')
    time.sleep(delay)
    pyperclip.copy(global_exe_name)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')  # 清空剪切板
    time.sleep(delay * 3)
    results, _, _ = get_ocr()
    temp = []
    for text_info in results:
        temp.append(text_info['text'])
    pyautogui.hotkey('esc')
    if '卸载' not in temp:
        raise FileNotFoundError('程序不存在，无法卸载！')


def open_installed_application():
    time.sleep(delay)
    pyautogui.hotkey('win', 'x')
    time.sleep(delay)
    pyautogui.hotkey('p')
    time.sleep(delay)


def find_icon(lst):  # small是我要找的东西 large是截屏
    small = lst[0]
    large = lst[1]
    large_image = cv2.imread(large)
    small = cv2.imread(small)
    result = cv2.matchTemplate(large_image, small, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 设置匹配阈值
    locations = np.where(result >= threshold)
    if locations[0].size > 0:
        point = locations[1].item(), locations[0].item()
        return point
    else:
        return -1, -1


def slowly_click(position):
    pyautogui.moveTo(position, duration=delay)  # 持续一秒
    pyautogui.click()


def click_and_copy(position):
    pyautogui.click(position)
    pyperclip.copy(global_exe_name)
    pyautogui.hotkey('ctrl', 'v')


def read_yaml():
    global yaml_data
    with open(r'/TrainModel/model_uninstall/data.yaml', 'r') as file:
        data = yaml.safe_load(file)
    yaml_data = data.get('names', [])


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def close_exe():
    run_cmd(f'''wmic process where "name='{global_exe_name}.exe'" delete''')
    # temp = run_cmd('''wmic process where "name='qq.exe'" delete''').stdout
    # print('删除实例' in temp)  # True说明关闭成功，其实直接执行就好了，没必要判断是否执行成功


def set_operate(temp_list):
    for item in temp_list:
        time.sleep(delay)
        check = item[0]
        value = item[1]
        if check == 0:  # 直接执行函数
            value()
        elif check == 1:  # 识别文字——文字操作——文字方位
            start_ocr_text(value)
        elif check == 2:
            start_img_strong(value)  # 强类型检测


def get_ocr(diff=1):  # 返回True表示相似
    global last_img_path
    global last_img_data
    now_time = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒%f')[:-4]  # 使用毫秒(两位)
    temp_save_path = f'log/{now_time}.jpg'  # 这个最后会被删除并导出视频，所以不需要名称
    ImageGrab.grab().save(temp_save_path, format='JPEG')
    if last_img_path != '':
        tmp = cal_img_differ(old_img=last_img_path, new_img=temp_save_path)
        # print('相似度：', tmp)
        if tmp < diff:  # [相似] 如果与上一张图片相似，则不进行检测，直接返回结果
            tmp = last_img_data
            tmp[2] = True  # True表示相似 same
            return tmp
    last_img_path = temp_save_path  # 保存最新路径
    # False表示不同
    last_img_data = [requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json(),
                     last_img_path, False]
    return last_img_data


def __space_lower(__text_list):  # 全部删除空格且转小写
    return __text_list.replace(" ", "").lower()


def start_ocr_text(rec_text: RecText):
    __position = rec_text.direction
    time.sleep(delay)  # 前置Sleep
    __end_flag = False
    while True:
        if __end_flag:
            break
        # results, path, same = get_ocr(diff=3)
        results, path, same = get_ocr()
        # print(same)
        for text_info in results:  # 遍历结果
            if __space_lower(rec_text.text) in __space_lower(text_info['text']):
                box = text_info['position']  # 左上 右上 右下 左下
                # 难道是点的问题？为什么都不动了
                if __position == 'start':
                    __point = box[0][0], (box[0][1] + box[3][1]) / 2
                else:
                    __point = int((box[0][0] + box[2][0]) / 2), int((box[0][1] + box[2][1]) / 2)
                rec_text.operation(__point)  # 为什么没有click
                # print(__point)
                # if same:
                #     time.sleep(delay)  # 前置Sleep
                # rec_text.operation(__point)  # 为什么没有click
                # 如果点击后图像过一秒还没有任何变化就再点一次
                # TODO check difference
                if rec_text.operation == pyautogui.click:  # Click就Repeat，设置里会有问题，只点一次的话
                    rec_text.operation(__point)
                __end_flag = True


def start_img_strong(click_img_strong: ClickImgStrong):
    time.sleep(delay)
    __end_flag = False
    while True:
        if __end_flag:
            break
        results, path, _ = get_ocr()  # 关于变化率的设想——点击这个按钮的变化率是固定的，大约5%，可以界定4-6%，认为点击成功
        args = [click_img_strong.args, path]
        outcome = click_img_strong.operation(args)
        if outcome[0] != -1 and outcome[1] != -1:
            __end_flag = True
            pyautogui.click(outcome)


def click_label(label_name, file_path):  # 判断有没有选中
    yolo_results = yolo_model(file_path)
    boxes = yolo_results[0].boxes
    for i in range(len(boxes.xyxy)):
        # 判断这两个距离是不是小于某一阈值，我需要OCR识别位置，与YOLO的位置对比
        # label = yaml_data[int(boxes.cls[i].item())]
        label = int(boxes.cls[i].item())
        confidence = round(boxes.conf[i].item(), 2)
        # 或者X差在10以内，Y的差在5以内
        if label == label_name and confidence > 0.2:  # 认为符合条件
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            points = center_x.item(), center_y.item
            pyautogui.click(points)


def combination_keys(keys):  # 很神奇，封装后就不会直接执行了
    pyautogui.hotkey(keys)


def close_focus_exe():
    pyautogui.hotkey('alt', 'f4')


def Uninstall(exe_name):
    global global_exe_name
    global_exe_name = exe_name

    read_yaml()  # 获取训练标记
    mkdir_if_not_exists(screen_path)  # 创建OCR临时存储文件夹

    op = [
        [0, check_exe_exists],
        [0, close_exe],
        [0, open_installed_application],
        [1, RecText(text='搜索应用', operation=click_and_copy)],
        # 如果程序不存在，这一步会出错
        [2, ClickImgStrong(operation=find_icon, args=r'C:\Users\USER\PycharmProjects\WindowsAI\res\windows_icon\uninstall.jpg')],
        # 图像强检测点击
        [1, RecText(text='卸载', operation=pyautogui.click)],
        [1, RecText(text='卸载', operation=pyautogui.click)],
        [1, RecText(text='是', operation=pyautogui.click)],
        [1, RecText(text='确定', operation=pyautogui.click)],
        [0, close_focus_exe],  # 关闭当前窗口
        # 怎么我还没执行呢直接就到最后了
    ]
    set_operate(op)


if __name__ == '__main__':
    # 分支问题
    try:
        Uninstall('QQ')  # 单函数仅需启用OCR
    except FileNotFoundError:
        print("文件不存在")
    finally:
        shutil.rmtree(screen_path)  # 移除OCR图片

    # TODO 仅适用于线性操作，对于上一步操作有返回的操作需要封装成函数
    # combination_keys(['ctrl', 'b'])
    # check_exe_exists()
