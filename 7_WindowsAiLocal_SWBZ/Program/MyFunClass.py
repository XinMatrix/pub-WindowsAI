import ctypes
import glob
import re
import shlex
import shutil
import subprocess
import sys
import webbrowser
import winreg
from datetime import datetime, timedelta
from pathlib import Path

import keyboard
import openai
import psutil
import pyautogui
import pyperclip
import win32api
import win32com
# import win32com.client
import win32con
import win32gui
# import win32gui
from PIL import Image, ImageDraw, ImageFont, ImageGrab
from moviepy.video.io.VideoFileClip import VideoFileClip

from OCR import start_ocr
from config import last_img, my_logger
# from Data import temp_check

import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib

import tkinter as tk

# 关闭 PyAutoGUI 的安全模式
pyautogui.FAILSAFE = False


class ScreenTextOverlay:
    def __init__(self, initial_text, font_size, text_color, margin_left, margin_bottom):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.8)

        # 设置透明背景
        self.root.attributes('-transparentcolor', 'black')
        self.root.config(bg='black')

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算可用宽度（屏幕宽度减去左右边距）
        available_width = screen_width - margin_left * 2

        self.label = tk.Label(
            self.root,
            text=initial_text,
            font=('Microsoft YaHei', font_size, 'bold'),
            fg=text_color,
            bg='black',  # 使用黑色作为透明色
            padx=0,
            pady=0,
            wraplength=available_width,  # 设置自动换行宽度
            justify='left',  # 左对齐
            anchor='nw'  # 文本对齐方式：西北角（左上角）
        )
        self.label.pack(anchor='w', padx=(margin_left, 0))  # 左对齐并添加左侧边距

        # 计算窗口大小和位置
        self.root.update_idletasks()
        label_height = self.label.winfo_reqheight()

        # 设置窗口位置和大小（整个屏幕宽度，文字高度）
        pos_x = 0  # 从屏幕最左侧开始
        pos_y = screen_height - label_height - margin_bottom  # 底部边距

        self.root.geometry(f"{screen_width}x{label_height}+{pos_x}+{pos_y}")
        self.root.deiconify()

    def update_text(self, new_text):
        """更新显示文字"""
        if hasattr(self, 'label'):
            self.label.config(text=new_text)
            self.root.update_idletasks()

            # 调整窗口高度（保持宽度为屏幕宽度）
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            label_height = self.label.winfo_reqheight()

            # 保持底部边距一致
            pos_y = screen_height - label_height - 10  # 20是默认底部边距
            self.root.geometry(f"{screen_width}x{label_height}+0+{pos_y}")

    def destroy(self):
        """销毁窗口"""
        if hasattr(self, 'root'):
            self.root.destroy()


