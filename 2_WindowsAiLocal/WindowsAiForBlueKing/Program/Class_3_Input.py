import os
import re
import time

import pyautogui
import pyperclip
import win32api
from pynput.mouse import Controller

from Class_4_Fun import _detect_language_status, once_ocr_zh, once_ocr_en, fuzzy_search, MapValue
from config import my_logger

# 关闭 PyAutoGUI 的安全模式
pyautogui.FAILSAFE = False


def average_position(points):
    sum_x = 0
    sum_y = 0
    for point in points:
        sum_x += point[0]
        sum_y += point[1]
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)
    return avg_x, avg_y


def _smooth_move_win32(x, y, duration=1, steps=100):  # 平滑移动——最快一秒，你自己看着办吧
    start_x, start_y = win32api.GetCursorPos()
    x_distance = x - start_x
    y_distance = y - start_y
    for i in range(steps):
        progress = i / steps
        if progress < 0.5:
            easing_progress = 2 * progress * progress
        else:
            easing_progress = -1 + (4 - 2 * progress) * progress
        move_to_x = round(start_x + x_distance * easing_progress)
        move_to_y = round(start_y + y_distance * easing_progress)
        win32api.SetCursorPos((move_to_x, move_to_y))
        time.sleep(duration / steps)


def click(x, y):  # 点击位置
    pyautogui.click(x, y)


def click_right():  # 右键
    pyautogui.rightClick()


def mouse_slide_down():
    Controller().scroll(0, -10)


def press(key):  # 按键
    pyautogui.press(key)


def hot_key(keys):  # 按键
    pyautogui.hotkey(keys)


def click_text_auto(target_text):  # 平滑点击文字
    __flag = True
    while __flag:
        time.sleep(1)  # 忘记给延迟了
        language_result = _detect_language_status([target_text])
        if language_result == 'ZH':
            temp_results = once_ocr_zh()
        elif language_result == 'EN':
            temp_results = once_ocr_en()
        else:
            raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
        text_list = []
        pos_list = []
        for item in temp_results:
            text_list.append(item['text'])
            ave_pos = average_position(item['position'])  # 别忘了
            pos_list.append(ave_pos)
        for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
            # 应该加一个模糊匹配才对
            if fuzzy_search(target_text.lower(), value.lower()):
                _smooth_move_win32(pos_list[index][0], pos_list[index][1])
                click(pos_list[index][0], pos_list[index][1])
                __flag = False
                break


def click_text_all(target_text):
    __flag = True
    while __flag:
        time.sleep(1)
        language_result = _detect_language_status([target_text])
        if language_result == 'ZH':
            temp_results = once_ocr_zh()
        elif language_result == 'EN':
            temp_results = once_ocr_en()
        else:
            raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
        text_list = []
        pos_list = []
        for item in temp_results:
            text_list.append(item['text'])
            ave_pos = average_position(item['position'])
            pos_list.append(ave_pos)
        for index, value in enumerate(text_list):
            if fuzzy_search(target_text.lower(), value.lower()):
                _smooth_move_win32(pos_list[index][0], pos_list[index][1])
                click(pos_list[index][0], pos_list[index][1])
                __flag = False
                # break # 注释 break 以连续点击多个相同的文字


def click_text_up(target_text):  # 平滑点击文字
    temp = target_text.split(',')  # 文本,50
    target_text = temp[0]
    offset = temp[1]  # 向上为UP，向下为DOWN
    __flag = True
    while __flag:
        time.sleep(1)  # 忘记给延迟了
        language_result = _detect_language_status([target_text])
        if language_result == 'ZH':
            temp_results = once_ocr_zh()  # 获取画面信息
        elif language_result == 'EN':
            temp_results = once_ocr_en()
        else:
            raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
        text_list = []
        pos_list = []
        for item in temp_results:
            text_list.append(item['text'])
            ave_pos = average_position(item['position'])  # 别忘了
            pos_list.append(ave_pos)
        for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
            if fuzzy_search(target_text.lower(), value.lower()):  # 应该加一个模糊匹配才对
                _smooth_move_win32(pos_list[index][0], pos_list[index][1])
                click(pos_list[index][0], pos_list[index][1] - int(offset))
                __flag = False
                break


