import logging
import os
import re
import time

import keyboard
import pyautogui
import pygetwindow
import requests
from PIL import ImageGrab

from MyFunClass import MyFun, get_system_id, start_action
from config import db, last_img, ocr_url, ocr_acc

pyautogui.FAILSAFE = False  # 注意安全，可以新增键盘输入结束控制

# 在这里新建文件夹算了
MyFun.Init.create_directories('MyWindowsAi',
                              ['Programs', 'Downloads', 'Projects', 'Statics', 'Configs', 'Logs'])  # 默认先都在C盘创建

# 定义日志格式
log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running_log.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    # filename='main_output.log',  # 日志输出到的文件
                    filename=log_path,  # 日志输出到的文件
                    filemode='w')  # 发布时日志应该是连续的 'a' 表示追加模式，'w' 表示覆盖模式


def on_hotkey():
    logging.error('用户强行停止程序')
    os._exit(0)


def init_program():
    # 检测是否为管理员权限
    if MyFun.System.is_admin() != 1:
        logging.critical('PERMISSION NOT ALLOWED!')
        raise PermissionError('权限不足，请使用管理员权限')

    # 初始化程序目录，程序放在Program，配置文件放在config，下载放在Downloads
    # Program 安装程序
    # Downloads 下载文件程序
    # Projects 项目文件
    # Outputs 输出文件，如WIFI密码等
    # Configs 配置文件，如WindowsAi.png

    # 初次下载资源，并解压删除移动到Configs文件夹
    file_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Configs\\BG_WindowsAi.png')
    if not os.path.exists(file_path):  # 检查是否已经下载过，没有才下载
        logging.info('Downloading Init Resources...')
        new_path = MyFun.Fun.download('BG_WindowsAi.png')
        MyFun.Fun.move_files(new_path, 'Configs')  # From - To(Standard)

    logging.info('Add Stop Hotkey')
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)  # 强行停止快捷键 Ctrl+Alt+K


def main_function():
    # 初始化环境
    init_program()

    id_list = []

    task = input('请输入操作名称: ')
    result = db.find_tasks_by_task(task)  # 先拿到一大类的所有数据
    uuid = get_system_id()
    if not result:  # 查找识别的情况
        logging.error('CAN NOT FOUND TASK IN DB.')
        raise ModuleNotFoundError('数据库中无该操作')

    # 记得给个新建桌面
    # pyautogui.hotkey('ctrl', 'win', 'd')  # 新建桌面——这个是需要的，但是现在测试可以不用，注意顺序
    MyFun.Init.show_bg()

    logging.info('Start OCR Detection')

    time.sleep(1)  # 作用是什么——当然是等待背景加载完成，给一秒把，0.5有时会出问题

    # TODO 不一定要OCR主导吧，能不能想办法降低OCR使用频率
    # 本来想的是模拟人眼，每秒看一次屏幕，但其实很多操作闭着眼睛做也行，效率更高——记忆、准确、迅速

    while True:

        logging.info('Looping...')

        # logging.info(f'Running Window Titles: {pygetwindow.getAllTitles()}')  # 这里不需要句柄，所以可以用getAllTitles()

        ImageGrab.grab().save(last_img, format='JPEG')
        # 截屏不显示鼠标  # 这一行居然会报错权限不足，偶发性异常，报错Invalid argument: 'last_img.jpg'

        ocr_text, ocr_position = [], []
        ocr_outputs = requests.post(ocr_url, files={'image': open(last_img, 'rb')}, data={'uuid': uuid}).json()

        if not ocr_outputs:  # 内容为空应警告
            logging.error('OCR内容为空')
            continue  # 进入下一轮检测

        for item in ocr_outputs:  # 什么时候变小写，这个是不是不太好，应该在判定的地方用小写
            ocr_text.append(item['text'])
            ocr_position.append(MyFun.Input.average_position(item['position']))

        ocr_accuracy_outputs = requests.post(ocr_acc, files={'image': open(last_img, 'rb')}, data={'uuid': uuid}).json()

        logging.info(f'OCR Text = {ocr_text}')

        # 我咋感觉这个应该用while True呢，因为它会自动结束，使用FINISH函数
        for item in result:
            if re.search(r"\bOCR\((.*?)\)", item[2]):  # OCR(TEXT%) 匹配
                target = re.search(r"\bOCR\((.*?)\)", item[2]).group(1)
                db_collection = target.split('->')  # 哈哈这个是错的，但是不影响，应该是3而不是2——并不是错的，而是我之前OCR是可以使用多文本的，现在没写而已
                for j in db_collection:  # 检测OCR文本，单文本无视即可
                    if MyFun.Fun.fuzzy_search(j, ocr_text):  # 匹配成功 包含关系 找到返回True
                        if item[0] in id_list:  # 避免重复操作
                            break
                        id_list.append(item[0])
                        logging.info(f'Match Succeed OCR : {item}')
                        start_action(result, item[3], logging, ocr_text, ocr_position, ocr_accuracy_outputs)
                        break  # 结束匹配
            # 为什么不直接使用RUN函数以执行id操作
            elif item[2].startswith('WindowsAi特殊标识符'):  # 用户GOTO继续
                break  # 直接下一条
            else:  # 给予更多可能性
                logging.info(f'鉴别符错误 : {item[2]}')
                raise ValueError('鉴别符错误')
        time.sleep(1)  # 间隔一秒的OCR——因为OCR本身也需要识别时间，所以可以快一点，还是一秒把，快了容易出问题


if __name__ == '__main__':
    try:
        main_function()
    except Exception as e:
        # 这时应该打开日志——Nice 一次成功
        logging.error(f'An error occurred: {e}', exc_info=True)
        os.startfile(log_path)  # 打开日志
