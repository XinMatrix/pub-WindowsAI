# 第二次运行时不会打印结果，因为已经结束了
import threading
import time
import webbrowser

import keyboard
import pyautogui
import requests
from PIL import ImageGrab, ImageChops
from ultralytics import YOLO

# 配置代码
ocr_url = 'http://127.0.0.1:5000/ocr'
pyautogui.FAILSAFE = False
standard_confidence = 0.85
delay = 1

# 实例代码
download_url = 'https://www.listary.com/download-completion?version=stable'
# model = YOLO('x_100.onnx', task='detect')
yolo_model = YOLO('TrainModel/v1.pt', task='detect')


def __detectImage():
    time.sleep(1)  # 一秒一次，优化性能
    picture = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    # if __calDifference(picture):
    #     return
    ocrExecution(picture)
    yoloExecution(picture)


# 可以使用try捕获异常结束，同时输入esc
__exit_flag = False


def __detect_keyboard_input():  # 双下划线开头表示私有(实际Python并没有私有的概念)
    global __exit_flag
    while True:
        if keyboard.is_pressed('esc'):
            __exit_flag = True
            break


def __detect_screen_image():
    while not __exit_flag:
        __detectImage()


# 开启两个线程——这个好像要手动结束，有时候会变卡
def start():
    threading.Thread(target=__detect_keyboard_input).start()
    threading.Thread(target=__detect_screen_image).start()


# 等待最后一次结束后停止(可选)
# keyboard_thread.join()
# screen_thread.join()


__imageOld_pil = None  # 检测图片差异


# 检测差异，再选择是否计算——已验证
def __calDifference(image_new):  # 这个应该后期写
    global __imageOld_pil
    if __imageOld_pil is None:
        __imageOld_pil = image_new.convert('RGB')
        return False
    imageNew_pil = image_new.convert('RGB')
    diff = ImageChops.difference(imageNew_pil, __imageOld_pil)
    bbox = diff.getbbox()
    if bbox is None:
        return True  # 无差异
    else:
        __imageOld_pil = imageNew_pil
        return False  # 有差异


# 点击输入相关操作
def myPress(key_list):
    for key in key_list:
        pyautogui.keyDown(key)
    for key in key_list:
        pyautogui.keyUp(key)


def myInput(input_text):
    pyautogui.typewrite(input_text, interval=0.1)


# Next和Accept是同时出现的

# name_list = ['在文件夹中显示', 'Listary.exe', 'I accept the agreement', 'Next']
# name_list = ['在文件夹中显示', 'Listary.exe', 'I accept the agreement', '']
name_list = ['在文件夹中显示', 'Listary.exe']  # 检测到在文件夹中显示后 Tab Enter即可
# name_list_no_spaces = [name.replace(" ", "") for name in name_list]

index = 0


# 为什么点击之后GPU就是0了 Index Out of Range——因为那两个同时识别到了
def ocrExecution(picture):
    global index
    if index == 2:
        myPress(['tab'])
        myPress(['up'])
        myPress(['enter'])
        myPress(['enter'])
        # myPress(['enter'])
    # if index >= len(name_list_no_spaces):
    #     return
    temp_path = 'last_screen_shoot.jpg'
    picture.save(temp_path, format='JPEG')
    files = {'image': open(temp_path, 'rb')}
    response = requests.post(ocr_url, files=files)
    print('i:' + str(index))
    if response.status_code == 200:
        text_info_list = response.json()
        # if '在文件夹中显示' in text_info_list:
        #     print('In-------------在文件夹中显示')
        # elif 'Listary.exe' in text_info_list:
        #     print('In-------------Listary.exe')
        # elif 'I accept the agreement' in text_info_list:
        #     print('In-------------I accept the agreement')
        # elif 'Next' in text_info_list:
        #     print('In-------------Next')
        for text_info in text_info_list:
            if name_list[index] in text_info['text'].replace(" ", ""):
                # print('Text--------------------' + text_info['text'].replace(" ", ""))
                if index != 0:
                    pyautogui.moveTo(text_info['position'])
                    pyautogui.click()
                index += 1
                # if index == len(nameList_no_spaces) + 1:
                #     print('Exists-------------------------------')
                #     sys.exit()
                break
        # return
        # if text_info['confidence'] > standard_confidence:
        #     if index != 0:
        #         pyautogui.moveTo(text_info['position'])
        #         pyautogui.click()
        #     index += 1
        #     if index == len(nameList_no_spaces):
        #         print('Exists-------------------------------')
        #         sys.exit()
        #     break


# 应同时由YOLO判断是Download页面
def yoloExecution(picture):
    return
    results = yolo_model(picture)
    boxes = results[0].boxes
    for i in range(len(boxes.xyxy)):
        # 前置判断
        print("Box {}: ".format(i + 1))
        # center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
        # center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
        # pyautogui.moveTo(center_x, center_y)
        # pyautogui.click()
        # pyautogui.click()
        print("  Confidence: ", boxes.conf[i])
        print("  Label: ", boxes.cls[i])


# TODO 为什么按键不行呢
if __name__ == '__main__':
    # 正式操作
    webbrowser.open(download_url)  # 在默认浏览器中打开指定的网址
    time.sleep(delay)
    myPress(['ctrl', 'j'])  # 打开下载页面
    # 判断是否下载完成
    time.sleep(delay)
    text = ''
    while text != '在文件夹中显示':
        time.sleep(delay)
        picture = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        temp_path = 'last_screen_shoot.jpg'
        picture.save(temp_path, format='JPEG')
        files = {'image': open(temp_path, 'rb')}
        response = requests.post(ocr_url, files=files)
        print('i:' + str(index))
        if response.status_code == 200:
            text_info_list = response.json()
            for text_info in text_info_list:
                if text_info['text'] == '在文件夹中显示':
                    text = '在文件夹中显示'
    # time.sleep(delay)
    time.sleep(5)
    # myPress(['tab'])
    myPress(['tab'])
    time.sleep(delay)
    myPress(['enter'])
    # start()