def click_text_down(target_text):  # 平滑点击文字
    temp = target_text.split(',')  # 文本,50
    target_text = temp[0]
    offset = temp[1]
    __flag = True
    while __flag:
        time.sleep(1)  # 忘记给延迟了
        language_result = _detect_language_status([target_text])
        if language_result == 'ZH':
            temp_results = once_ocr_zh()  # 获取画面信息
        elif language_result == 'EN':
            temp_results = once_ocr_en()
        else:
            raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
        text_list = []
        pos_list = []
        for item in temp_results:
            text_list.append(item['text'])
            ave_pos = average_position(item['position'])  # 别忘了
            pos_list.append(ave_pos)
        for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
            if fuzzy_search(target_text.lower(), value.lower()):  # 应该加一个模糊匹配才对
                _smooth_move_win32(pos_list[index][0], pos_list[index][1])
                click(pos_list[index][0], pos_list[index][1] + int(offset))
                __flag = False
                break


def click_position(position):  # 点击坐标
    x, y = position.split(',')
    x = int(x)  # 没有转换类型导致错误
    y = int(y)
    _smooth_move_win32(x, y)
    click(x, y)


def click_text_area(space, target_text, text_list, pos_list):  # 平滑点击文字
    if space == 'ProgramAndFunction':  # 这里应该使用数据库，但前期简单一点就直接写坐标
        x1, x2, y1, y2 = 250, 1375, 270, 1000  # x应该在x1-x2之间，y同理
    else:
        # TODO 等待测试
        raise ModuleNotFoundError('找不到区域程序!')
    for index, value in enumerate(text_list):
        if target_text in value:  # 这里使用in，因为限制了区域
            if pos_list[index][0] in range(x1, x2) and pos_list[index][1] in range(y1, y2):
                _smooth_move_win32(pos_list[index][0], pos_list[index][1])
                click(pos_list[index][0], pos_list[index][1])
                break


def input_content(target_text):
    old_clip = pyperclip.paste()
    pyperclip.copy(target_text)
    pyautogui.hotkey('ctrl', 'a')  # 新增全选
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy(old_clip)  # 恢复之前的剪切数据


def input_param_content(target_text):  # 这次一定行
    pattern = re.compile(r'\{(\w+)}')

    def replace_variable(match):
        key = match.group(1)  # 提取变量名
        if key in MapValue:
            return MapValue[key]  # 返回字典中对应的值
        else:
            my_logger.error(f"未找到参数 : {{{key}}}")
            raise ValueError(f"未找到参数 : {{{key}}}")

    # 替换字符串中的变量
    result_text = pattern.sub(replace_variable, target_text)
    my_logger.info(f"已替换参数 : {result_text}")
    input_content(result_text)


def input_download(target):  # 传入文件夹名称，默认在 MyWindowsAi/Program
    downloads_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Programs\\{target}')
    input_content(downloads_path)


def input_project(target):  # 传入文件夹名称，默认在 MyWindowsAi/Projects
    project_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Projects\\{target}')
    input_content(project_path)


def click_text_accuracy(target_text, accuracy_info):  # 平滑点击精确文字
    pos_list = []
    for temp_result in accuracy_info:
        text = temp_result['text']
        text_word = temp_result['text_word']
        text_word_region = temp_result['text_word_region']
        if target_text in text:
            full_string = ''.join(text_word)
            start_index = full_string.find(target_text)
            if start_index != -1:
                end_index = start_index + len(target_text)
                for i in range(start_index, end_index):
                    pos_list.append(text_word_region[i])
                ave_list = []
                for item_position in pos_list:
                    ave_pos = average_position(item_position)
                    ave_list.append(ave_pos)
                ave_x = 0
                ave_y = 0
                for item in ave_list:
                    ave_x += item[0]
                    ave_y += item[1]
                x, y = ave_x / len(ave_list), ave_y / len(ave_list)
                _smooth_move_win32(x, y)  # 移动后要点击呢
                click(x, y)
                break


def _click_center():
    # 获取屏幕的宽度和高度
    screen_width, screen_height = pyautogui.size()
    # 计算屏幕中心的坐标
    center_x, center_y = screen_width // 2, screen_height // 2
    # 移动鼠标到屏幕中心并点击
    _smooth_move_win32(center_x, center_y)
    click(center_x, center_y)
