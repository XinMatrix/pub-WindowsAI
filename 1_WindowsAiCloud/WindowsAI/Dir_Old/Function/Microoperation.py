# 微操作处理类，定义了各种微型操作函数
# 2024/5/13
import os
import time

import cv2
import numpy as np
import pyautogui
import pyperclip
import requests
from PIL import ImageGrab, Image

pyautogui.FAILSAFE = False  # 禁用安全模式 即使将鼠标光标移动到屏幕的左上角时 PyAutoGUI 不会触发异常

temp_save_path = 'temp_file.jpg'


def find_icon(lst):  # small是我要找的东西 large是截屏
    small = lst[0]
    large = lst[1]
    large_image = cv2.imread(large)
    small = cv2.imread(small)
    result = cv2.matchTemplate(large_image, small, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 设置匹配阈值
    locations = np.where(result >= threshold)
    if locations[0].size > 0:
        return locations[1].item(), locations[0].item()
    else:
        return -1, -1


def get_image_average_color(image_path):  # 获取图像整体RGB值
    # 打开图片
    img = Image.open(image_path)
    # 将图片转换为RGB模式（如果不是）
    img = img.convert("RGB")
    # 获取图片的像素数据
    pixels = img.load()
    # 初始化颜色累加值
    total_red = 0
    total_green = 0
    total_blue = 0
    total_pixels = img.width * img.height
    # 遍历所有像素，并累加颜色值
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            total_red += r
            total_green += g
            total_blue += b
    # 计算颜色均值
    average_red = total_red // total_pixels
    average_green = total_green // total_pixels
    average_blue = total_blue // total_pixels
    return (average_red + average_green + average_blue) / 3


def crop_and_save(image_path, center_x, center_y, output_path):  # 以某点为中心裁剪图像
    img = Image.open(image_path)  # 打开图片
    value = 5  # 5*5
    # 计算截取区域的左上角和右下角坐标
    left = max(0, center_x - value)
    top = max(0, center_y - value)
    right = min(img.width, center_x + value)
    bottom = min(img.height, center_y + value)
    cropped_img = img.crop((left, top, right, bottom))  # 截取图片
    cropped_img.save(output_path)  # 保存截取后的图片


def average_coordinates(points):
    # 初始化总和为0
    sum_x = 0
    sum_y = 0
    # 遍历每个点的坐标
    for point in points:
        # 将x坐标和y坐标分别加到总和中
        sum_x += point[0]
        sum_y += point[1]
    # 计算平均值
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)
    # 返回平均值的元组
    return avg_x, avg_y


