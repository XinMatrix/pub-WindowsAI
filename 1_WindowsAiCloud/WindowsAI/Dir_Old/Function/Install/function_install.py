# 下载程序
import datetime
import math
import os
import shutil
import subprocess
import threading
import time
import cv2
import numpy as np
import pyautogui
import pyperclip
import requests
import yaml
from PIL import ImageGrab
from ultralytics import YOLO

from Dir_Old.Function.Install.function_tkinter import showTK, update_text, destroyTK

delay = 0.8
global_exe_name = ''
screen_path = 'log'

create_path = ''
yolo_model = YOLO(r'/TrainModel/model_install/best.onnx', task='detect')  # 模型加载有点慢
yaml_data = []

last_img_path = ''  # 用于与上一张图片对比
last_img_data = ''  # OCR信息


class RecText:  # 1
    def __init__(self, text, operation, position='default'):  # 必须传入文字与操作，方向可选
        self.text = text
        self.operation = operation
        self.direction = position


class ClickImgStrong:  # 1
    def __init__(self, operation, args):  # 必须传入函数名称与参数
        self.operation = operation
        self.args = args


class ClickImgAndText:  # 1
    def __init__(self, text, label):  # 必须传入函数名称与参数
        self.text = text
        self.label = label


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


def start_install():
    check_exists()
    results, _ = get_ocr()
    temp = []
    for text_info in results:
        temp.append(text_info['text'])
    if '卸载' in temp:
        pyautogui.hotkey('enter')
        exit()
    elif '运行' in temp:
        pyautogui.hotkey('enter')
        install_exe()  # 检测到安装包，打开后安装
        exit()
    else:
        pyautogui.hotkey('esc')
        download_in_cmd()
        install_exe()
        exit()


def open_installed_application():
    time.sleep(delay)
    pyautogui.hotkey('win', 'x')
    time.sleep(delay)
    pyautogui.hotkey('p')
    time.sleep(delay)


# 感觉这个函数写的不错
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


def set_operate(temp_list):  # 这个函数是必要的
    for item in temp_list:
        time.sleep(delay)
        check = item[0]
        value = item[1]
        if check == 0:  # 直接执行函数
            value()
        elif check == 1:  # 识别文字——文字操作——文字方位
            start_ocr_text(value)
        elif check == 2:  # 强识别
            start_img_strong(value)
        elif check == 3:  # 弱识别
            start_img_week(value)


def get_ocr():
    global last_img_path
    global last_img_data
    now_time = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒%f')[:-4]  # 使用毫秒(两位)
    temp_save_path = f'log/{now_time}.jpg'  # 这个最后会被删除并导出视频，所以不需要名称
    ImageGrab.grab().save(temp_save_path, format='JPEG')
    if last_img_path != '':
        tmp = cal_img_differ(old_img=last_img_path, new_img=temp_save_path)
        # print('相似度：', tmp)
        if tmp < 1:  # 如果与上一张图片相似，则不进行检测，直接返回结果
            return last_img_data
    last_img_path = temp_save_path
    last_img_data = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json(), last_img_path
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
        results, path = get_ocr()
        for text_info in results:  # 遍历结果
            if __space_lower(rec_text.text) in __space_lower(text_info['text']):
                box = text_info['position']
                __point = int((box[0][0] + box[2][0]) / 2), int((box[0][1] + box[2][1]) / 2)
                rec_text.operation(__point)  # 为什么没有click
                if rec_text.operation == pyautogui.click:  # Click就Repeat，设置里会有问题，只点一次的话
                    rec_text.operation(__point)
                __end_flag = True


def start_img_week(c: ClickImgAndText):
    time.sleep(delay)
    __end_flag = False
    while True:
        if __end_flag:
            break
        results, path = get_ocr()
        for text_info in results:  # 遍历结果
            if c.text in text_info['text']:
                box = text_info['position']
                point = int((box[0][0] + box[2][0]) / 2), int((box[0][1] + box[2][1]) / 2)
                if start_yolo(c.label, path, point):
                    __end_flag = True


def start_img_strong(click_img_strong: ClickImgStrong):
    time.sleep(delay)
    __end_flag = False
    while True:
        if __end_flag:
            break
        _, path = get_ocr()
        args = [click_img_strong.args, path]
        outcome = click_img_strong.operation(args)
        if outcome[0] != -1 and outcome[1] != -1:
            __end_flag = True
            pyautogui.click(outcome)


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def start_yolo(label_name, file_path, text_position):  # 判断有没有选中
    yolo_results = yolo_model(file_path)
    boxes = yolo_results[0].boxes
    for i in range(len(boxes.xyxy)):
        # 判断这两个距离是不是小于某一阈值，我需要OCR识别位置，与YOLO的位置对比
        label = yaml_data[int(boxes.cls[i].item())]
        # label = int(boxes.cls[i].item())
        confidence = round(boxes.conf[i].item(), 2)
        # 或者X差在10以内，Y的差在5以内
        # 我需要对label_name取反，即点击后正确
        if str(label_name).startswith('un'):
            click_label = label_name[2:]
        else:
            click_label = f'un{label_name}'
        if label == click_label and confidence > 0.2:  # 认为符合条件
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            points = center_x.item(), center_y.item
            points_differ = calculate_distance(center_x, center_y, text_position[0], text_position[1])
            if points_differ < 50:  # 两个像素差小于50认为在一块
                pyautogui.click(points)
                return True
    return False


