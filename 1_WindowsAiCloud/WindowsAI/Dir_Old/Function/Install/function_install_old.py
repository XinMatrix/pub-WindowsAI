import datetime
import math
import os
import shutil
import subprocess
import threading
import time

import pyautogui
import pyperclip
import requests
import yaml
from PIL import ImageGrab
from ultralytics import YOLO

from Dir_Old.Function.Install.function_tkinter import update_text, showTK, destroyTK

pyautogui.FAILSAFE = False  # 禁用安全模式 即使将鼠标光标移动到屏幕的左上角时 PyAutoGUI 不会触发异常
# screen_path = 'log_download'
screen_path = 'log'
global_exe_name = 'error'  # 为什么没有初始化上
create_path = ''
yolo_model = YOLO(r'/TrainModel/model_install/best.onnx', task='detect')  # 模型加载有点慢
yaml_data = []


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def read_yaml():
    global yaml_data
    # with open(r'/TrainModel/data.yaml', 'r') as file:
    with open(r'/TrainModel/model_install/data.yaml', 'r') as file:
        data = yaml.safe_load(file)
    yaml_data = data.get('names', [])


def check_chosen(file_path, text_point, choose):  # 判断有没有选中
    if choose == '-1':  # 暂时不检测选中状态
        return
    update_text('识别图像中')  # 更新提示文本
    yolo_results = yolo_model(file_path)
    update_text('程序安装中')
    boxes = yolo_results[0].boxes
    for i in range(len(boxes.xyxy)):
        # 判断这两个距离是不是小于某一阈值，我需要OCR识别位置，与YOLO的位置对比
        center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
        center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
        points_distance = distance(text_point[0], text_point[1], center_x.item(), center_y.item())
        label = yaml_data[int(boxes.cls[i].item())]
        confidence = round(boxes.conf[i].item(), 2)
        condition = 'select' if choose == '1' else 'unselect'
        # 或者X差在10以内，Y的差在5以内
        if points_distance < 5 and label == condition and confidence > 0.2:  # 认为符合条件
            return True
        # print("Box {}: ".format(i + 1))  # 1
        # print("  Center Point (x, y): ", (center_x.item(), center_y.item()))  # (501.374267578125, 819.1305541992188)
        # print("  Confidence: ", round(boxes.conf[i].item(), 2))  # 0.84
        # print("  Label: ", yaml_data[int(boxes.cls[i].item())])  # select
    return False  # 认为不符合条件


def __space_lower(text_list):  # 全部删除空格且转小写
    return text_list.replace(" ", "").lower()


def __start_ocr(__recognize_text, __operation, __position, choose):  # 记得开OCR
    time.sleep(0.8)  # 前置Sleep
    __end_flag = False
    while True:
        if __end_flag:
            break
        results, path = __get_ocr()
        for text_info in results:  # 遍历结果
            if __space_lower(__recognize_text) in __space_lower(text_info['text']):
                __end_flag = True
                box = text_info['position']
                if __position == 'start':
                    __point = box[0][0] + 10, (box[1][1] + box[3][1]) / 2
                else:  # 默认指定center
                    __point = int((box[0][0] + box[2][0]) / 2), int((box[0][1] + box[2][1]) / 2)
                if check_chosen(path, __point, choose):  # 这里要检查一遍是不是选中了
                    return
                __operation(__point)
                if check_chosen(path, __point, choose):  # 这里要再检查一遍是不是选中了
                    raise ValueError("操作失败!")


def __download_in_cmd():  # 使用阻塞线程
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
        # stopScreenRecording()
        return

    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    save_path = f'{global_exe_name}.exe'
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    __start_cmd(f'start {save_path}')


def __start_cmd(temp_command):  # 过程试图写入的管道不存在
    cmd_process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    cmd_process.stdin.write((temp_command + '\n').encode('gbk'))
    if 'curl' == temp_command[:4]:  # 仅针对Curl指令进行异步回调
        temp_output, _ = cmd_process.communicate()  # 这一行可以形成异步回调


def __set_operate(temp_list):  # 这个函数是必要的
    for item in temp_list:
        __start_ocr(item[0], item[1], item[2], item[3])


def start_install(check_delay=1):
    update_text('正在检查程序是否存在')
    time.sleep(check_delay)
    pyautogui.hotkey('Win', 'q')
    time.sleep(check_delay)
    pyperclip.copy(global_exe_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(check_delay)
    results, _ = __get_ocr()
    for text_info in results:
        if '卸载' in text_info['text']:
            pyautogui.hotkey('enter')
            return 1
    for text_info in results:
        if '运行' in text_info['text']:
            pyautogui.hotkey('enter')
            __install_exe()
            return 2
    pyautogui.hotkey('esc')
    __download_in_cmd()
    __install_exe()
    return 3


def __install_exe():  # TODO 准备进行NER识别
    update_text('程序安装中')
    temp_name = __space_lower(global_exe_name)
    if temp_name == 'qq':
        operations = [
            ['阅读并同意软件许可协议和青少年上网安全指导、隐私政策协议', pyautogui.click, 'start', 1],  # 判断这一步有没有勾选上
            ['自定义选项', pyautogui.click, 'center', -1],
            ['生成快捷方式', pyautogui.click, 'center', 0],
            ['开机自启', pyautogui.click, 'center', 1],
            ['Program Files', replace_text, 'center', -1],
            ['立即安装', pyautogui.click, 'center', -1],
            ['完成安装', pyautogui.click, 'center', -1]
        ]
    elif temp_name == '网易云音乐':
        operations = [
            ['自定义设置', pyautogui.click, 'center', -1],
            ['\\', replace_text, 'center', -1],
            ['立即安装', pyautogui.click, 'center', -1],
            ['立即使用', pyautogui.click, 'center', -1]
        ]
    else:
        operations = []
    __set_operate(operations)


def __get_ocr():
    now_time = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒%f')[:-4]  # 使用毫秒(两位)
    # temp_save_path = f'log_download/{now_time}.jpg'  # 这个最后会被删除并导出视频，所以不需要名称
    temp_save_path = f'log/{now_time}.jpg'  # 这个最后会被删除并导出视频，所以不需要名称
    ImageGrab.grab().save(temp_save_path, format='JPEG')
    return requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json(), temp_save_path


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def replace_text(position):  # 替换文字
    pyautogui.click(position)
    pyperclip.copy(create_path)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')


def Install(exe_name):
    global global_exe_name
    global create_path
    # global yolo_model
    global_exe_name = exe_name
    create_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'WindowsAI\\{global_exe_name}')

    # 准备工作
    threading.Thread(target=showTK).start()  # 启动页面
    update_text('程序启动中')  # 更新提示文本
    mkdir_if_not_exists(screen_path)  # 创建OCR临时存储文件夹
    mkdir_if_not_exists(create_path)  # 创建安装文件夹——后台操作，所以不需要delay
    # threading.Thread(target=startScreenRecording, args=(global_exe_name,)).start()  # 开始录屏 为什么一定要加个括号呀啊啊啊啊
    read_yaml()  # 获取训练标记

    time.sleep(1)

    # 安装工作
    status = start_install()

    time.sleep(1)

    # 结尾工作
    threading.Thread(target=destroyTK).start()  # 结束窗口
    shutil.rmtree(screen_path)  # 移除OCR图片
    if status != 1:
        os.remove(f'{global_exe_name}.exe')
    # stopScreenRecording()  # 结束录屏


if __name__ == '__main__':
    Install('QQ')
    # 点击生成快捷方式后就卡柱了
    # 无法完成安装，疑似YOLO问题
    # 要不要直接强对比，因为我知道QQ是什么样子的