def start_action(temp_order):
    global temp_save_path
    ocr_sleep_time = 2  # 因为要考虑部分动画效果，所以延迟大点好
    total_split = temp_order.split('>>')
    head = total_split[0].split('_')
    method = head[0]  # Install
    obj = head[1]  # QQ
    body = total_split[1]
    split_order = body.split('->')
    # for item in split_order:
    #     start_action()
    # map?
    for item in split_order:
        time.sleep(ocr_sleep_time)  # 每个操作之间间隔一秒
        middle = item.split('_')
        action = middle[0]
        content = middle[1].lower()
        if action == 'key':  # 组合输入键盘内容
            collections = content.split('+')
            pyautogui.hotkey(collections)
        elif action == 'cp':
            old_clip = pyperclip.paste()
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v')
            pyperclip.copy(old_clip)  # 恢复之前的剪切数据
        elif action == 'ocr':
            # 开启之前先连接本地Service
            # 这里要考虑OCR是一直开着还是需要的时候再开的问题了
            # 现阶段不考虑错误问题，即我们认为计算机操作有健壮性
            # 这里需要的是截图直接返回结果，查找定位文字并点击
            # now_time = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒%f')[:-4]  # 使用毫秒(两位)
            # temp_save_path = f'log/{now_time}.jpg'
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                outputs = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json()
                for text in outputs:
                    if content in text['text'].lower():  # 注意小写 注意不应该是等于，而是in，注意content是我写入的，text是查到的
                        pyautogui.click(average_coordinates(text['position']))
                        __flag = False
        elif action == 'ocra':  # ocr agree
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                outputs = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json()
                for text in outputs:
                    if content in text['text'].lower():
                        position = text['position']  # 左上 右上 右下 左下
                        # 把0和2的y平均一下，1的x左移一下
                        new_x = position[0][0] + 10  # OK
                        new_y = (position[0][1] + position[2][1]) / 2
                        pyautogui.click(new_x, new_y)
                        __flag = False
        elif action == 'ocrd':  # ocr download 替换为下载链接
            # 点击
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                outputs = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json()
                for text in outputs:
                    # if 'Program Files' or 'WindowsAI' in text['text'].lower():  # Nice
                    # if 'Program Files' in text['text'].lower():  # Nice
                    # if 'Program Files'.lower() in text['text'].lower():  # Nice
                    if content in text['text'].lower():  # Nice
                        pyautogui.click(average_coordinates(text['position']))
                        __flag = False
            # 替换
            old_clip = pyperclip.paste()
            pyautogui.hotkey('ctrl', 'a')
            install_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'WindowsAI\\{obj}')
            pyperclip.copy(install_path)
            pyautogui.hotkey('ctrl', 'v')
            pyperclip.copy(old_clip)  # 恢复之前的剪切数据
        elif action == 'opene':  # 打开程序文件 我应该首先默认在指定位置搜索，不行再Win+Q，CP # 因为要等待下载，所以用OCR更好
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            # Documents（文档）：用于存储用户文档文件的文件夹。
            # Pictures（图片）：存储用户图片和照片的文件夹，如JPEG、PNG等格式的图片文件。
            # Music（音乐）：用于存储用户音乐文件的文件夹，如MP3、WAV等格式的音乐文件。
            # Videos（视频）：用于存储用户视频文件的文件夹，如MP4、AVI等格式的视频文件。
            # Desktop（桌面）：用户桌面上的文件夹，通常用于存放常用的文件和快捷方式。
            # Documents（文档）：用于存储用户文档文件的文件夹。
            # Downloads（下载）：存放下载的文件的默认文件夹。
            # Public（公共）：用于存储公共文件的文件夹，可以被所有用户访问。
            for root, dirs, files in os.walk(download_folder):
                for file in files:
                    if content in file.lower() and file.endswith(".exe"):  # 注意用小写
                        file_path = os.path.join(root, file)
                        os.startfile(file_path)  # 运行程序
                        break
                else:
                    continue
                break  # 停止遍历，因为已经找到并打开了文件
            else:
                # 下载找不到
                print("Opene Error:Execution Not Found!")
        elif action == 'opt0':  # 写成op0了，我说怎么不行 # moveTo但并不点击
            # 先尝试使用硬编码，计算图形学特征（色彩提取）
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                outputs = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json()
                for text in outputs:
                    if content in text['text'].lower():
                        position = text['position']
                        new_x = position[0][0] + 10
                        new_y = (position[0][1] + position[2][1]) / 2
                        # 以新坐标为中心，截取一个10*10的矩形，计算平均颜色
                        crop_path = 'temp_crop.jpg'
                        crop_and_save(temp_save_path, new_x, new_y, crop_path)
                        ave_rgb = get_image_average_color(crop_path)
                        if ave_rgb in range(0, 50) or ave_rgb in range(200, 255):  # 平均像素值在边界范围，即黑色或白色，认为未选中
                            pyautogui.moveTo(new_x, new_y)  # 认为未选中，仅移动鼠标
                        else:  # 认为选中，点击取消选择
                            pyautogui.click(new_x, new_y)
                        __flag = False
        elif action == 'opt1':
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                outputs = requests.post('http://127.0.0.1:5000/ocr', files={'image': open(temp_save_path, 'rb')}).json()
                for text in outputs:
                    if content in text['text'].lower():
                        position = text['position']
                        new_x = position[0][0] + 10
                        new_y = (position[0][1] + position[2][1]) / 2
                        # 以新坐标为中心，截取一个10*10的矩形，计算平均颜色
                        crop_path = 'temp_crop.jpg'
                        crop_and_save(temp_save_path, new_x, new_y, crop_path)
                        ave_rgb = get_image_average_color(crop_path)
                        if ave_rgb in range(0, 50) or ave_rgb in range(200, 255):  # 平均像素值在边界范围，即黑色或白色，认为未选中
                            pyautogui.click(new_x, new_y)
                        else:
                            pyautogui.moveTo(new_x, new_y)  # 认为未选中，仅移动鼠标
                        __flag = False
        elif action == 'ece':  # execute 执行内部函数 'ece_StopProgram'
            if content == 'stopprogram':  # 注意小写
                os.system(f'taskkill /f /im {obj}.exe')
        elif action == 'hi':  # hard icon 识别并点击
            if content == 'uninstall':
                time.sleep(2)
                ImageGrab.grab().save(temp_save_path, format='JPEG')
                tmp = find_icon([r'C:\Users\USER\PycharmProjects\WindowsAI\res\windows_icon\uninstall.jpg', temp_save_path])
                if tmp[0] != -1:  # -1说明没找到
                    pyautogui.click(tmp)


