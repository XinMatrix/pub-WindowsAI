import ctypes
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser
import winreg
import zipfile
from pathlib import Path

import psutil
import pyautogui
import pyperclip
import requests
import win32api
import win32com.client
import win32con
import win32gui
from PIL import Image, ImageDraw, ImageFont, ImageGrab

from config import http_host, last_img, ocr_url, temp_check


def get_system_id():  # 这个东西是唯一的，因为我和虚拟机都弄了所以有两个。。
    result = subprocess.check_output("wmic csproduct get uuid", shell=True)  # 7372C4C3-B6D5-5A45-9AF0-6F642FAAC557
    result = result.decode().split('\n')[1].strip()
    return result


# OCR信息可空
def start_action(results, action_string, log, user_message, temp_ocr_text=None, temp_ocr_position=None,
                 temp_ocr_accuracy_outputs=None):
    action_list = action_string.split('->')  # 还是用箭头吧，因为有些函数名字比较长，KeyWord也是
    for action in action_list:
        time.sleep(0.25)  # 感觉0.25有点快了——还是在db里添加把，不然会越来越大
        # time.sleep(0.5)  # 我不喜欢它笨笨的感觉，太慢了
        # 这个函数库将来会非常大，非常
        # 按键
        if re.search(r"\bKEY\((.*?)\)", action):  # Nice 使用正则匹配减小工作量——加\b是为了完全有且仅有匹配模式
            target = re.search(r"\bKEY\((.*?)\)", action).group(1)
            log.info(f'Match Process KEY : {action}')
            MyFun.Input.press(target)

        # 输入内容
        elif re.search(r"\bINPUT\((.*?)\)", action):
            target = re.search(r"\bINPUT\((.*?)\)", action).group(1)
            log.info(f'Match Process INPUT : {action}')
            MyFun.Input.input_content(target)

        # 组合键
        elif re.search(r"\bHOTKEY\((.*?)\)", action):
            target = re.search(r"\bHOTKEY\((.*?)\)", action).group(1)
            log.info(f'Match Process HOTKEY : {action}')
            keys = target.split('+')
            lowercase_keys = [key.lower() for key in keys]  # 转换为小写防止按住Shift模拟大小——这个是必要的
            MyFun.Input.hot_key(lowercase_keys)

        # OCR点击文本
        elif re.search(r"\bCLICK_TEXT\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT\((.*?)\)", action).group(1)
            log.info(f'Match Process CLICK_TEXT : {action}')
            MyFun.Input.click_text(target, temp_ocr_text, temp_ocr_position)

        # FIXME 测试中 按区域点击
        elif re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action):
            # target = re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action).group(1)  # TODO 识别出两个参数
            target = re.search(r"\bCLICK_TEXT_AREA\((.*?),(.*?)\)", action)
            t1 = target.group(1)  # 区域程序名称
            t2 = target.group(2)  # 点击文字
            log.info(f'Match Process CLICK_TEXT_AREA : {action}')
            MyFun.Input.click_text_area(t1, t2, temp_ocr_text, temp_ocr_position)

        # 点击精确文字
        elif re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action).group(1)
            log.info(f'Match Process CLICK_TEXT_ACCURACY : {action}')
            MyFun.Input.click_text_accuracy(target, temp_ocr_accuracy_outputs)

        # 使用默认浏览器打开网址
        elif re.search(r"\bWEB_BROWSER\((.*?)\)", action):
            target = re.search(r"\bWEB_BROWSER\((.*?)\)", action).group(1)
            log.info(f'Match Process WEB_BROWSER : {action}')
            MyFun.System.open_web(target)

        # 精准搜索打开 MyWindowsAi/Downloads/ 下文件
        elif re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action):
            target = re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action).group(1)
            log.info(f'Match Process OPEN_DOWNLOADED : {action}')
            MyFun.System.open_downloaded(target)

        # 打开已安装程序，系统或 MyWindowsAi/Program/ 下程序
        elif re.search(r"\bOPEN_INSTALLED\((.*?)\)", action):  # 模糊匹配已安装程序
            target = re.search(r"\bOPEN_INSTALLED\((.*?)\)", action).group(1)
            log.info(f'Match Process OPEN_INSTALLED : {action}')
            MyFun.System.open_installed(target)

        # 打开系统程序，如用户帐户控制、程序和功能
        elif re.search(r"\bOPEN_SYSTEM\((.*?)\)", action):  # 打开系统程序
            target = re.search(r"\bOPEN_SYSTEM\((.*?)\)", action).group(1)
            log.info(f'Match Process OPEN_SYSTEM : {action}')
            MyFun.System.open_system(target, log)

        # FIXME 检查程序是否存在
        elif re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action):
            target = re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action).group(1)
            log.info(f'Match Process CHECK_EXE_EXIST : {action}')
            MyFun.System.check_exe_exists(target)

        # 设置程序焦点
        elif re.search(r"\bSET_FOCUS\((.*?)\)", action):  # 普通切换
            target = re.search(r"\bSET_FOCUS\((.*?)\)", action).group(1)
            log.info(f'Match Process SET_FOCUS : {action}')
            check = True
            while check:
                time.sleep(1)
                check = MyFun.System.switch_to_windows(target, log)  # 循环检测

        # 设置全屏焦点
        elif re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action):  # 全屏切换——有点问题，Chrome安装和普通程序都会被打开隐藏
            target = re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action).group(1)
            log.info(f'Match Process SET_FOCUS_FULL : {action}')
            check = True
            while check:
                time.sleep(1)
                check = MyFun.System.switch_to_windows_full(target)  # 循环检测

        # 执行函数，如获取WIFI密码，也可以是好玩
        elif re.search(r"\bFUN\((.*?)\)", action):
            target = re.search(r"\bFUN\((.*?)\)", action).group(1)
            log.info(f'Match Process FUN : {action}')
            MyFun.Fun.start_inner_fun(target, log)

        # 循环检测文件夹下文件以判断是否下载完成
        elif re.search(r"\bWAIT_DOWNLOAD\((.*?)\)", action):
            target = re.search(r"\bWAIT_DOWNLOAD\((.*?)\)", action).group(1)
            log.info(f'Match Process WAIT_DOWNLOAD : {action}')
            check = True
            while check:
                check = MyFun.Fun.wait_download(target)  # ChromeSetup.exe
                time.sleep(1)

        # 小睡一会
        elif re.search(r"\bSLEEP\((.*?)\)", action):
            target = re.search(r"\bSLEEP\((.*?)\)", action).group(1)
            log.info(f'Match Process SLEEP : {action}')
            MyFun.Fun.delay(target)

        # 关闭运行窗口/清理后台程序
        elif re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action):
            target = re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action).group(1)
            log.info(f'Match Process CLOSE_WINDOWS : {action}')
            MyFun.Fun.close_windows(target)

        # 下载文件，默认保存在MyWindowsAi/Download目录下
        elif re.search(r"\bDOWNLOAD\((.*?)\)", action):
            target = re.search(r"\bDOWNLOAD\((.*?)\)", action).group(1)
            log.info(f'Match Process DOWNLOAD : {action}')
            temp = MyFun.Fun.download(target)
            if temp.endswith('.zip'):
                with zipfile.ZipFile(temp, 'r') as zip_ref:
                    files = zip_ref.namelist()  # 获取压缩包内的文件列表
                    for file in files:  # 原地解压文件
                        zip_ref.extract(file, os.path.dirname(temp))
                os.remove(temp)  # 解压完成后删除压缩包
                log.info(f'Deleted source file: {temp}')

        # 输入安装目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action):  # 下载程序文件，默认保存在MyWindowsAi/Download目录下
            target = re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action).group(1)
            log.info(f'Match Process INPUT_DOWNLOAD : {action}')
            MyFun.Input.input_download(target)

        # 输入项目目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_PROJECT\((.*?)\)", action):
            target = re.search(r"\bINPUT_PROJECT\((.*?)\)", action).group(1)
            log.info(f'Match Process INPUT_PROJECT : {action}')
            MyFun.Input.input_project(target)

        elif re.search(r"\bGOTO\((.*?)\)", action):
            target = re.search(r"\bGOTO\((.*?)\)", action).group(1)
            log.info(f'Match Process GOTO : {action}')
            # 先查找，再执行 Nice
            for y in results:  # 这个是必中的
                if y[2] == target:
                    start_action(results, y[3], log, user_message)
                    break

        # 循环OCR，并等待检测target
        elif re.search(r"\bWAIT_OCR\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR\((.*?)\)", action).group(1)
            log.info(f'Match Process WAIT_OCR : {action}')
            while True:
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break

        elif re.search(r"\bWAIT_OCR_END\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR_END\((.*?)\)", action).group(1)
            log.info(f'Match Process WAIT_OCR_END : {action}')
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
            log.info(f'Match Process SELECT_OCR')
            target_list = []
            action_list = []
            for y in results:  # 这个是必中的
                if re.search(r"\bOCR\((.*?)\)", y[2]):
                    target = re.search(r"\bOCR\((.*?)\)", y[2]).group(1)
                    target_list.append(target)
                    action_list.append(y[3])
            while True:
                time.sleep(1)
                ocr_outputs = MyFun.Fun.once_ocr()
                for x in ocr_outputs:
                    for index, y in enumerate(target_list):
                        if MyFun.Fun.fuzzy_search(y, x['text']):
                            start_action(results, action_list[index], log, user_message)

        # 移动文件夹到项目中
        elif re.search(r"\bMOVE_TO_PROJECT\((.*?)\)", action):
            target = re.search(r"\bMOVE_TO_PROJECT\((.*?)\)", action).group(1)
            log.info(f'Match Process MOVE_TO_PROJECT : {action}')
            from_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Downloads\\{target}')
            MyFun.Fun.move_files(from_path, 'Projects')

        # 下载Python包，使用默认pip
        # elif re.search(r"\bINSTALL_PYTHON_PACKAGE\((.*?)\)", action):
        #     target = re.search(r"\bINSTALL_PYTHON_PACKAGE\((.*?)\)", action).group(1)
        #     log.info(f'Match Process INSTALL_PYTHON_PACKAGE : {action}')
        #     MyFun.Fun.install_python_package(target, log)

        # FIXME 右键
        elif action == 'CLICK_RIGHT()':  # 无参函数
            log.info(f'Match Process CLICK_RIGHT')
            MyFun.Input.click_right()

        elif action == 'FINISH()':  # 无参函数
            log.info(f'Match Process FINISH')
            MyFun.System.finish(log)
            # 我想让它执行完成后返回聊天内容
            global temp_check
            temp_check['Value'] = True

        else:
            log.critical(f'ACTION NOT FOUND: {action}')
            raise ModuleNotFoundError(f'ACTION NOT FOUND: {action}')
            # return  # return会无法显示错误信息，所以还是用raise吧


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
                print(f"Error accessing HKEY_LOCAL_MACHINE: {e}")
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
                print(f"Error accessing HKEY_CURRENT_USER: {e}")
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
        def switch_to_windows(name_like, logging):
            windows = MyFun.System._get_running_windows()
            for hwnd, title in windows:
                if name_like in title:  # 模糊搜索，其实也可以精准搜索，只要字足够多
                    logging.info(f'Switch to {title}')
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
        def open_system(target_exe, logging):
            if target_exe == 'UserAccountControlSettings':
                subprocess.Popen(r'C:\Windows\System32\UserAccountControlSettings.exe')  # 可以先写个检测程序检测这些路径是否存在
                time.sleep(0.2)  # 时间不确定，等待实战测试
                MyFun.System.switch_to_windows('用户帐户控制设置', logging)  # 切换焦点，稳妥起见
            # 默认在下载位置，所以遍历下载文件查找
            elif target_exe == 'ProgramAndFunction':
                subprocess.call('appwiz.cpl', shell=True)  # 这个是打开卸载，比系统自带的好用
                time.sleep(0.2)
                MyFun.System.switch_to_windows('程序和功能', logging)  # 已验证

        @staticmethod
        def check_exe_exists(target):  # 检查文件是否存在
            exist_exe_list = MyFun.System._get_installed_programs()
            if target in exist_exe_list:
                print(f'{target} Exists!')

        @staticmethod
        def finish(logging):
            logging.info('Program Finished!')
            MyFun.System.kill_processes('Photos.exe')  # 推荐使用精准关闭

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
            img_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Configs\\BG_WindowsAi.png')  # 路径错误，所以打开不对
            time.sleep(1)
            subprocess.Popen(['explorer', img_path])  # 使用explorer打开图片
            time.sleep(2)  # 给几秒让他加载会——因为不确定打开时间——要不要写个程序专门监听——不行，尝试失败
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

        @staticmethod
        def click(x, y):  # 点击位置
            pyautogui.click(x, y)

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
        def click_text(target_text, text_list, pos_list):  # 平滑点击文字
            for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
                if value.lower() == target_text.lower():  # 注意小写——仅在对比时使用小写
                    MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
                    MyFun.Input.click(pos_list[index][0], pos_list[index][1])
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
        def _run_cmd(cmd):
            return subprocess.run(cmd, shell=True, capture_output=True, text=True)

        @staticmethod
        def start_inner_fun(target_fun, log):
            if target_fun == 'GET_WIFI_PASSWORD':
                names, passwords = MyFun.Fun._get_wifi_status()
                tmp_list = []
                for name, password in zip(names, passwords):
                    tmp_list.append(f'{name} : {password}')
                log.info(tmp_list)
                # write_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Outputs')
                write_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Statics')
                with open(f'{write_path}/wifi_result.txt', 'w', encoding='utf-8') as f:
                    for item in tmp_list:
                        f.write(item + '\n\n')
                    f.close()  # 关闭文件
                os.startfile(f'{write_path}/wifi_result.txt')
                time.sleep(1.5)
                MyFun.System.switch_to_windows_full('wifi_result.txt')  # 切换焦点
            # 会导致程序无法正常运行，所以注释掉
            # elif target_fun == 'UPGRADE_PIP':  # 升级pip
            #     try:
            #         result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
            #         current_version = result.stdout.split()[1]
            #         log.info(f"当前pip版本：{current_version}")
            #         subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            #         log.info("pip升级成功！")
            #     except subprocess.CalledProcessError as e:
            #         log.error(f"pip升级失败：{e}")
            else:
                log.error(f'未知函数 {target_fun}')
                raise ValueError(f'未知函数 {target_fun}')

        @staticmethod
        def _get_wifi_status():  # 获取所有连接过的WIFI的密码
            output = MyFun.System.run_cmd('netsh wlan show profiles')
            wifi_name_list = []
            wifi_password_list = []
            lines = output.strip().split('\n')
            user_profiles = [line.strip().split(' : ')[-1] for line in lines if '所有用户配置文件' in line]
            for profile in user_profiles:
                wifi_name_list.append(profile)
            for item in wifi_name_list:
                output = MyFun.System.run_cmd(f'netsh wlan show profile name="{item}" key=clear')
                if output is not None:  # 安全防护
                    match = re.search(r"关键内容\s*:\s*(\S+)", output)
                    if match:
                        password = match.group(1)
                        wifi_password_list.append(password)
                    else:
                        wifi_password_list.append('检索失败')
                else:
                    wifi_password_list.append('检索失败')
            return wifi_name_list, wifi_password_list

        # @staticmethod  # 模糊搜索文本
        # def fuzzy_search(string, data_list):  # %s%
        #     if string.startswith('%') and string.endswith('%'):  # %s% 表示模糊搜索
        #         regex_pattern = string.replace('%', '.*')
        #     elif string.startswith('%'):  # %s 表示前置模糊搜索
        #         regex_pattern = string.replace('%', '.*') + '$'
        #     elif string.endswith('%'):  # s% 表示后置模糊搜索
        #         regex_pattern = '^' + string.replace('%', '.*')
        #     else:  # s 表示原文搜索
        #         regex_pattern = '^' + string + '$'
        #     for item in data_list:
        #         if re.search(regex_pattern, item, re.IGNORECASE):  # 使用正则表达式进行搜索
        #             return True
        #     return False  # False表示没有搜索到

        @staticmethod  # 基于字符串的模糊搜索
        def fuzzy_search(string1, string2):
            if string1.startswith('%') and string1.endswith('%'):  # %s% 表示模糊搜索
                regex_pattern = string1.replace('%', '.*')
            elif string1.startswith('%'):  # %s 表示前置模糊搜索
                regex_pattern = string1.replace('%', '.*') + '$'
            elif string1.endswith('%'):  # s% 表示后置模糊搜索
                regex_pattern = '^' + string1.replace('%', '.*')
            else:  # s 表示原文搜索
                regex_pattern = '^' + string1 + '$'
            return bool(re.search(regex_pattern, string2, re.IGNORECASE))  # 使用正则表达式进行搜索

        # @staticmethod
        # def wait_windows(name):
        #     windows = MyFun.System._get_running_windows()
        #     for hwnd, title in windows:
        #         if name == title:
        #             # TODO Set Focus
        #             MyFun.System.switch_to_windows(name)  # 切换焦点
        #             return False  # 找到就返回False
        #     return True

        @staticmethod
        def wait_download(name):  # 持续检测下载内容
            downloads_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Downloads')
            # downloads_path = os.path.expandvars('%USERPROFILE%\\Downloads')
            if os.path.exists(downloads_path):  # 检查下载文件夹是否存在
                for item in os.listdir(downloads_path):  # 遍历下载文件夹中的所有项
                    # if item == name:
                    if name in item:  # 这里使用包含，因为文件名可能包含版本号
                        return False  # 找到就返回False
            return True

        @staticmethod
        def delay(target):  # 小睡一会
            delay_time = float(target)
            time.sleep(delay_time)

        @staticmethod
        def close_windows(target):  # 关闭程序进程，用于卸载预处理
            temp = MyFun.Fun._run_cmd(f'''wmic process where "name='{target}'" delete''').stdout
            # wmic process get caption,CSName,ProcessID 查看正在运行的进程
            return '删除实例' in temp  # 删除成功就会return True

        @staticmethod
        def download(target):  # 判断有没有不如直接删除之前
            # Download之前要先判断是否已经下载过
            file_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Downloads\\{target}')  # 下载到桌面
            # TODO 我想判断MyWindowsAi文件夹下是否存在target名称的文件
            # directory_path = Path(os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi'))
            # for item in directory_path.rglob('*'):  # 如果已经下载就直接返回路径
            #     if item.name == target:
            #         return item.absolute()
            # if os.path.exists(file_path):  # 如果已经下载就直接返回路径
            #     return file_path
            if target.endswith('.exe'):  # ChromeSetup.exe
                download_url = f'http://{http_host}:5002/download_program/'
            elif target.endswith('.zip'):  # Sample_YOLOv8.zip
                download_url = f'http://{http_host}:5002/download_project/'
            else:  # BG_WindowsAi.png
                download_url = f'http://{http_host}:5002/download_file/'
            with requests.get(download_url + target, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return file_path

        @staticmethod
        def unzip_and_remove(zip_path):
            parent_dir = os.path.dirname(zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(parent_dir)
            os.remove(zip_path)

        @staticmethod
        def move_files(move_from, move_to):
            if os.path.exists(move_to):  # 如果存在就不移动了，直接删除原文件——直接删除好像还有问题，写错了，应该是 move_to 而不是 move_from
                return
            to_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\{move_to}')  # 下载到桌面
            shutil.move(move_from, to_path)

        @staticmethod
        def once_ocr():
            ImageGrab.grab().save(last_img, format='JPEG')
            uuid = get_system_id()
            return requests.post(ocr_url, files={'image': open(last_img, 'rb')}, data={'uuid': uuid}).json()

        # 有问题，所以注释掉
        # @staticmethod
        # def install_python_package(target, log):
        #     mirrors = [  # 定义国内镜像源
        #         "https://mirrors.aliyun.com/pypi/simple/",
        #         "https://pypi.tuna.tsinghua.edu.cn/simple/",
        #         "https://pypi.mirrors.ustc.edu.cn/simple/"
        #     ]
        #     for mirror in mirrors:
        #         command = f"{sys.executable} -m pip install {target} -i {mirror}"
        #         try:
        #             subprocess.check_call(command, shell=True)
        #             log.info(f"{target} 安装成功！（镜像：{mirror}）")
        #             return  # 安装成功后退出函数
        #         except subprocess.CalledProcessError as e:
        #             log.error(f"{target} 安装失败：（镜像：{mirror}），尝试下一个镜像。 错误：{e}")
        #     log.error(f"{target} 在所有镜像源上都安装失败。")

        # @staticmethod
        # def uninstall_python_package(target, log):
        #     command = f"{sys.executable} -m pip uninstall -y {target}"
        #     try:
        #         subprocess.check_call(command, shell=True)
        #         log.info(f"{target} 卸载成功！")
        #     except subprocess.CalledProcessError as e:
        #         log.error(f"{target} 卸载失败：{e}")