def combination_keys(keys):  # 很神奇，封装后就不会直接执行了
    pyautogui.hotkey(keys)


def close_focus_exe():
    pyautogui.hotkey('alt', 'f4')


def check_exists():
    time.sleep(delay)
    pyautogui.hotkey('Win', 'q')
    time.sleep(delay)
    pyperclip.copy(global_exe_name)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')


def replace_text(text):  # 替换文字
    pyautogui.click(text)
    pyperclip.copy(create_path)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')


def install_exe():  # TODO 准备进行NER识别
    update_text('程序安装中')
    temp_name = __space_lower(global_exe_name)
    if temp_name == 'qq':
        operations = [
            [0, start_install],  # 直接执行函数 可以在卸载前先检测程序是否存在
            # [0, close_exe],  # 直接执行函数
            # [2, ClickImgStrong(operation=find_icon, args=r'C:\Users\USER\PycharmProjects\WindowsAI\res\windows_icon\uninstall.jpg')],  # 图像强检测点击
            [1, RecText(text='阅读并同意软件许可协议和青少年上网安全指导、隐私政策协议', operation=pyautogui.click, position='start')],
            [1, RecText(text='自定义选项', operation=pyautogui.click)],
            [3, ClickImgAndText(text='生成快捷方式', label='unselect')],  # TODO 调用YOLO 测试Install
            # [3, ClickImgWeek(operation=click_label, args=1)]  # label int 安装选中检测 图像若检测点击
            [3, ClickImgAndText(text='开机自启', label='select')],  # 我希望检测到label是 select 或 unselect 的，并且距离参数文字较近
            [1, RecText(text='Program Files', operation=replace_text)],
            [1, RecText(text='立即安装', operation=pyautogui.click)],
            [1, RecText(text='确定', operation=pyautogui.click)],
            [1, RecText(text='完成安装', operation=pyautogui.click)],
        ]
        # operations = [
        #     ['阅读并同意软件许可协议和青少年上网安全指导、隐私政策协议', pyautogui.click, 'start', 1],  # 判断这一步有没有勾选上
        #     ['自定义选项', pyautogui.click, 'center', -1],
        #     ['生成快捷方式', pyautogui.click, 'center', 0],
        #     ['开机自启', pyautogui.click, 'center', 1],
        #     ['Program Files', replace_text, 'center', -1],
        #     ['立即安装', pyautogui.click, 'center', -1],
        #     ['完成安装', pyautogui.click, 'center', -1]
        # ]
    # elif temp_name == '网易云音乐':
    #     operations = [
    #         ['自定义设置', pyautogui.click, 'center', -1],
    #         ['\\', replace_text, 'center', -1],
    #         ['立即安装', pyautogui.click, 'center', -1],
    #         ['立即使用', pyautogui.click, 'center', -1]
    #     ]
    else:
        operations = []
    set_operate(operations)


def start_cmd(temp_command):  # 过程试图写入的管道不存在
    cmd_process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd_process.stdin.write((temp_command + '\n').encode('gbk'))
    if 'curl' == temp_command[:4]:  # 仅针对Curl指令进行异步回调
        temp_output, _ = cmd_process.communicate()  # 这一行可以形成异步回调


def download_in_cmd():  # 使用阻塞线程
    update_text('程序下载中')
    download_url_map = {  # 创建一个映射
        'qq': 'https://dldir1.qq.com/qqfile/qq/QQNT/Windows/QQ_9.9.9_240410_x64_01.exe',  # 4月13日已更新
        '网易云音乐': 'https://d1.music.126.net/dmusic/NeteaseCloudMusic_Music_official_3.0.0.Beta.03.25.202691.64.exe'
    }
    # 查找对应的值
    temp_name = __space_lower(global_exe_name)
    if temp_name in download_url_map:
        value = download_url_map[temp_name]
        download_url = value
    else:
        update_text('程序下载地址暂未录入')
        threading.Thread(target=destroyTK).start()  # 结束窗口
        shutil.rmtree(screen_path)  # 移除OCR图片
        os.remove(global_exe_name + '.exe')
        return

    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    save_path = f'{global_exe_name}.exe'
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    start_cmd(f'start {save_path}')


def Install(exe_name):
    global global_exe_name
    global create_path
    global_exe_name = exe_name
    create_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'WindowsAI\\{global_exe_name}')

    threading.Thread(target=showTK).start()  # 启动页面
    update_text('程序启动中')  # 更新提示文本
    read_yaml()  # 获取训练标记
    mkdir_if_not_exists(screen_path)  # 创建OCR临时存储文件夹
    mkdir_if_not_exists(create_path)  # 创建安装文件夹——后台操作，所以不需要delay

    op = [[0, start_install]]
    set_operate(op)

    # [3, ClickImgWeek(operation=click_label, args=1)]  # label int 安装选中检测 图像若检测点击

    shutil.rmtree(screen_path)  # 移除OCR图片
    # stopScreenRecording()  # 结束录屏


if __name__ == '__main__':
    Install('QQ')  # TODO 测试QQ安装，修复Bug
    # 果然问题多多
    # combination_keys(['ctrl', 'b'])
    # check_exe_exists()
