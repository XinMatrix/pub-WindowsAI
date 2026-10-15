# 编写脚本快速启动开发环境
import os
import time

import pyautogui


def PressKey(param):
    keys = param.split('+')
    temp_keys = []
    for key in keys:
        temp_keys.append(key.lower())
    pyautogui.hotkey(temp_keys)


def Input(s):
    pyautogui.typewrite(s)


if __name__ == '__main__':
    # 为什么管理员运行会报错但是普通用户运行就没问题？

    input('请按任意键开始...')

    # 打开软件
    delay = 1

    # 暂时无法使用管理员身份运行，需要的话再改
    time.sleep(delay)
    PressKey('Ctrl+B')
    time.sleep(delay)
    Input('PyCharm Community Edition 2023.3.4')
    time.sleep(delay * 2)
    PressKey('Right')
    time.sleep(delay)
    Input('A')
    time.sleep(delay)
    PressKey('Enter')
    time.sleep(delay)

    os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2023.3.4.lnk')
    time.sleep(delay * 5)
    os.startfile(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VMware\VMware Workstation Pro.lnk')
    time.sleep(delay * 5)
    pyautogui.click(100, 190)
    # 直接打开会无法生成安装包，必须使用anaconda prompt
    # # 打开 Anaconda Prompt
    time.sleep(delay * 5)
    PressKey('Ctrl+B')
    time.sleep(delay)
    Input('Anaconda Prompt')
    time.sleep(delay)
    PressKey('Enter')
    time.sleep(delay)