# All Lower in Operations
# 还是用Chrome吧，真窒息，毕竟是第一占有率的浏览器
if __name__ == '__main__':

    # 'start_qq>>key_win+q->cp_qq->key_enter' # 安装完会直接打开，不需要这个

    # 怎么QQ下载文字还变了
    # 下载安装卸载QQ测试成功!
    orders = [  # 下载安装QQ # 卸载QQ
        'download_qq>>key_win+d->key_win+q->cp_Chrome->key_enter->cp_https://im.qq.com/index/->key_enter->ocr_下载->ocr_windows->ocr_全新版本下载',
        'install_qq>>ocr_完成->ocra_阅读并同意->ocr_自定义选项->ocrd_Program->opt0_生成快捷方式->opt1_开机自动启动->ocr_立即安装->ocr_完成安装',
        # 'uninstall_qq>>ece_StopProgram->key_win+x->key_p->ocr_搜索应用->cp_qq->hi_uninstall->ocr_卸载->ocr_卸载->ocr_卸载->ocr_是->ocr_确定'
    ]
    # 卸载完应该关闭设置页面

    # OCRD_Program = OCR_Program->rp_downloadurl

    # Win + Up Or Win + D
    # 下载安装网易云音乐测试成功!
    # orders = [  # 下载安装网易云音乐
    #     'download_网易云音乐>>key_win+d->key_win+q->cp_Chrome->key_enter->cp_https://music.163.com/#->key_enter->ocr_下载客户端->ocr_下载新版客户端',
    #     'install_网易云音乐>>ocr_完成->ocr_自定义设置->ocrd_Program->opt0_创建桌面快捷方式->opt0_添加到任务栏->opt1_开机启动->opt0_将网易云音乐设为默认播放器->ocr_立即安装->ocr_立即使用',
    # ]

    # 如果屏幕在动就不进行操作？

    # orders = ['None_Object>>ece_StopProgram']
    # orders = ['None_Object>>hi_uninstall']

    # 错误处理怎么办——这将会是个大模块

    # 实践是检验真理的唯一标准
    # 发现一个问题：保留二字如何处理——异常处理怎么做
    # 发现另一个问题：点击之后效果不对，找不到下一步，是不是应该重复操作，OCR

    for order in orders:
        start_action(order)

    # 大数据的重要性
    # 问一段文字，它最可能出现在哪里，作用是什么
    # 文字相似度匹配，如果表达的意思相同则认为是同一种方式
    # 该内容为第三阶段
    # 考虑动态规划，根据页面内容生成下一步操作，比如说我要安装一个未知的程序，我应该制定一个基本框架，让程序在框架内自由发挥，程序根据大量训练内容结合OCR文本选择点击
    # 如安装XX->下载XX，安装XX，启动XX
    # 对已有操作可直接生成，未知操作应逐步生成(所需资源较多)
    # 重要的是生成下一步，而不是所有，也就在所有文字中选择最可能的那个
    # 感觉数据量大了之后NLP可以理解，不需要专门制作数据集
    # 感觉可以出一个系统专门判别文字匹配度，匹配度高就可以泛化结果了
    # 卸载是不是也得做——当然
    # ocra == ocr agree 点击前方
    # ocrd == ocr download 粘贴填入下载链接

    # QQ发送/查看消息
    # 网易云音乐播放歌单/搜索音乐