def sj(a, p=None, v=None):
    # ---------- 0. 让省略 action 时自动按 GET 处理 ----------
    if a not in ('GET', 'SET'):
        p, a, v = a, 'GET', None  # 把第一个实参当作 p

    # ---------- 1. JSON 文件路径 ----------
    file_path = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\Program\MyParameters.json"

    # ---------- 2. 初始化：若文件不存在则写入默认参数 ----------
    if not os.path.exists(file_path):
        temp_params = {
            'DateFilepath': '',
            'VideoLink': '',
            'JijidownPath': r'D:\myJiJiDown\JiJiDownForWPF.exe',
            'MumuPath': r'D:\myMuMu\MuMu Player 12\shell\MuMuPlayer.exe',
            'BuildVideoPath': r'C:\Users\USER\Documents\MuMu共享文件夹\Movies',
            'json_path': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\GPT生成内容.json',
            'XiaoHongShu': 'https://creator.xiaohongshu.com/publish/publish?from=menu',
            'ShiPinHao': 'https://channels.weixin.qq.com/platform/post/create',
            'DouYin': 'https://creator.douyin.com/creator-micro/content/upload',
            'BaiJiaHao': 'https://baijiahao.baidu.com/builder/rc/edit?type=videoV2&is_from_cms=1',
            'BZhan': 'https://member.bilibili.com/platform/upload/video/frame',
            'VideoPath': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\导出视频.mp4',
            'CoverPath': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\封面.png',
            'TempFolder': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作',
            'FinishedVideo': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\已完成视频.txt',
            'UnFinishedVideo': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\未完成视频.txt',
            'ReadyToUpload': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\待发布视频',
            'FontPath': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\阿里妈妈东方大楷.ttf',
            'StartEndTime': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\裁剪视频时间戳.txt',
            'VideoNoAudio': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\裁剪空镜.mp4',
            'VideoAsset': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\超长空镜素材.mp4',  # 不小心错删了这个，好嘛，现在没视频素材了
            'AudioWithSubtitles': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\音频带字幕.mp4',
            'RawTextFolder': r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\原文文字稿',
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(temp_params, f, indent=4, ensure_ascii=False)
        my_logger.info("JSON 文件已创建并写入默认参数。")

    # ---------- 3. 读取当前配置 ----------
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ---------- 4. GET / SET ----------
    if a == 'GET':
        result = data.get(p)
        my_logger.info(f"参数读取成功：{p}={result}")
        return result

    elif a == 'SET':
        data[p] = v
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        my_logger.info(f"参数 {p} 已更新为：{v}")

    else:
        raise ValueError("无效的 action 参数，只能是 GET 或 SET")


def start_action(results, action_string, user_message, temp_ocr_text=None, temp_ocr_position=None,
                 temp_ocr_accuracy_outputs=None):
    action_list = action_string.split('->')  # 还是用箭头吧，因为有些函数名字比较长，KeyWord也是
    overlay = ScreenTextOverlay(
        initial_text="初始化",
        font_size=10,
        text_color='white',
        margin_left=10,  # 左侧边距20像素
        margin_bottom=10  # 底部边距20像素
    )
    i = 1
    formatted_str = "\n".join(f"{i} : {s}" for i, s in enumerate(action_list, 1))
    my_logger.info(f"操作列表:\n{formatted_str}")
    for action in action_list:
        temp_show = re.sub(r'%[^%]*%', '<模糊搜索>', action)  # 替换%LOCAL%为<模糊搜索> 如果有%XXX%的话
        overlay.update_text(f"正在执行 | {i}/{len(action_list)} | {temp_show}")

        # 动态输出进度条
        def ascii_bar(k, total, width=30):
            filled = int(width * k / total)
            return '▶' * filled + '·' * (width - filled)

        bar = ascii_bar(i, len(action_list))  # \r 回到行首覆盖，end='' 防止换行，flush 强制刷新
        sys.stdout.write(f"\r|{bar}|")

        i += 1
        time.sleep(0.25)  # 每一个动作的执行时间间隔

        # 按键
        if re.search(r"\bKEY\((.*?)\)", action):  # Nice 使用正则匹配减小工作量——加\b是为了完全有且仅有匹配模式
            target = re.search(r"\bKEY\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：按键'} : {target}")  # 原来要区分引号要
            MyFun.Input.press(target)

        # 复制
        elif re.search(r"\bCOPY\((.*?)\)", action):
            target = re.search(r"\bCOPY\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制'} : {target}")
            MyFun.Input.copy(target)

        # 输入内容
        elif re.search(r"\bINPUT\((.*?)\)", action):
            target = re.search(r"\bINPUT\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：输入'} : {target}")
            MyFun.Input.input_content(target)

        # 组合键
        elif re.search(r"\bHOTKEY\((.*?)\)", action):
            target = re.search(r"\bHOTKEY\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：热键'} : {target}")
            if target == 'CTRL++':
                keys = ['CTRL', '+']
            else:
                keys = target.split('+')
            lowercase_keys = [key.lower() for key in keys]  # 转换为小写防止按住Shift模拟大小——这个是必要的
            MyFun.Input.hot_key(lowercase_keys)

        # OCR点击文本
        elif re.search(r"\bCLICK_TEXT\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：点击文本'} : {target}")
            # MyFun.Input.click_text(target, temp_ocr_text, temp_ocr_position)
            MyFun.Input.click_text(target)

        # elif re.search(r"\bMOVE_TO_TEXT\((.*?)\)", action):
        #     target = re.search(r"\bMOVE_TO_TEXT\((.*?)\)", action).group(1)
        #     my_logger.info(f"{'匹配操作：移动到文本'} : {target}")
        #     MyFun.Input.move_to_text(target)

        elif re.search(r"\bCLICK_TEXT_TOP\((.*?)\)", action):
            content = re.search(r"\bCLICK_TEXT_TOP\((.*?)\)", action).group(1)
            params = [p.strip() for p in content.split(',')]
            my_logger.info(f"{f'匹配操作：点击文本{params[0]} 向上偏移{params[1]}像素'} : {content}")
            MyFun.Input.click_text_top(params[0], params[1])  # 可以使用*解包参数

        elif re.search(r"\bCLICK_TEXT_RIGHT\((.*?)\)", action):
            content = re.search(r"\bCLICK_TEXT_RIGHT\((.*?)\)", action).group(1)
            params = [p.strip() for p in content.split(',')]
            my_logger.info(f"{f'匹配操作：点击文本{params[0]} 向右偏移{params[1]}像素'} : {content}")
            MyFun.Input.click_text_right(params[0], params[1])  # 可以使用*解包参数

        elif re.search(r"\bCLICK_TEXT_LEFT\((.*?)\)", action):
            content = re.search(r"\bCLICK_TEXT_LEFT\((.*?)\)", action).group(1)
            params = [p.strip() for p in content.split(',')]
            my_logger.info(f"{f'匹配操作：点击文本{params[0]} 向右左偏移{params[1]}像素'} : {content}")
            MyFun.Input.click_text_left(params[0], params[1])  # 可以使用*解包参数

        # FIXME 测试中 按区域点击
        elif re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action):
            # target = re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action).group(1)  # TODO 识别出两个参数
            target = re.search(r"\bCLICK_TEXT_AREA\((.*?),(.*?)\)", action)
            t1 = target.group(1)  # 区域程序名称
            t2 = target.group(2)  # 点击文字
            my_logger.info(f"{'匹配操作：点击区域文本'} : {target}")
            MyFun.Input.click_text_area(t1, t2, temp_ocr_text, temp_ocr_position)

        # 点击精确文字
        elif re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：点击精确文本'} : {target}")
            MyFun.Input.click_text_accuracy(target, temp_ocr_accuracy_outputs)

        # 使用默认浏览器打开网址
        elif re.search(r"\bWEB_BROWSER\((.*?)\)", action):
            target = re.search(r"\bWEB_BROWSER\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：打开浏览器'} : {target}")
            MyFun.System.open_web(target)

        # 使用默认浏览器打开网址
        elif re.search(r"\bWEB_BROWSER_EDGE\((.*?)\)", action):
            target = re.search(r"\bWEB_BROWSER_EDGE\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：打开EDGE浏览器'} : {target}")
            MyFun.System.open_web_edge(target)

        # 精准搜索打开 MyWindowsAi/Downloads/ 下文件
        elif re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action):
            target = re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：打开下载内容'} : {target}")
            MyFun.System.open_downloaded(target)

        # 打开已安装程序，系统或 MyWindowsAi/Program/ 下程序
        elif re.search(r"\bOPEN_INSTALLED\((.*?)\)", action):  # 模糊匹配已安装程序
            target = re.search(r"\bOPEN_INSTALLED\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：打开安装程序'} : {target}")
            MyFun.System.open_installed(target)

        elif re.search(r"\bSTART_PROGRAM_BY_PATH\((.*?)\)", action):  # 模糊匹配已安装程序
            target = re.search(r"\bSTART_PROGRAM_BY_PATH\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：通过地址打开程序'} : {target}")
            MyFun.System.start_program_by_path(target)

        # 打开系统程序，如用户帐户控制、程序和功能
        elif re.search(r"\bOPEN_SYSTEM\((.*?)\)", action):  # 打开系统程序
            target = re.search(r"\bOPEN_SYSTEM\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：打开系统程序'} : {target}")
            MyFun.System.open_system(target)

        # 设置程序焦点
        elif re.search(r"\bSET_FOCUS\((.*?)\)", action):  # 普通切换
            target = re.search(r"\bSET_FOCUS\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：设置焦点'} : {target}")
            check = True
            while check:
                time.sleep(1)
                check = MyFun.System.switch_to_windows(target)  # 循环检测

        # 设置全屏焦点
        elif re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action):  # 全屏切换——有点问题，Chrome安装和普通程序都会被打开隐藏
            target = re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：设置焦点并全屏'} : {target}")
            check = True
            while check:
                time.sleep(1)
                check = MyFun.System.switch_to_windows_full(target)  # 循环检测

        # 小睡一会
        elif re.search(r"\bSLEEP\((.*?)\)", action):
            target = re.search(r"\bSLEEP\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：睡眠'} : {target}")
            MyFun.Fun.delay(target)

        # 点击——无参函数
        elif re.search(r"\bCLICK\((.*?)\)", action):
            my_logger.info(f"{'匹配操作：点击'} : {action}")
            MyFun.Fun.click()

        # 关闭运行窗口/清理后台程序
        elif re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action):
            target = re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：关闭程序窗口'} : {target}")
            MyFun.Fun.close_windows(target)

        # 输入安装目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action):  # 下载程序文件，默认保存在MyWindowsAi/Download目录下
            target = re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：输入安装地址'} : {target}")
            MyFun.Input.input_download(target)

        # 输入项目目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_PROJECT\((.*?)\)", action):
            target = re.search(r"\bINPUT_PROJECT\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：输入项目地址'} : {target}")
            MyFun.Input.input_project(target)

        elif re.search(r"\bGOTO\((.*?)\)", action):
            target = re.search(r"\bGOTO\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：跳转'} : {target}")
            # 先查找，再执行 Nice
            for y in results:  # 这个是必中的
                if y[0] == target:  # 这里需要修改，一直是这里报错，注意，将 2 改为 0 ， 将 3 改为 1
                    start_action(results, y[1], my_logger, user_message)
                    break

        # 循环OCR，并等待检测target
        elif re.search(r"\bWAIT_OCR\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR\((.*?)\)", action).group(1)  # 下载管理
            my_logger.info(f"{'匹配操作：等待文本出现'} : {target}")
            temp = 1
            while True:
                temp += 1
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break

        # 循环OCR，并等待检测target
        elif re.search(r"\bWAIT_OCR_F5\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR_F5\((.*?)\)", action).group(1)  # 下载管理
            my_logger.info(f"{'匹配操作：等待文本出现，长时间将刷新网页'} : {target}")
            temp = 1
            while True:
                temp += 1
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break
                if temp % 20 == 0:  # TODO 测试一下
                    MyFun.Input.press('F5')  # 按下f5刷新

        elif re.search(r"\bWAIT_OCR_END\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR_END\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：等待文本出现并消失'} : {target}")
            while True:  # 等待文本出现
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break
            while True:  # 等待文本消失
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                if not any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break

        # SELECT_OCR() 匹配数据库OCR 如 OCR(%ABC%)
        elif action == 'SELECT_OCR()':
            _Flag = True
            my_logger.info(f"{'匹配操作：特征文本转操作'} : {action}")
            target_list = []
            action_list = []
            for y in results:  # 这个是必中的
                if re.search(r"\bOCR\((.*?)\)", y[0]):
                    target = re.search(r"\bOCR\((.*?)\)", y[0]).group(1)
                    target_list.append(target)
                    action_list.append(y[1])
            while _Flag:
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                for x in ocr_outputs:
                    for index, y in enumerate(target_list):
                        if MyFun.Fun.fuzzy_search(y, x['text']):
                            _Flag = False
                            start_action(results, action_list[index], my_logger, user_message)

        elif re.search(r"\bMOVE_FILE\((.*?)\)", action):
            target = re.search(r"\bMOVE_FILE\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：移动文件'} : {target}")
            MyFun.System._move_file(target)

        elif re.search(r"\bAUDIO_2_TEXT_BY_API\((.*?)\)", action):
            target = re.search(r"\bAUDIO_2_TEXT_BY_API\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：语音转文本'} : {target}")
            MyFun.Fun.audio_2_text_by_api(target)

        elif re.search(r"\bSTART_GPT_API\((.*?)\)", action):
            target = re.search(r"\bSTART_GPT_API\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：GPT文本生成内容'} : {target}")
            MyFun.Fun.start_gpt_api(target)

        # elif re.search(r"\bSTART_GPT_API_TO_WECHAT_ARTICLE\((.*?)\)", action):
        #     target = re.search(r"\bSTART_GPT_API_TO_WECHAT_ARTICLE\((.*?)\)", action).group(1)
        #     my_logger.info(f"{'匹配操作：GPT生成微信文章'} : {target}")
        #     MyFun.Fun.start_gpt_api_to_wechat_article(target)

        elif re.search(r"\bGENERATE_COVER\((.*?)\)", action):
            target = re.search(r"\bGENERATE_COVER\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：文字生成封面'} : {target}")
            MyFun.Fun.generate_cover(target)

        elif re.search(r"\bCOPY_TEXT_FROM_JSON\((.*?)\)", action):
            target = re.search(r"\bCOPY_TEXT_FROM_JSON\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制文本'} : {target}")
            MyFun.Fun.copy_content_from_json(target, 'text')

        elif re.search(r"\bCOPY_TITLE_FROM_JSON\((.*?)\)", action):
            target = re.search(r"\bCOPY_TITLE_FROM_JSON\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制标题'} : {target}")
            MyFun.Fun.copy_content_from_json(target, 'title')

        elif re.search(r"\bCOPY_INTRODUCTION_FROM_JSON\((.*?)\)", action):
            target = re.search(r"\bCOPY_INTRODUCTION_FROM_JSON\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制简介'} : {target}")
            MyFun.Fun.copy_content_from_json(target, 'introduction')

        elif re.search(r"\bCOPY_BAIJIAHAO_FROM_JSON\((.*?)\)", action):
            target = re.search(r"\bCOPY_BAIJIAHAO_FROM_JSON\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制简介'} : {target}")
            MyFun.Fun.copy_content_from_json(target, 'BaiJiaHao')

        elif re.search(r"\bCOPY_NOTAGS_FROM_JSON\((.*?)\)", action):
            target = re.search(r"\bCOPY_NOTAGS_FROM_JSON\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：复制简介'} : {target}")
            MyFun.Fun.copy_content_from_json(target, 'NoTAGS')

        elif re.search(r"\bINPUT_LABELS_AND_KEY_ENTER\((.*?)\)", action):
            target = re.search(r"\bINPUT_LABELS_AND_KEY_ENTER\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：输入标签并回车'} : {target}")
            MyFun.Fun.input_labels_and_key_enter(target)

        # elif re.search(r"\bCLICK_XHS_LABEL\((.*?)\)", action):
        #     target = re.search(r"\bCLICK_XHS_LABEL\((.*?)\)", action).group(1)
        #     my_logger.info(f"{'匹配操作：点击小红书标签'} : {target}")
        #     MyFun.Fun.click_xhs_label(target)

        elif re.search(r"\bINPUT_BZHAN_TAGS\((.*?)\)", action):
            target = re.search(r"\bINPUT_BZHAN_TAGS\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：点击B站标签'} : {target}")
            MyFun.Fun.input_bzhan_tags(target)

        elif re.search(r"\bCLICK_POSITION\((.*?)\)", action):
            content = re.search(r"\bCLICK_POSITION\((.*?)\)", action).group(1)
            params = [p.strip() for p in content.split(',')]
            my_logger.info(f"{f'匹配操作：点击坐标:{params[0]},{params[1]}'} : {action}")
            MyFun.Fun.click_position(params[0], params[1])  # 可以使用*解包参数

        elif re.search(r"\bMOVE_TO_MAKE\((.*?)\)", action):
            target = re.search(r"\bMOVE_TO_MAKE\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：移动视频至制作位置'} : {target}")
            MyFun.Fun.move_to_make(target)

        elif re.search(r"\bCUT_VIDEO\((.*?)\)", action):
            target = re.search(r"\bCUT_VIDEO\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：移动视频至制作位置'} : {target}")
            MyFun.Fun.cut_video()

        elif re.search(r"\bROLL_TO\((.*?)\)", action):
            target = re.search(r"\bROLL_TO\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：滚轮至指定位置'} : {target}")
            MyFun.Fun.roll_to(target)

        elif re.search(r"\bTAG\((.*?)\)", action):
            target = re.search(r"\bTAG\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：正在运行操作流'} : {target}")

        elif re.search(r"\bMOVE_MOUSE_TO_TOP\((.*?)\)", action):
            target = re.search(r"\bMOVE_MOUSE_TO_TOP\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：向上移动鼠标'} : {target}")
            MyFun.Fun.move_mouse_to_top(target)

        elif re.search(r"\bWAIT_MP3\((.*?)\)", action):
            target = re.search(r"\bWAIT_MP3\((.*?)\)", action).group(1)
            my_logger.info(f"{'匹配操作：等待MP3文件出现'} : {target}")
            MyFun.Fun.wait_mp3(target)

        elif action == 'PAST_TEXT()':  # 无参函数
            my_logger.info(f"{'匹配操作：粘贴文本'} : {action}")
            MyFun.Fun.past_text()

        elif action == 'CLICK_RIGHT()':  # 无参函数
            my_logger.info(f"{'匹配操作：右键'} : {action}")
            MyFun.Input.click_right()

        elif action == 'FINISH()':  # 无参函数
            my_logger.info(f"{'匹配操作：程序结束'} : {action}")
            MyFun.System.finish()

        elif action == 'FINISH_BACK()':  # 无参函数
            my_logger.info(f"{'匹配操作：程序结束'} : {action}")
            MyFun.System.finish_back()

        elif action == 'CREATE_FINAL_VIDEO()':
            my_logger.info(f"{'匹配操作：生成视频'} : {action}")
            MyFun.Fun.create_final_video()

        elif action == 'CLICK_SCREEN_CENTER()':
            my_logger.info(f"{'匹配操作：点击屏幕中心'} : {action}")
            MyFun.Fun.click_screen_center()

        elif action == 'ROLL_TO_BOTTOM()':
            my_logger.info(f"{'匹配操作：滚轮至底部'} : {action}")
            MyFun.Fun.roll_to_bottom()

        elif action == 'INIT_FILES()':
            my_logger.info(f"{'匹配操作：初始化文件'} : {action}")
            MyFun.Fun.init_files()

        elif action == 'GIT_REPO()':
            my_logger.info(f"{'匹配操作：提交git仓库'} : {action}")
            MyFun.Fun.git_repo()

        elif action == 'UPDATE_VIDEO_PATH()':
            my_logger.info(f"{'匹配操作：更新明天的视频路径'} : {action}")
            MyFun.Fun.update_video_path()

        elif action == 'COPY_VIDEO_TO_FOLDER()':
            my_logger.info(f"{'匹配操作：复制生成视频内容到指定文件夹'} : {action}")
            MyFun.Fun.copy_video_to_folder()

        elif action == 'DELETE_MIDDLE_FILES()':
            my_logger.info(f"{'匹配操作：删除中间文件'} : {action}")
            MyFun.Fun.delete_middle_files()

        else:
            text = f"{'操作未定义'} : {action}"
            my_logger.critical(text)
            raise ModuleNotFoundError(text)

    overlay.destroy()


