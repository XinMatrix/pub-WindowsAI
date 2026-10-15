import logging
import os
import time

import keyboard

from MyFunClass import MyFun, start_action

# 默认导入会出现问题，Pyinstaller
# from Dir_New.Program.MyFunClass import MyFun, start_action
# from Dir_New.Program.config import db

# 不需要这个了
# pyautogui.FAILSAFE = False  # 注意安全，可以新增键盘输入结束控制

MyFun.Init.create_directories('MyWindowsAi',
                              ['Programs', 'Downloads', 'Projects', 'Statics', 'Configs', 'Logs'])  # 默认先都在C盘创建

# 定义日志格式
log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running_log.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
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
        MyFun.Fun.move_files(new_path, 'Configs')  # From - To

    # 能不能直接下载到Config里

    logging.info('Add Stop Hotkey')
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)  # 强行停止快捷键 Ctrl+Alt+K


# 我需要使用非OCR主导的逻辑循环
def main_function(result, user_message):
    init_program()

    MyFun.Init.show_bg()
    time.sleep(1)

    ocr_outputs = MyFun.Fun.once_ocr()  # 先进行一次OCR识别，开始任务

    # 开始使用强制检测，必须完全相等，相当于一次小自检
    if any(item['text'] == 'WindowsAi' for item in ocr_outputs):  # 执行第一条，第一条永远是第一条，不存在分支情况
        start_action(result, result[0][3], logging, user_message)  # start_action函数仅仅是执行数据库操作，其他概不影响
    else:
        logging.error('WindowsAi识别失败')
        raise Exception('WindowsAi识别失败')