class MyFun:
    class System:  # 系统预处理

        @staticmethod
        def get_all_programs_from_start_menu():  # 这个是检测不到安装包的
            start_menu_dirs = [
                os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
                os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs")
            ]
            all_programs = []
            for directory in start_menu_dirs:
                program_list = []
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.lower().endswith(".lnk"):
                            shortcut_path = os.path.join(root, file)
                            shell = win32com.client.Dispatch("WScript.Shell")
                            shortcut = shell.CreateShortcut(shortcut_path)
                            target_path = shortcut.Targetpath
                            if target_path and os.path.exists(target_path):
                                program_list.append(target_path)
                all_programs.extend(program_list)
            return all_programs

        @staticmethod
        def _get_running_windows():  # 枚举当前正在运行的所有窗口
            def callback(tmp_hwnd, tmp_windows):
                if win32gui.IsWindowVisible(tmp_hwnd) and win32gui.GetWindowText(tmp_hwnd):
                    tmp_windows.append((tmp_hwnd, win32gui.GetWindowText(tmp_hwnd)))
                return True

            windows_list = []
            win32gui.EnumWindows(callback, windows_list)
            return windows_list

        @staticmethod
        def run_cmd(tmp_cmd):
            result = subprocess.run(tmp_cmd, capture_output=True, text=True, shell=True)
            return result.stdout

        @staticmethod
        def _get_installed_programs():
            installed_programs = []
            reg_flags = winreg.KEY_READ | winreg.KEY_WOW64_32KEY  # 64位系统下访问32位注册表需要加上 winreg.KEY_WOW64_32KEY 标志
            try:
                reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, reg_flags) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            try:
                                program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                                installed_programs.append(program_name)
                            except FileNotFoundError:
                                continue
            except Exception as e:
                my_logger.error(f"{'获取已安装程序时发生错误'} {e}")
            try:
                reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, reg_flags) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            try:
                                program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                                if program_name not in installed_programs:
                                    installed_programs.append(program_name)
                            except FileNotFoundError:
                                continue
            except Exception as e:
                my_logger.error(f"{'获取已安装程序时发生错误'} {e}")
            return installed_programs

        @staticmethod
        def is_admin():  # 判断是否为管理员，因非管理员打开会导致程序无效
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except OSError:  # 未测试 OSError
                return False

        @staticmethod
        def kill_processes(processes_name):  # 关闭程序进程
            running_processes = psutil.process_iter()
            for process in running_processes:
                if process.name() == processes_name:  # Photos.exe
                    process.terminate()  # 发送终止信号
                    process.wait()  # 等待进程终止

        @staticmethod
        def switch_to_windows(name_like):
            windows = MyFun.System._get_running_windows()
            my_logger.info(f"{'找到程序窗口'} : {windows}")
            for hwnd, title in windows:
                if name_like in title:  # 模糊搜索，其实也可以精准搜索，只要字足够多
                    my_logger.info(f"{'切换到程序窗口'} : {title}")  # 多了一个大括号。。
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 原设置
                    win32gui.SetForegroundWindow(hwnd)  # 执行操作
                    time.sleep(1)  # 给点延迟，防止下一步时程序没有反应过来
                    return False  # 正常返回False，终止循环
            return True

        @staticmethod
        def switch_to_windows_full(name_like):
            windows = MyFun.System._get_running_windows()
            for hwnd, title in windows:
                if name_like in title:  # 模糊搜索
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 最大化
                    win32gui.SetForegroundWindow(hwnd)  # 执行操作
                    return False  # 正常返回False，终止循环
            return True

        @staticmethod
        def open_web(target_url):  # 以默认方式打开浏览器
            webbrowser.open(target_url)

        @staticmethod
        def open_web_edge(target_url):
            edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
            subprocess.Popen([edge_path, target_url])

        @staticmethod
        def open_downloaded(target_exe):  # 下载安装程序
            downloads_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Downloads')
            if os.path.exists(downloads_path):  # 检查下载文件夹是否存在
                for item in os.listdir(downloads_path):  # 遍历下载文件夹中的所有项
                    # if target_exe in item:  # ChromeSetup.exe
                    if target_exe == item:  # ChromeSetup.exe
                        target_path = os.path.join(downloads_path, item)
                        os.startfile(target_path)  # 这个更具通用性 Nice
                        break

        @staticmethod
        def open_installed(target_exe):  # 快速打开程序，自带SetFocus
            programs = MyFun.System.get_all_programs_from_start_menu()
            for program in programs:
                if target_exe in program:
                    os.startfile(program)
                    break

        @staticmethod
        def start_program_by_path(target_like):  # 启动程序，模糊搜索
            subprocess.Popen(target_like)

        @staticmethod
        def open_system(target_exe):
            if target_exe == 'UserAccountControlSettings':
                subprocess.Popen(r'C:\Windows\System32\UserAccountControlSettings.exe')  # 可以先写个检测程序检测这些路径是否存在
                time.sleep(0.2)  # 时间不确定，等待实战测试
                MyFun.System.switch_to_windows('用户帐户控制设置')  # 切换焦点，稳妥起见
            # 默认在下载位置，所以遍历下载文件查找
            elif target_exe == 'ProgramAndFunction':
                subprocess.call('appwiz.cpl', shell=True)  # 这个是打开卸载，比系统自带的好用
                time.sleep(0.2)
                MyFun.System.switch_to_windows('程序和功能')  # 已验证

        @staticmethod
        def check_exe_exists(target):  # 检查文件是否存在
            exist_exe_list = MyFun.System._get_installed_programs()
            if target in exist_exe_list:
                # TODO 未测试
                my_logger.info(f"{'检测到已安装程序'} : {target}")

        @staticmethod
        def finish():
            time.sleep(1)
            MyFun.System.kill_processes('Photos.exe')  # 推荐使用精准关闭
            my_logger.info(f"{'程序已结束'}")

        @staticmethod
        def finish_back():
            time.sleep(1)
            MyFun.System.kill_processes('Photos.exe')  # 推荐使用精准关闭
            my_logger.info(f"{'程序已结束'}")
            pyautogui.hotkey('alt', 'tab')

        @staticmethod
        def _move_file(target):
            _from = target.split(',')[0]  # cudnn-windows-x86_64-8.9.7.29_cuda12-archive\\include
            _to = target.split(',')[1]  # C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6
            # 源 include 文件夹的完整路径
            source_dir = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Downloads\\{_from}')
            # 目标路径，直接复制 include 文件夹到此路径下
            dest_dir = os.path.join(_to, os.path.basename(_from))
            # 确保目标路径存在
            os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
            # 移动 include 文件夹到目标路径
            try:
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)  # 文件存在则直接覆盖
            except Exception as e:  # 移动不成功会报错，所以可信度比较高
                my_logger.error(f"{'移动文件时发生错误'} {e}")

    class Init:  # 程序预处理

        @staticmethod
        def create_directories(base_dir, sub_dirs):  # 这里不使用log，因为还没有新建文件夹
            desktop_path = Path.home() / "Desktop"
            base_dir_path = desktop_path / base_dir
            if not os.path.exists(base_dir_path):  # 创建基础文件夹
                os.makedirs(base_dir_path)
            for sub_dir in sub_dirs:  # 创建子文件夹
                dir_path = base_dir_path / sub_dir
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

        @staticmethod
        def _draw_bg_img(path):  # 绘制背景图片
            width, height = pyautogui.size()
            background_color = (64, 64, 64)  # 深灰色
            image = Image.new('RGB', (width, height), background_color)
            draw = ImageDraw.Draw(image)
            text = "WindowsAi"
            font_size = 200
            font_color = (255, 255, 255)  # 白色
            font = ImageFont.truetype("arial.ttf", font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            draw.text((text_x, text_y), text, fill=font_color, font=font)
            image.save(path)

        @staticmethod
        def show_bg():  # 打开背景图像
            img_path = os.path.join(os.path.expanduser('~'),
                                    f'Desktop\\MyWindowsAi\\Configs\\BG_WindowsAi.png')  # 路径错误，所以打开不对
            time.sleep(1)
            subprocess.Popen(['explorer', img_path])  # 使用explorer打开图片
            # time.sleep(3)  # 给几秒让他加载会——因为不确定打开时间——要不要写个程序专门监听——不行，尝试失败
            time.sleep(2.5)  # 给几秒让他加载会——因为不确定打开时间——要不要写个程序专门监听——不行，尝试失败
            pyautogui.hotkey('F11')  # 虚拟机没有全屏快捷键，只在最右下角有

    class Input:
        @staticmethod
        def average_position(points):
            sum_x = 0
            sum_y = 0
            for point in points:
                sum_x += point[0]
                sum_y += point[1]
            avg_x = sum_x / len(points)
            avg_y = sum_y / len(points)
            return avg_x, avg_y

        @staticmethod
        def _smooth_move_win32(x, y, duration=1, steps=100):  # 平滑移动——最快一秒，你自己看着办吧
            start_x, start_y = win32api.GetCursorPos()
            x_distance = int(x) - start_x
            y_distance = int(y) - start_y
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

        @staticmethod
        def click(x, y):  # 点击位置
            pyautogui.click(x=int(x), y=int(y))  # 不知道是不是这里把数字解释成了文件名——不是这个
            # pyautogui.click(x, y)  # 不知道是不是这里把数字解释成了文件名
            # 。。。。。。。。。。。。。我说有什么bug呢，原来是这里。。。。。。

        @staticmethod
        def click_right():  # 右键
            pyautogui.rightClick()

        @staticmethod
        def press(key):  # 按键
            pyautogui.press(key)

        @staticmethod
        def hot_key(keys):  # 按键
            pyautogui.hotkey(keys)

        @staticmethod
        # def click_text(target_text, text_list, pos_list):  # 平滑点击文字
        def click_text(target_text):  # 平滑点击文字
            # 为什么之前没有while True
            __flag = True
            while __flag:
                time.sleep(1)  # 忘记给延迟了
                temp_results = MyFun.Fun.once_ocr()
                text_list = []
                pos_list = []
                for item in temp_results:
                    text_list.append(item['text'])
                    ave_pos = MyFun.Input.average_position(item['position'])  # 别忘了
                    pos_list.append(ave_pos)
                for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
                    # 应该加一个模糊匹配才对
                    if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
                        # if value.lower() == target_text.lower():  # 注意小写——仅在对比时使用小写
                        MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
                        time.sleep(0.25)  # 防止移动中点击。。
                        MyFun.Input.click(pos_list[index][0], pos_list[index][1])
                        __flag = False
                        break

        # @staticmethod
        # def move_to_text(target_text):
        #     __flag = True
        #     while __flag:
        #         time.sleep(1)  # 忘记给延迟了
        #         temp_results = MyFun.Fun.once_ocr()
        #         text_list = []
        #         pos_list = []
        #         for item in temp_results:
        #             text_list.append(item['text'])
        #             ave_pos = MyFun.Input.average_position(item['position'])  # 别忘了
        #             pos_list.append(ave_pos)
        #         for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
        #             # 应该加一个模糊匹配才对
        #             if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
        #                 # if value.lower() == target_text.lower():  # 注意小写——仅在对比时使用小写
        #                 MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
        #                 time.sleep(0.5)  # 防止移动中点击。。
        #                 MyFun.Input.click(pos_list[index][0], pos_list[index][1])
        #                 __flag = False
        #                 break

        @staticmethod
        def click_text_top(target_text, offset_y=0):  # 添加offset_y参数，默认值为0（不偏移）
            __flag = True
            while __flag:
                time.sleep(1)  # 延迟防止CPU占用过高
                temp_results = MyFun.Fun.once_ocr()
                text_list = []
                pos_list = []
                for item in temp_results:
                    text_list.append(item['text'])
                    ave_pos = MyFun.Input.average_position(item['position'])
                    pos_list.append(ave_pos)
                for index, value in enumerate(text_list):
                    if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
                        x, y = pos_list[index]
                        # 应用向上偏移
                        y -= float(offset_y)  # 减去偏移量实现向上移动——注意这里要转换类型
                        MyFun.Input._smooth_move_win32(x, y)
                        MyFun.Input.click(x, y)
                        __flag = False
                        break

        @staticmethod
        def click_text_right(target_text, offset_x=0):  # 改为 offset_x，默认值为0
            __flag = True
            while __flag:
                time.sleep(1)  # 延迟防止CPU占用过高
                temp_results = MyFun.Fun.once_ocr()
                text_list = []
                pos_list = []
                for item in temp_results:
                    text_list.append(item['text'])
                    ave_pos = MyFun.Input.average_position(item['position'])
                    pos_list.append(ave_pos)
                for index, value in enumerate(text_list):
                    if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
                        x, y = pos_list[index]
                        x += float(offset_x)  # 加上偏移量实现向右移动
                        MyFun.Input._smooth_move_win32(x, y)
                        MyFun.Input.click(x, y)
                        __flag = False
                        break

        @staticmethod
        def click_text_left(target_text, offset_x=0):  # 改为 offset_x，默认值为0
            __flag = True
            while __flag:
                time.sleep(1)  # 延迟防止CPU占用过高
                temp_results = MyFun.Fun.once_ocr()
                text_list = []
                pos_list = []
                for item in temp_results:
                    text_list.append(item['text'])
                    ave_pos = MyFun.Input.average_position(item['position'])
                    pos_list.append(ave_pos)
                for index, value in enumerate(text_list):
                    if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
                        x, y = pos_list[index]
                        x -= float(offset_x)  # 减去偏移量实现向左移动
                        MyFun.Input._smooth_move_win32(x, y)
                        MyFun.Input.click(x, y)
                        __flag = False
                        break

        @staticmethod
        def click_text_area(space, target_text, text_list, pos_list):  # 平滑点击文字
            if space == 'ProgramAndFunction':  # 这里应该使用数据库，但前期简单一点就直接写坐标
                x1, x2, y1, y2 = 250, 1375, 270, 1000  # x应该在x1-x2之间，y同理
            else:
                raise ModuleNotFoundError('找不到区域程序!')
            for index, value in enumerate(text_list):
                if target_text in value:  # 这里使用in，因为限制了区域
                    if pos_list[index][0] in range(x1, x2) and pos_list[index][1] in range(y1, y2):
                        MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
                        MyFun.Input.click(pos_list[index][0], pos_list[index][1])
                        break

        @staticmethod
        def copy(input_text):
            pyperclip.copy(input_text)

        @staticmethod
        def input_content(target_text):
            old_clip = pyperclip.paste()
            pyperclip.copy(target_text)
            pyautogui.hotkey('ctrl', 'a')  # 新增全选
            pyautogui.hotkey('ctrl', 'v')
            pyperclip.copy(old_clip)  # 恢复之前的剪切数据

        @staticmethod
        def input_download(target):  # 传入文件夹名称，默认在 MyWindowsAi/Program
            downloads_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Programs\\{target}')
            MyFun.Input.input_content(downloads_path)

        @staticmethod
        def input_project(target):  # 传入文件夹名称，默认在 MyWindowsAi/Projects
            project_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Projects\\{target}')
            MyFun.Input.input_content(project_path)

        @staticmethod
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
                            ave_pos = MyFun.Input.average_position(item_position)
                            ave_list.append(ave_pos)
                        ave_x = 0
                        ave_y = 0
                        for item in ave_list:
                            ave_x += item[0]
                            ave_y += item[1]
                        x, y = ave_x / len(ave_list), ave_y / len(ave_list)
                        MyFun.Input._smooth_move_win32(x, y)  # 移动后要点击呢
                        MyFun.Input.click(x, y)
                        break

    class Fun:

        @staticmethod
        def delete_middle_files():
            def remove_file_by_key(keys):
                for key in keys:
                    try:
                        file_path = sj(key)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            my_logger.info(f"已删除：{file_path}")
                        else:
                            my_logger.warning(f"文件不存在或不是常规文件：{file_path}")
                    except Exception as e:
                        my_logger.error(f"删除 {key} 对应文件失败：{e}")

            # 删除中间文件——虽然AudioWithSubtitles永远删不掉，努力了
            # remove_file_by_key(['AudioWithSubtitles', 'VideoNoAudio', 'CoverPath'])  # VideoAsset不是中间文件.........
            remove_file_by_key(['VideoNoAudio', 'CoverPath'])  # VideoAsset不是中间文件.........

        # 音频带字幕文件在使用，最后再删除

        @staticmethod
        def update_video_path():
            finished_video_path = sj('FinishedVideo')
            unfinished_video_path = sj('UnFinishedVideo')
            # 读取未完成视频.txt的第一条信息
            with open(unfinished_video_path, 'r', encoding='utf-8') as file:
                first_line = file.readline()
            text = first_line.strip().split(' ')  # ['2023-6-25', 'BV1aV411u7mA', '拒绝电池思维——认清现实，理性看待上学和找工作']
            # 复制文本到已完成视频.txt
            with open(finished_video_path, 'a', encoding='utf-8') as file:
                file.write(
                    f"{datetime.now().strftime("%Y-%m-%d")} | {text[0]} {text[1]} {text[2]}\n")  # 写入已完成视频.txt的最后一行
            # 删除未完成视频.txt的第一条信息
            with open(unfinished_video_path, 'r', encoding="utf-8") as file:
                lines = file.readlines()  # 注意readline()和readlines()的区别
            with open(unfinished_video_path, 'w', encoding="utf-8") as file:
                file.writelines(lines[1:])  # 从第二行开始写入
            sj('SET', 'VideoLink', f"https://www.bilibili.com/video/{text[1]}/")

        # JiJiDown会使用.temp下载
        @staticmethod
        def wait_mp3(folder_path):
            while True:
                files = os.listdir(folder_path)
                mp3_files = [f for f in files if f.lower().endswith(".mp3")]
                temp_files = [f for f in files if f.lower().endswith(".temp")]
                if mp3_files and not temp_files:  # 条件满足：有 mp3，且没有 .temp
                    my_logger.info(f"发现 mp3 文件且未检测到 .temp：{mp3_files}，准备继续…")
                    break
                time.sleep(1)

        @staticmethod
        def move_mouse_to_top(value):
            pyautogui.moveRel(0, -int(value))  # 向上移动500像素，0表示横向不动

        @staticmethod
        def roll_to(target):
            pyautogui.scroll(int(target))

        @staticmethod
        def _run_cmd(cmd):
            return subprocess.run(cmd, shell=True, capture_output=True, text=True)

        @staticmethod  # 基于字符串的模糊搜索
        def fuzzy_search(string1, string2):  # str1 == %s%
            if string1.startswith('%') and string1.endswith('%'):  # %s% 表示模糊搜索
                regex_pattern = string1.replace('%', '.*')
            elif string1.startswith('%'):  # %s 表示前置模糊搜索
                regex_pattern = string1.replace('%', '.*') + '$'
            elif string1.endswith('%'):  # s% 表示后置模糊搜索
                regex_pattern = '^' + string1.replace('%', '.*')
            else:  # s 表示原文搜索
                regex_pattern = '^' + string1 + '$'
            return bool(re.search(regex_pattern, string2, re.IGNORECASE))  # 使用正则表达式进行搜索

        @staticmethod
        def delay(target):  # 小睡一会
            delay_time = float(target)
            time.sleep(delay_time)

        @staticmethod
        def click():
            pyautogui.click()  # 默认左键

        @staticmethod
        def click_screen_center():
            MyFun.Fun.click_position(x=pyautogui.size()[0] // 2, y=pyautogui.size()[1] // 2)

        @staticmethod
        def roll_to_bottom():
            for _ in range(10):
                pyautogui.scroll(-500)
                time.sleep(0.1)

        @staticmethod
        def close_windows(target):  # 关闭程序进程，用于卸载预处理
            temp = MyFun.Fun._run_cmd(f'''wmic process where "name='{target}'" delete''').stdout
            # wmic process get caption,CSName,ProcessID 查看正在运行的进程
            return '删除实例' in temp  # 删除成功就会return True

        @staticmethod
        def once_ocr():
            ImageGrab.grab().save(last_img, format='JPEG')
            return start_ocr(last_img)

        @staticmethod
        def audio_2_text_by_api(date_filepath):

            # 没有定义.temp检查
            def find_mp3(folder_path):
                # 遍历文件夹中的所有文件和子文件夹
                for root, dirs, files in os.walk(folder_path):
                    for temp_file in files:
                        # 检查文件扩展名是否为.mp3（不区分大小写）
                        if temp_file.lower().endswith('.mp3'):
                            # 返回完整的文件路径
                            my_logger.info(f"发现MP3文件: {os.path.join(root, temp_file)}")
                            return os.path.join(root, temp_file)
                # 如果没有找到MP3文件，返回None
                my_logger.error(f"找不到MP3文件: {folder_path}")
                raise FileNotFoundError('找不到MP3文件!')

            file_path = find_mp3(sj('TempFolder'))

            my_logger.info(f"开始识别音频文件: {file_path}")

            lfasr_host = 'https://raasr.xfyun.cn/v2/api'
            api_upload = '/upload'
            api_get_result = '/getResult'

            class RequestApi:
                def __init__(self, appid, secret_key, upload_file_path):
                    self.appid = appid
                    self.secret_key = secret_key
                    self.upload_file_path = upload_file_path
                    self.ts = str(int(time.time()))
                    self.signa = self.get_signa()

                def get_signa(self):
                    m2 = hashlib.md5()
                    m2.update((self.appid + self.ts).encode('utf-8'))
                    md5 = m2.hexdigest()
                    md5 = bytes(md5, encoding='utf-8')
                    signa = hmac.new(self.secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
                    return base64.b64encode(signa).decode('utf-8')

                def upload(self):
                    file_len = os.path.getsize(self.upload_file_path)
                    file_name = os.path.basename(self.upload_file_path)

                    param_dict = {
                        'appId': self.appid,
                        'signa': self.signa,
                        'ts': self.ts,
                        "fileSize": file_len,
                        "fileName": file_name,
                        "duration": "200"
                    }

                    # data = open(self.upload_file_path, 'rb', encoding='utf-8').read(file_len)
                    data = open(self.upload_file_path, 'rb').read(file_len)
                    response = requests.post(url=lfasr_host + api_upload + "?" + urllib.parse.urlencode(param_dict),
                                             headers={"Content-type": "application/json"}, data=data)
                    return json.loads(response.text)

                def get_result(self):
                    uploader = self.upload()
                    orderId = uploader['content']['orderId']
                    param_dict = {
                        'appId': self.appid,
                        'signa': self.signa,
                        'ts': self.ts,
                        'orderId': orderId,
                        'resultType': "transfer,predict"
                    }

                    status = 3
                    while status == 3:
                        response = requests.post(
                            url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                            headers={"Content-type": "application/json"})
                        result = json.loads(response.text)
                        status = result['content']['orderInfo']['status']
                        if status == 4:
                            break
                        time.sleep(5)
                    return result

            # Start processing
            start_time = time.time()

            # Call API to get results
            # EB5's API (quota resets on March 10)
            api = RequestApi(appid="9e15eefd", secret_key="228fc32fabca0fd9497d7fbca20732c4",
                             upload_file_path=file_path)
            # Alternative API api = RequestApi(appid="2481d92c", secret_key="daa40d136f63f1f74b9cd242eca8d271",
            # upload_file_path=file_path)

            temp_result = api.get_result()
            my_result = temp_result['content']['orderResult']
            data = json.loads(my_result)

            # Extract text
            text = ""
            for lattice in data['lattice']:
                st = json.loads(lattice['json_1best'])['st']
                for rt in st['rt']:
                    for ws in rt['ws']:
                        for cw in ws['cw']:
                            if cw['w']:
                                text += cw['w']

            # 填入到 2025_5_18.txt 中
            output_file_path = os.path.join(date_filepath)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(text)

            my_logger.info(f"文本已保存到: {output_file_path}")
            my_logger.info(f"任务完成，耗时：{int(time.time() - start_time)} 秒")

            # 删除下载的MP3文件，不然会重复生成
            os.remove(file_path)
            my_logger.info(f"已删除下载的MP3文件: {file_path}")

        @staticmethod
        def start_gpt_api(date_filepath):
            with open(date_filepath, 'r', encoding='utf-8') as f:
                data = f.read()

            class MinimalGPTChat:
                def __init__(self, api_key, base_url=None, persona="", model="gpt-4o-mini"):
                    self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
                    self.model = model
                    self.messages = [{"role": "system", "content": persona}]

                def chat(self, user_input):
                    self.messages.append({"role": "user", "content": user_input})

                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        temperature=0.7
                    )

                    ai_response = response.choices[0].message.content
                    self.messages.append({"role": "assistant", "content": ai_response})
                    return ai_response

            bot = MinimalGPTChat(
                api_key='YOUR_OPENAI_API_KEY',
                base_url='https://api.gpt.ge/v1',
            )

            text_list = [
                "你是一个互联网从业者，男性，姓陈，前鹅厂管理层，22年被裁，目前38"
                "岁，经营一家创业公司，技术出身，喜欢批判说明社会现状，并以骂醒人的语气讲述故事，你的面向对象是企图改变自己认知的青年、中年人。"
                "下面我会发一个别人的文字稿，请你将这个文字稿以自己的语气重新梳理一遍，换个角度说明，但主题观点应该一致，这个很重要，"
                "需要自行发挥一部分，如新增故事或修改数字、案例，不要缩减，而应该适当补充，字数要多于这个文字稿，注意不要过多暴露自己的信息，"
                "而应该是处理文字稿。不要有层次结构如首先、其次等，而应该连续说明，就像一个人在面对面给你讲。记得字数要多于原文。不要带地名，"
                "人名等敏感信息。目标用户不一定只有年轻人，注意用语。例子要修改为我的朋友的经历，不要写我的。尽量与原文语气一致，"
                "可以使用较为尖锐的文字，同时引起讨论，可以极端一点，但要能过审。如果出现时间内容则改为今天的时间。"
                "注意字数应维持在2000左右，不能太少，可以多一点"
                "千万千万千万千万不要出现日期如今天是6月1日等！"
                "自己的事情就不要说了，如参加会议，举办活动。只说观点看法和商业内容\n"
                + data
                ,
                '总结生成的文字稿的视频标题，直接输出一个即可，不需要带引号。'
                '20字以内，不要太多。'
                '要让大家能看懂，不要太专业，符合我的目标画像，'
                '精准涵盖内容点，同时要吸引人，20字以内。最好能带点对立，极端，让大家讨论。'
                ,
                '总结生成的文字稿的视频标签，生成五个，要求常见，热度高，贴合内容，流量总和最大，注意按流量排序，我要发布在B站、小红书、'
                '百家号、抖音等平台，写成一横排，按热度排序，用空格分开。'
                '注意我的内容多为社会和商业内容，请避免出现无关标签。'
            ]

            index = 0

            gpt_generate_text = ''
            gpt_generate_title = ''
            gpt_generate_tags = []

            while True:
                try:
                    if index >= len(text_list):
                        break
                    user_input = text_list[index]
                    index += 1
                    response = bot.chat(user_input)
                    if index == 1:
                        gpt_generate_text = response + ('我创建了一个知识星球，用于记录我所经历的商业从零到一的落地和赚钱过程，1980'
                                                        '元一人，可以帮助你在失业后维持收入，开启副业，私信我获取链接（需要审核）。\n'
                                                        '如果你在思考关于赚钱、副业、个人发展的问题，欢迎私信我进行付费咨询，298元一次！')
                    elif index == 2:
                        def check_punctuation(string):
                            # 使用正则表达式匹配句号、感叹号、问号
                            matches = re.findall(r'[.?!:，。：！？]', string)
                            # 如果匹配的标点符号超过两个，则返回True
                            return len(matches) > 2

                        if check_punctuation(response):
                            index = 1
                            continue
                        gpt_generate_title = response
                    elif index == 3:
                        gpt_generate_tags = response.split(' ')
                    if index == 3:
                        # 保存文件路径
                        output_filename = sj('json_path')

                        # new_tags = [f"#{tag}" for tag in gpt_generate_tags]

                        output_text = gpt_generate_text.replace('“', '').replace('”', '')
                        output_text = re.sub(r'\d{4}年', '之前', output_text)

                        gpt_generate_tags = [tag.strip() for tag in gpt_generate_tags if tag.strip() != '']

                        # 准备要保存的数据
                        data_to_save = {
                            # "text": gpt_generate_text.replace('“', '').replace('”', ''),  # 去掉引号
                            "text": output_text,
                            "title": gpt_generate_title[:20],  # 因为小红书限制标题长度为20
                            # "tags": gpt_generate_tags,  # ['商业', '创业', '副业', '个人发展']
                            "tags": [tag.strip() for tag in gpt_generate_tags if tag.strip() != ''],  # 去除空格
                            "introduction": f"{gpt_generate_title}"
                                            f"\n我创建了一个知识星球，用于记录我所经历的商业从零到一的落地和赚钱过程，1980元一人，"
                                            f"可以帮助你在失业后维持收入，开启副业，私信我获取链接。"
                                            f"\n如果你在思考关于赚钱、副业、个人发展的问题，欢迎私信我进行付费咨询，298元一次！"
                                            f"\n{' '.join([f'#{item}' for item in gpt_generate_tags])}",
                            "BaiJiaHao": f"{gpt_generate_title}"
                                         f"\n如果你在思考关于赚钱、副业、个人发展的问题，欢迎私信我进行付费咨询，298元一次！"
                                         f"\n{' '.join([f'#{item}' for item in gpt_generate_tags])}",
                            "NoTAGS": f"{gpt_generate_title}"
                                      "\n我创建了一个知识星球，用于记录我所经历的商业从零到一的落地和赚钱过程，1980元一人，"
                                      "可以帮助你在失业后维持收入，开启副业，私信我获取链接。"
                                      "\n如果你在思考关于赚钱、副业、个人发展的问题，欢迎私信我进行付费咨询，298元一次！",
                            # "#商业 #创业 #副业 #个人发展"
                            # f"\n{'  '.join([f'#{item}' for item in gpt_generate_tags])}"
                            # f"\n{new_tags}"
                        }

                        # 保存为JSON文件
                        with open(output_filename, 'w', encoding='utf-8') as f:
                            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

                        my_logger.info(f"GPT生成内容已保存: {output_filename}\n{data_to_save}")

                except Exception as e:
                    my_logger.error(f"GPT生成内容失败: {e}")
                    break

        # 准备要发布的文章内容
        # @staticmethod
        # def start_gpt_api_to_wechat_article(json_path):
        #     with open(json_path, 'r', encoding='utf-8') as f:
        #         text_content = json.load(f).get('text')
        # 
        #     def gpt_to_markdown(prompt, output_md_path):
        #         try:
        #             # 初始化 GPT API 客户端
        #             client = openai.OpenAI(
        #                 api_key='YOUR_OPENAI_API_KEY',
        #                 base_url='https://api.gpt.ge/v1'
        #             )
        # 
        #             # 构造对话消息
        #             messages = [
        #                 # {"role": "system", "content": (
        #                 #     "你是一个互联网从业者，男性，技术背景，前鹅厂管理层，现在创业。"
        #                 #     "你的语言风格尖锐、现实，常以批判方式指出社会问题，讲述现实故事，"
        #                 #     "面向试图改变认知的年轻人与中年人。请用你自己的语气讲述用户提供的主题，"
        #                 #     "内容要更丰富，可以虚构但要贴近现实。不要提及你自己，要像讲别人的故事，"
        #                 #     "不能使用“首先”“其次”等结构化语言，像聊天一样自然说出来。"
        #                 # )},
        #                 {"role": "user", "content": prompt}
        #             ]
        # 
        #             # 发起请求
        #             response = client.chat.completions.create(
        #                 model="gpt-4o-mini",
        #                 messages=messages,
        #                 temperature=0.7
        #             )
        # 
        #             # 获取回复内容
        #             content = response.choices[0].message.content.strip()
        # 
        #             if not os.path.exists(os.path.dirname(output_md_path)):
        #                 os.makedirs(os.path.dirname(output_md_path))
        # 
        #             # 保存为 Markdown
        #             with open(output_md_path, 'w', encoding='utf-8') as f:
        #                 f.write(content)
        # 
        #             my_logger.info(f"推文内容已保存至：{output_md_path}")
        # 
        #         except Exception as e:
        #             my_logger.error(f"GPT生成微信文章失败: {e}")
        # 
        #     # text = '将以下内容整理格式为微信推文，内容不变，仅增加小标题，黑体等格式\n' + text_content
        #     text = '将以下内容整理格式为微信推文，核心内容不变，仅修改文本风格和叙事方式，更符合微信用户阅读习惯。\n' + text_content
        #     path = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作\微信文章.md'
        # 
        #     gpt_to_markdown(text, path)

        @staticmethod
        def generate_cover(json_path):
            with open(json_path, 'r', encoding='utf-8') as file:
                text_content = json.load(file).get('title')

            font_path = sj('FontPath')

            # 创建白色背景图片 (1920×1080)
            width, height = 1920, 1080
            background_color = (255, 255, 255)  # 白色
            image = Image.new("RGB", (width, height), background_color)
            draw = ImageDraw.Draw(image)

            main_font = ImageFont.truetype(font_path, 100)  # 主文字大小
            sub_font = ImageFont.truetype(font_path, 40)  # 副文字大小

            text_list = re.split(r'[，。！：？,.:?!]', text_content)
            first_two_punctuation = re.findall(r'[，。！：？,.:?!]', text_content)[:2]

            # if first_two_punctuation[0] in ['！', '？']:
            #     text_list[0] = text_list[0] + first_two_punctuation[0]
            # if first_two_punctuation[1] in ['！', '？']:
            #     text_list[1] = text_list[1] + first_two_punctuation[1]

            if len(first_two_punctuation) > 0 and first_two_punctuation[0] in ['！', '？']:
                text_list[0] = text_list[0] + first_two_punctuation[0]
            if len(first_two_punctuation) > 1 and first_two_punctuation[1] in ['！', '？']:
                text_list[1] = text_list[1] + first_two_punctuation[1]

            if len(text_list) == 1:
                text_list.append('')

            # 主文本（居中）
            main_text = text_list[0]
            main_text_width = draw.textlength(main_text, font=main_font)
            main_text_x = (width - main_text_width) / 2
            main_text_y = height / 2 - 260  # 稍微偏上

            second_text = text_list[1]
            second_text_width = draw.textlength(second_text, font=main_font)
            second_text_x = (width - second_text_width) / 2
            second_text_y = height / 2 - 120  # 稍微偏上

            # 副文本（固定内容，较小字号）
            sub_text = "楚门世界指南"
            sub_text_width = draw.textlength(sub_text, font=sub_font)
            sub_text_x = (width - sub_text_width) / 2
            sub_text_y = height / 2 + 300  # 主文本下方

            # 绘制文本（黑色）
            text_color = (0, 0, 0)  # 黑色
            draw.text((main_text_x, main_text_y), main_text, fill=text_color, font=main_font)
            draw.text((second_text_x, second_text_y), second_text, fill=text_color, font=main_font)
            draw.text((sub_text_x, sub_text_y), sub_text, fill=text_color, font=sub_font)

            # 保存图片
            temp_folder = sj('TempFolder')
            output_file = os.path.join(temp_folder, '封面.png')
            image.save(output_file, "PNG")
            my_logger.info(f"封面已生成: {output_file}")

        @staticmethod
        def copy_content_from_json(json_path, temp_type):
            with open(json_path, 'r', encoding='utf-8') as file:
                text_content = json.load(file).get(temp_type)
                my_logger.info(f"正在复制 {temp_type} 内容...\n{text_content}")
            if temp_type == 'title':
                pyperclip.copy(text_content[:20])  # 标题只截取前20个字符
            else:
                pyperclip.copy(text_content)

        @staticmethod
        def input_labels_and_key_enter(json_path):
            with open(json_path, 'r', encoding='utf-8') as file:
                text_content = json.load(file).get("tags")
                my_logger.info(f"正在复制 tags 内容...\n{text_content}")
            for i in text_content:
                my_logger.info(f"正在输入标签: #{i}")
                pyperclip.copy('#' + i)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                keyboard.press('enter')
                time.sleep(1)
                # pyautogui.write(' ')
                # time.sleep(1)

        @staticmethod
        def past_text():
            # 粘贴到输入框
            # 这个可能会出问题
            keyboard.press_and_release('ctrl+v')
            my_logger.info(f"文本已粘贴到输入框")

        @staticmethod
        def click_position(x, y):
            MyFun.Input._smooth_move_win32(x, y)
            MyFun.Input.click(x, y)

        @staticmethod
        def move_to_make(file_path):
            # 在 file_path 中找到最新的视频并移动到 E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作
            video_extensions = ['*.mp4']
            video_files = []

            for ext in video_extensions:
                video_files.extend(glob.glob(os.path.join(file_path, ext)))

            if not video_files:
                my_logger.error("No video files found in the directory.")
                return

            newest_video = max(video_files, key=os.path.getmtime)
            new_filename = "音频带字幕.mp4"
            new_filepath = os.path.join(os.path.dirname(newest_video), new_filename)
            dest_dir = sj('TempFolder')
            dest_path = os.path.join(dest_dir, new_filename)

            os.makedirs(dest_dir, exist_ok=True)

            try:
                # 先重命名
                os.rename(newest_video, new_filepath)
                my_logger.info(f"Renamed {newest_video} to {new_filename}")

                # 如果目标文件已存在，先删除
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                    my_logger.info(f"Removed existing file at {dest_path}")

                # 移动文件（覆盖模式）
                shutil.move(new_filepath, dest_path)
                my_logger.info(f"Moved {new_filename} to {dest_dir}")
            except Exception as e:
                my_logger.error(f"Error processing file: {e}")

        # 能不能读取raw_video_path的总长度，并计算所用百分比（end_time/raw_video_path总长度），并写入文件第二行\
        # 带百分比的CUT_VIDEO
        @staticmethod
        def cut_video():

            # ---------- 工具函数 ----------
            def read_first_line(file_path: str) -> str:
                """
                仅读取文件的第一行（去掉换行符），避免后续 float() 解析受第二行影响
                """
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.readline().strip()
                except FileNotFoundError:
                    raise FileNotFoundError(f'未找到 {file_path}')
                except Exception as e:
                    raise RuntimeError(f'读取 {file_path} 出错: {e}')

            def write_two_lines(file_path: str, first: str, second: str) -> None:
                """
                覆盖写入两行内容：第一行 end_time，第二行占比百分比
                """
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f'{first}\n{second}')

            # ---------- 路径 ----------
            start_time_file = sj('StartEndTime')
            output_file = sj('VideoNoAudio')
            raw_video_path = sj('VideoAsset')
            time_from_video_path = sj('AudioWithSubtitles')

            # ---------- 读取起始时间 ----------
            start_time = float(read_first_line(start_time_file))

            # ---------- 结束时间 ----------
            end_time = start_time + VideoFileClip(time_from_video_path).duration

            # ---------- 计算原片时长与百分比 ----------
            with VideoFileClip(raw_video_path) as raw_clip:
                total_duration = raw_clip.duration

            if total_duration == 0:
                raise ValueError('原始视频时长为 0，无法计算百分比')

            used_percent = f'{round(end_time / total_duration * 100, 2)}%'

            # TODO 查看日志
            my_logger.info(f"视频总时长: {total_duration:.2f}s, 已用时长: {end_time:.2f}s, 已用百分比: {used_percent}")

            # ---------- 写回 txt（两行） ----------
            write_two_lines(start_time_file, str(end_time), used_percent)

            # ---------- 裁剪命令 ----------
            command = [
                'ffmpeg',  # 确保 ffmpeg 已在 PATH
                '-hide_banner',
                '-loglevel', 'error',
                '-ss', str(start_time),
                '-to', str(end_time),
                '-i', raw_video_path,
                '-c', 'copy',
                output_file,
                '-y'
            ]

            try:
                subprocess.run(command, check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return output_file
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f'ffmpeg 裁剪失败: {e}')

        @staticmethod
        def create_final_video():
            cover_image_path = sj('CoverPath')
            silent_video_path = sj('VideoNoAudio')
            audio_video_path = sj('AudioWithSubtitles')
            final_output = sj('VideoPath')
            print("final_output", final_output)

            temp_overlay = "temp_overlay.mp4"
            temp_cover = "temp_cover.mp4"
            concat_list = "temp_concat_list.txt"

            try:
                # 步骤1：黑色背景去除 + 叠加
                subprocess.run([
                    "ffmpeg", "-y",
                    "-hide_banner",
                    "-loglevel", "error",  # 只显示错误信息
                    "-i", audio_video_path,
                    "-i", silent_video_path,
                    "-filter_complex",
                    "[0:v]scale=iw*1.1:ih*1.1,colorkey=black:0.3:0.2[fg];"
                    "[1:v][fg]overlay=x=(W-w)/2:y=(H-h)/2:format=auto",
                    "-c:v", "libx264",
                    "-crf", "18",
                    "-preset", "veryfast",
                    "-pix_fmt", "yuv420p",
                    "-map", "0:a?",  # 保留原音频（如果有）
                    temp_overlay
                ], check=True)

                # 步骤2：创建封面视频（3秒静音）
                subprocess.run([
                    "ffmpeg", "-y",
                    "-hide_banner",
                    "-loglevel", "error",  # 只显示错误信息
                    "-loop", "1",
                    "-i", cover_image_path,
                    "-f", "lavfi", "-t", "3",
                    "-i", "anullsrc=r=44100:cl=stereo",
                    "-shortest",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-pix_fmt", "yuv420p",
                    temp_cover
                ], check=True)

                # 步骤3：写入拼接列表
                with open(concat_list, "w", encoding="utf-8") as f:
                    f.write(f"file '{os.path.abspath(temp_cover)}'\n")
                    f.write(f"file '{os.path.abspath(temp_overlay)}'\n")

                # 步骤4：拼接封面视频和合成视频（同时拼接音频）
                subprocess.run([
                    "ffmpeg", "-y",
                    "-hide_banner",
                    "-loglevel", "error",  # 只显示错误信息
                    "-i", temp_cover,
                    "-i", temp_overlay,
                    "-filter_complex",
                    "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]",
                    "-map", "[outv]",
                    "-map", "[outa]",
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-pix_fmt", "yuv420p",
                    final_output
                ], check=True)

                my_logger.info(f"视频合成成功，路径: {final_output}")
                # 复制链接到剪贴板
                pyperclip.copy(final_output)

            finally:
                # 清理临时文件
                for file in [temp_overlay, temp_cover, concat_list]:
                    if os.path.exists(file):
                        os.remove(file)
                my_logger.info("临时文件已清理。")

        # @staticmethod
        # def click_xhs_label(target):
        #     with open(target, 'r', encoding='utf-8') as file:
        #         tag_list = json.load(file).get('tags')
        #
        #     def run_click(item_text):
        #         MyFun.Input.click_text("#" + item_text)
        #         time.sleep(1)
        #         MyFun.Input.press('LEFT')
        #         time.sleep(0.5)
        #         MyFun.Input.press('LEFT')
        #         time.sleep(0.5)
        #         MyFun.Input.press('LEFT')
        #         time.sleep(0.5)
        #
        #     for item in reversed(tag_list):
        #         run_click(item)
        #     # ['创业', '心态成长', '职场发展', '自我提升', '社会观察']

        @staticmethod
        def input_bzhan_tags(target):
            # 删不掉标签，算了
            # for _ in range(10):
            #     keyboard.send('delete')  # 模拟真实按键，很多浏览器能识别
            # pyautogui.press('delete')
            # time.sleep(0.5)
            with open(target, 'r', encoding='utf-8') as file:
                tag_list = json.load(file).get('tags')
            new_items = ["赚钱", "认知", "商业"]
            tag_list = new_items + tag_list
            for item in tag_list:
                pyperclip.copy(item)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.5)

        # TODO 检验，create_date_file日期加一，然后注释掉get_today_VideoLink再运行一次
        @staticmethod
        def init_files():

            def delete_mp3():
                folder_path = sj('TempFolder')
                for name in os.listdir(folder_path):
                    if name.lower().endswith('.mp3'):
                        file_path = os.path.join(folder_path, name)
                        try:
                            os.remove(file_path)
                            my_logger.info(f"已删除: {file_path}")
                        except Exception as exc:
                            my_logger.error(f"删除失败 {file_path} → {exc}")

            def create_date_file():
                # 基础路径
                base_path = sj('RawTextFolder')
                # 获取当前日期
                # today = datetime.now() + timedelta(days=1)  # 因为之前重复了一天，所以加一天
                today = datetime.now() + timedelta()
                year = today.year
                month = today.month
                day = today.day
                # 格式化月份为两位数（如05）
                month_str = f"{month:02d}"
                # 创建月份文件夹路径
                month_folder = os.path.join(base_path, month_str)
                # 如果月份文件夹不存在，则创建
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)
                    print(f"已创建月份文件夹: {month_folder}")
                # 尝试查找顺延文件名（如2025_05_26.txt、2025_05_26_2.txt、2025_05_26_3.txt...）
                base_filename = f"{year}_{month}_{day}"
                suffix = ""
                count = 1
                while True:
                    date_filename = f"{base_filename}{suffix}.txt"
                    date_candidate = os.path.join(month_folder, date_filename)
                    if not os.path.exists(date_candidate):
                        temp_value = date_candidate
                        with open(temp_value, 'w', encoding='utf-8') as f:
                            pass  # 创建空文件
                        my_logger.info(f"已创建日期文件: {temp_value}")
                        break
                    count += 1
                    suffix = f"_{count}"
                sj('SET', 'DateFilepath', temp_value)

            # 获取当天视频链接，并将未完成视频.txt的第一个链接写入已完成视频.txt的最后一行
            # 获取第二天视频链接，并将未完成视频.txt的第一个链接写入已完成视频.txt的最后一行
            # def get_today_VideoLink():
            #     finished_video_path = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\已完成视频.txt'
            #     unfinished_video_path = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\未完成视频.txt'
            #     # 读取未完成视频.txt的第一条信息
            #     with open(unfinished_video_path, 'r', encoding='utf-8') as file:
            #         first_line = file.readline()
            #     text = first_line.strip().split(' ')  # ['2023-6-25', 'BV1aV411u7mA', '拒绝电池思维——认清现实，理性看待上学和找工作']
            #     # 复制文本到已完成视频.txt
            #     with open(finished_video_path, 'a', encoding='utf-8') as file:
            #         file.write(
            #             f"{datetime.now().strftime("%Y-%m-%d")} | {text[0]} {text[1]} {text[2]}\n")  # 写入已完成视频.txt的最后一行
            #     # 删除未完成视频.txt的第一条信息
            #     with open(unfinished_video_path, 'r', encoding="utf-8") as file:
            #         lines = file.readlines()  # 注意readline()和readlines()的区别
            #     with open(unfinished_video_path, 'w', encoding="utf-8") as file:
            #         file.writelines(lines[1:])  # 从第二行开始写入
            #     sj('SET', 'VideoLink', f"https://www.bilibili.com/video/{text[1]}/")

            # 好像用不到，因为结束会自动删除
            delete_mp3()
            create_date_file()
            # get_today_VideoLink()

        # @staticmethod
        # def init_files():
        #     def create_date_file():
        #         # 基础路径
        #         base_path = r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\原文文字稿"
        #         # 获取当前日期
        #         today = datetime.now()
        #         year = today.year
        #         month = today.month
        #         day = today.day
        #         # 格式化月份为两位数（如05）
        #         month_str = f"{month:02d}"
        #         # 创建月份文件夹路径
        #         month_folder = os.path.join(base_path, month_str)
        #         # 如果月份文件夹不存在，则创建
        #         if not os.path.exists(month_folder):
        #             os.makedirs(month_folder)
        #             print(f"已创建月份文件夹: {month_folder}")
        #         # 尝试查找顺延文件名（如2025_05_26.txt、2025_05_26_2.txt、2025_05_26_3.txt...）
        #         base_filename = f"{year}_{month}_{day}"
        #         suffix = ""
        #         count = 1
        #         while True:
        #             date_filename = f"{base_filename}{suffix}.txt"
        #             date_candidate = os.path.join(month_folder, date_filename)
        #             if not os.path.exists(date_candidate):
        #                 temp_value = date_candidate
        #                 with open(temp_value, 'w', encoding='utf-8') as f:
        #                     pass  # 创建空文件
        #                 my_logger.info(f"已创建日期文件: {temp_value}")
        #                 break
        #             count += 1
        #             suffix = f"_{count}"
        #         start_json('SET', 'DateFilepath', temp_value)
        #
        #     # 获取当天视频链接，并将未完成视频.txt的第一个链接写入已完成视频.txt的最后一行
        #     def get_today_VideoLink():
        #         finished_video_path = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\已完成视频.txt'
        #         unfinished_video_path = r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\Static\未完成视频.txt'
        #         # 读取未完成视频.txt的第一条信息
        #         with open(unfinished_video_path, 'r', encoding='utf-8') as file:
        #             first_line = file.readline()
        #         text = first_line.strip().split(' ')  # ['2023-6-25', 'BV1aV411u7mA', '拒绝电池思维——认清现实，理性看待上学和找工作']
        #         # 复制文本到已完成视频.txt
        #         with open(finished_video_path, 'a', encoding='utf-8') as file:
        #             file.write(f"{datetime.now().strftime("%Y-%m-%d")} | {text[0]} {text[1]} {text[2]}\n")  # 写入已完成视频.txt的最后一行
        #         # 删除未完成视频.txt的第一条信息
        #         with open(unfinished_video_path, 'r', encoding="utf-8") as file:
        #             lines = file.readlines()  # 注意readline()和readlines()的区别
        #         with open(unfinished_video_path, 'w', encoding="utf-8") as file:
        #             file.writelines(lines[1:])  # 从第二行开始写入
        #         start_json('SET', 'VideoLink', f"https://www.bilibili.com/video/{text[1]}/")
        #
        #     create_date_file()
        #     get_today_VideoLink()

        @staticmethod
        def git_repo():
            repo_path = r'E:\WindowsAi'
            commit_msg = '''
                    自动化更新
                    已完成 6.29
                    还有一些小问题，改完后用小电脑测试一下。
            '''
            if not os.path.isdir(os.path.join(repo_path, ".git")):
                my_logger.error("指定路径不是 Git 仓库")
                raise ValueError("指定路径不是 Git 仓库")

            def run(cmd):
                # 用 shlex.split 兼容带空格的路径
                subprocess.run(shlex.split(cmd),
                               cwd=repo_path,
                               stdout=subprocess.PIPE,  # 捕获并静默标准输出
                               stderr=subprocess.PIPE,  # 捕获并静默警告
                               check=True)

            # 1. 仅添加已跟踪文件的改动
            run("git add -u")

            # 2. 若还有新文件需要纳入版本控制，可手动指定：
            # run('git add path/to/new_file')

            # 3. 提交（--allow-empty-message 防止空提交报错）
            try:
                run(f'git commit -m "{commit_msg}"')
            except subprocess.CalledProcessError as e:
                # 若没有任何变更会触发非零返回码；可选择忽略
                if "nothing to commit" in e.stderr:
                    my_logger.warning("没有检测到需要提交的改动")
                    return
                raise

            # 4. 推送
            run("git push")
            my_logger.info("自动化Git提交完成")

        @staticmethod
        def copy_video_to_folder():
            # 路径配置
            source_json = sj('json_path')
            # source_video = sj('SET', 'VideoPath') # 这里的SET导致参数为空，为什么我会这么写？
            source_video = sj('VideoPath')
            target_root = sj('ReadyToUpload')

            # 确保目标根目录存在
            os.makedirs(target_root, exist_ok=True)

            # 读取 JSON 获取标题，标题应该新增一个赏味不足的标题
            try:
                with open(source_json, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    title = json_data.get("title", "未命名标题").strip()
                    my_logger.info(f"读取 JSON 成功，标题为：{title}")
            except Exception as e:
                my_logger.error(f"读取 JSON 失败：{e}")
                return

            # 获取已存在文件夹数量确定编号
            # existing_folders = [
            #     name for name in os.listdir(target_root)
            #     if os.path.isdir(os.path.join(target_root, name)) and name[:2].isdigit()
            # ]
            # next_index = len(existing_folders) + 1
            # index_str = f"{next_index:02d}"

            # 改为最大的，这样没问题
            existing_indexes = [
                int(name[:2]) for name in os.listdir(target_root)
                if os.path.isdir(os.path.join(target_root, name)) and name[:2].isdigit()
            ]

            next_index = max(existing_indexes, default=0) + 1
            index_str = f"{next_index:02d}"

            # 读取目前完成的文件名
            finished_video_path = sj('FinishedVideo')  # 这里应该是完成的倒一，然后会新增一条
            # 应该读取最后一行而非第一行
            with open(finished_video_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                last_line = lines[-1].strip() if lines else ''

            # text = last_line.strip().split(' ')  # ['2023-6-25', 'BV1aV411u7mA', '拒绝电池思维——认清现实，理性看待上学和找工作']
            text = last_line.strip().replace('/', '，').split(' ')  # 斜杠变成文件夹也离谱
            # 创建目标文件夹——尝试使用赏味不足的标题
            # folder_name = f"{index_str}-{title}"
            folder_name = f"{index_str}-{text[4]}"  # 这里是2不是3.......又得重来了
            folder_path = os.path.join(target_root, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # 复制文件
            try:
                my_logger.info(f"复制文件：源文件：{source_json} → {folder_path}")
                shutil.copy2(source_json, os.path.join(folder_path, "GPT生成内容.json"))
                shutil.copy2(source_video, os.path.join(folder_path, "导出视频.mp4"))
                my_logger.info(f"文件复制成功，目标路径：{folder_path}")
            except Exception as e:
                my_logger.error(f"文件复制失败：{e}")
