# import ctypes
# import os
# import re
# import shutil
# import subprocess
# import time
# import webbrowser
# import winreg
# import zipfile
# from pathlib import Path
#
# import psutil
# import pyautogui
# import pyperclip
# import win32api
# import win32com.client
# import win32con
# import win32gui
# from PIL import Image, ImageDraw, ImageFont, ImageGrab
# from pynput.mouse import Controller
#
# from OCR import start_ocr_zh, start_ocr_en
# from config import get_language, last_img, my_logger
# from Data import temp_check  # 不要删除
#
# # 关闭 PyAutoGUI 的安全模式
# pyautogui.FAILSAFE = False
# # 预定义所需变量
# MapValue = {}
#
#
# def get_data(key):
#     MapValue.clear()  # 清空之前的变量
#     with open('user_info.txt', 'r', encoding='utf-8') as file:  # 这个文件需要一起打包给用户
#         for line in file:
#             line = line.strip()  # 去掉行末的换行符
#             if '=' in line and line.split('=')[1]:  # 确保该行包含一个等号且不为空 检查是否有等号，并确保右侧有值
#                 temp_key, temp_value = line.split('=')
#                 MapValue[temp_key] = temp_value
#     return MapValue.get(key, 'None')
#
#
# # 每次都会重新从文件读取，就不考虑问题了
# user_name = get_data('user_name')
# user_email = get_data('user_email')
# gitee_user_name = get_data('gitee_user_name')
# gitee_user_password = get_data('gitee_user_password')
# BKPAAS_APP_ID = get_data('BKPAAS_APP_ID')
# BKPAAS_APP_SECRET = get_data('BKPAAS_APP_SECRET')
# BKPAAS_APP_NAME = get_data('BKPAAS_APP_NAME')
#
#
# def start_action(results, action_string, user_message, temp_ocr_text=None, temp_ocr_position=None,
#                  temp_ocr_accuracy_outputs=None):
#     action_list = action_string.split('->')  # 还是用箭头吧，因为有些函数名字比较长，KeyWord也是
#     for action in action_list:
#         # time.sleep(0.25)  # 感觉0.25有点快了——还是在db里添加把，不然会越来越大
#         time.sleep(0.5)  # 我不喜欢它笨笨的感觉，太慢了
#         # 0.5谢谢，安全第一，安全第一
#
#         # 按键
#         if re.search(r"\bKEY\((.*?)\)", action):  # Nice 使用正则匹配减小工作量——加\b是为了完全有且仅有匹配模式
#             target = re.search(r"\bKEY\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 按键')} : {action}")  # 原来要区分引号要
#             MyFun.Input.press(target)
#
#         # 输入内容
#         elif re.search(r"\bINPUT\((.*?)\)", action):
#             target = re.search(r"\bINPUT\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 输入')} : {action}")
#             MyFun.Input.input_content(target)
#
#         elif re.search(r"\bINPUT_PARAM\((.*?)\)", action):
#             target = re.search(r"\bINPUT_PARAM\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 输入参数内容')} : {action}")
#             MyFun.Input.input_param_content(target)
#
#         # TODO INPUT_PARAM WindowsAi-BlueKingProject-{gitee_user_name}
#         # 需要 gitee_user_name、gitee_user_password
#
#         # 组合键
#         elif re.search(r"\bHOTKEY\((.*?)\)", action):
#             target = re.search(r"\bHOTKEY\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 热键')} : {action}")
#             keys = target.split('+')
#             lowercase_keys = [key.lower() for key in keys]  # 转换为小写防止按住Shift模拟大小——这个是必要的
#             MyFun.Input.hot_key(lowercase_keys)
#
#         # OCR点击文本——自带文本语言检测与循环检测
#         elif re.search(r"\bCLICK_TEXT\((.*?)\)", action):
#             target = re.search(r"\bCLICK_TEXT\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 点击文本')} : {action}")
#             MyFun.Input.click_text_auto(target)
#
#         # 遍历并点击所有文本，用户操作文本与标题重复的情况，较为特殊，在蓝鲸开发创建项目时第一次遇到
#         elif re.search(r"\bCLICK_TEXT_ALL\((.*?)\)", action):
#             target = re.search(r"\bCLICK_TEXT_ALL\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 点击全部匹配文本')} : {action}")
#             MyFun.Input.click_text_all(target)
#
#         # OCR点击文本——向上偏移
#         elif re.search(r"\bCLICK_TEXT_UP\((.*?)\)", action):
#             target = re.search(r"\bCLICK_TEXT_UP\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 点击文本并向上偏移')} : {action}")
#             MyFun.Input.click_text_up(target)
#
#         # OCR点击文本——向下偏移
#         elif re.search(r"\bCLICK_TEXT_DOWN\((.*?)\)", action):
#             target = re.search(r"\bCLICK_TEXT_DOWN\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 点击文本并向下偏移')} : {action}")
#             MyFun.Input.click_text_down(target)
#
#         # 点击坐标
#         elif re.search(r"\bCLICK_POS\((.*?)\)", action):
#             target = re.search(r"\bCLICK_POS\((.*?)\)", action).group(1)  # 200,600
#             my_logger.info(f"{get_language('匹配操作 点击坐标')} : {action}")
#             MyFun.Input.click_position(target)
#
#         # FIXME 测试中 按区域点击
#         elif re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action):
#             # target = re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action).group(1)  # TODO 识别出两个参数
#             target = re.search(r"\bCLICK_TEXT_AREA\((.*?),(.*?)\)", action)
#             t1 = target.group(1)  # 区域程序名称
#             t2 = target.group(2)  # 点击文字
#             my_logger.info(f"{get_language('匹配操作 点击区域文本')} : {action}")
#             MyFun.Input.click_text_area(t1, t2, temp_ocr_text, temp_ocr_position)
#
#         # 点击精确文字
#         elif re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action):
#             target = re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 点击精确文本')} : {action}")
#             MyFun.Input.click_text_accuracy(target, temp_ocr_accuracy_outputs)
#
#         # 使用默认浏览器打开网址
#         elif re.search(r"\bWEB_BROWSER\((.*?)\)", action):
#             target = re.search(r"\bWEB_BROWSER\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 打开浏览器')} : {action}")
#             MyFun.System.open_web(target)
#
#         elif re.search(r"\bOPEN_CHROME\((.*?)\)", action):
#             target = re.search(r"\bOPEN_CHROME\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 打开Chrome浏览器')} : {action}")
#             MyFun.System.open_chrome(target)
#
#         # 精准搜索打开 MyWindowsAi/Downloads/ 下文件
#         elif re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action):
#             target = re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 打开下载内容')} : {action}")
#             MyFun.System.open_downloaded(target)
#
#         # 打开已安装程序，系统或 MyWindowsAi/Program/ 下程序
#         elif re.search(r"\bOPEN_INSTALLED\((.*?)\)", action):  # 模糊匹配已安装程序
#             target = re.search(r"\bOPEN_INSTALLED\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 打开安装程序')} : {action}")
#             MyFun.System.open_installed(target)
#
#         # 打开系统程序，如用户帐户控制、程序和功能
#         elif re.search(r"\bOPEN_SYSTEM\((.*?)\)", action):  # 打开系统程序
#             target = re.search(r"\bOPEN_SYSTEM\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 打开系统程序')} : {action}")
#             MyFun.System.open_system(target)
#
#         # FIXME 检查程序是否存在
#         elif re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action):
#             target = re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 检查程序是否存在')} : {action}")
#             MyFun.System.check_exe_exists(target)
#
#         # 设置程序焦点
#         elif re.search(r"\bSET_FOCUS\((.*?)\)", action):  # 普通切换
#             target = re.search(r"\bSET_FOCUS\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 设置焦点')} : {action}")
#             check = True
#             while check:
#                 time.sleep(1)
#                 check = MyFun.System.switch_to_windows(target)  # 循环检测
#
#         # 设置全屏焦点
#         elif re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action):  # 全屏切换——有点问题，Chrome安装和普通程序都会被打开隐藏
#             target = re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 设置焦点并全屏')} : {action}")
#             check = True
#             while check:
#                 time.sleep(1)
#                 check = MyFun.System.switch_to_windows_full(target)  # 循环检测
#
#         # 执行函数，如获取WIFI密码，也可以是好玩
#         elif re.search(r"\bFUN\((.*?)\)", action):
#             target = re.search(r"\bFUN\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 执行函数')} : {action}")
#             MyFun.Fun.start_inner_fun(target)
#
#         # 小睡一会
#         elif re.search(r"\bSLEEP\((.*?)\)", action):
#             target = re.search(r"\bSLEEP\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 睡眠')} : {action}")
#             MyFun.Fun.delay(target)
#
#         # 关闭运行窗口/清理后台程序
#         elif re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action):
#             target = re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 关闭程序窗口')} : {action}")
#             MyFun.Fun.close_windows(target)
#
#         # TODO
#         # 下载文件，默认保存在MyWindowsAi/Download目录下
#         elif re.search(r"\bDOWNLOAD\((.*?)\)", action):
#             target = re.search(r"\bDOWNLOAD\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 下载内容')} : {action}")
#             temp = MyFun.Fun.download(target)  # download不见了
#             if temp.endswith('.zip'):
#                 with zipfile.ZipFile(temp, 'r') as zip_ref:
#                     files = zip_ref.namelist()  # 获取压缩包内的文件列表
#                     for file in files:  # 原地解压文件
#                         zip_ref.extract(file, os.path.dirname(temp))
#                 os.remove(temp)  # 解压完成后删除压缩包
#                 my_logger.info(f"{get_language('删除压缩包')} : {temp}")
#
#         # 输入安装目录到 MyWindowsAi/Project/{target} 下
#         elif re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action):  # 下载程序文件，默认保存在MyWindowsAi/Download目录下
#             target = re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 输入安装地址')} : {action}")
#             MyFun.Input.input_download(target)
#
#         # 输入项目目录到 MyWindowsAi/Project/{target} 下
#         elif re.search(r"\bINPUT_PROJECT\((.*?)\)", action):
#             target = re.search(r"\bINPUT_PROJECT\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 输入项目地址')} : {action}")
#             MyFun.Input.input_project(target)
#
#         elif re.search(r"\bGOTO\((.*?)\)", action):
#             target = re.search(r"\bGOTO\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 跳转')} : {action}")
#             # 先查找，再执行 Nice
#             for y in results:  # 这个是必中的
#                 if y[0] == target:  # 这里需要修改，一直是这里报错，注意，将 2 改为 0 ， 将 3 改为 1
#                     start_action(results, y[1], my_logger, user_message)
#                     break
#
#         # 循环OCR，并等待检测target
#         elif re.search(r"\bWAIT_OCR\((.*?)\)", action):
#             target = re.search(r"\bWAIT_OCR\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 等待文本出现')} : {action}")
#             while True:
#                 time.sleep(1)
#                 language_result = MyFun.Fun._detect_language_status([target])
#                 if language_result == 'ZH':
#                     ocr_outputs = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     ocr_outputs = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
#                     break
#
#         elif re.search(r"\bWAIT_OCR_END\((.*?)\)", action):
#             target = re.search(r"\bWAIT_OCR_END\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 等待文本出现并消失')} : {action}")
#             while True:  # 等待文本出现
#                 time.sleep(1)
#                 language_result = MyFun.Fun._detect_language_status([target])
#                 if language_result == 'ZH':
#                     ocr_outputs = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     ocr_outputs = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 if any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
#                     break
#             while True:  # 等待文本消失
#                 time.sleep(1)
#                 language_result = MyFun.Fun._detect_language_status([target])
#                 if language_result == 'ZH':
#                     ocr_outputs = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     ocr_outputs = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 if not any(MyFun.Fun.fuzzy_search(target, item['text']) for item in ocr_outputs):
#                     break
#
#         # SELECT_OCR() 匹配数据库OCR 如 OCR(%ABC%)
#         elif action == 'SELECT_OCR()':
#             _Flag = True
#             my_logger.info(f"{get_language('匹配操作 特征文本转操作')} : {action}")
#             target_list = []
#             action_list = []
#             for y in results:  # 这个是必中的
#                 if re.search(r"\bOCR\((.*?)\)", y[0]):
#                     target = re.search(r"\bOCR\((.*?)\)", y[0]).group(1)
#                     # TODO 判断 target 语言类型
#                     target_list.append(target)
#                     action_list.append(y[1])
#             while _Flag:
#                 time.sleep(1)
#                 language_result = MyFun.Fun._detect_language_status(target_list)
#                 if language_result == 'ZH':
#                     ocr_outputs = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     ocr_outputs = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 for x in ocr_outputs:
#                     for index, y in enumerate(target_list):
#                         if MyFun.Fun.fuzzy_search(y, x['text']):
#                             _Flag = False
#                             start_action(results, action_list[index], my_logger, user_message)
#
#         elif re.search(r"\bMOVE_FILE\((.*?)\)", action):
#             target = re.search(r"\bMOVE_FILE\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 移动文件')} : {action}")
#             MyFun.System._move_file(target)
#
#         elif re.search(r"\bADD_SYSTEM_PATH\((.*?)\)", action):
#             target = re.search(r"\bADD_SYSTEM_PATH\((.*?)\)", action).group(1)
#             my_logger.info(f"{get_language('匹配操作 添加系统路径')} : {action}")
#             MyFun.Fun._add_system_path(target)
#
#         # -----------------------------------
#
#         # FIXME 右键
#         elif action == 'CLICK_RIGHT()':  # 无参函数
#             my_logger.info(f"{get_language('匹配操作 右键')} : {action}")
#             MyFun.Input.click_right()
#
#         # 鼠标向下滑动
#         elif action == 'MOUSE_SLIDE_DOWN()':  # 无参函数
#             my_logger.info(f"{get_language('匹配操作 向下滑动鼠标')} : {action}")
#             MyFun.Input.mouse_slide_down()
#
#         elif action == 'FINISH()':  # 无参函数
#             my_logger.info(f"{get_language('匹配操作 程序结束')} : {action}")
#             MyFun.System.finish()
#             # 我想让它执行完成后返回聊天内容
#             global temp_check
#             temp_check['Value'] = True
#
#         else:
#             text = f"{get_language('操作未定义')} : {action}"
#             my_logger.critical(text)
#             raise ModuleNotFoundError(text)
#             # return  # return会无法显示错误信息，所以还是用raise吧
#
#
# class MyFun:
#     class System:  # 系统预处理
#
#         @staticmethod
#         def get_all_programs_from_start_menu():  # 这个是检测不到安装包的
#             start_menu_dirs = [
#                 os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
#                 os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs")
#             ]
#             all_programs = []
#             for directory in start_menu_dirs:
#                 program_list = []
#                 for root, dirs, files in os.walk(directory):
#                     for file in files:
#                         if file.lower().endswith(".lnk"):
#                             shortcut_path = os.path.join(root, file)
#                             shell = win32com.client.Dispatch("WScript.Shell")
#                             shortcut = shell.CreateShortcut(shortcut_path)
#                             target_path = shortcut.Targetpath
#                             if target_path and os.path.exists(target_path):
#                                 program_list.append(target_path)
#                 all_programs.extend(program_list)
#             return all_programs
#
#         @staticmethod
#         def _get_running_windows():  # 枚举当前正在运行的所有窗口
#             def callback(tmp_hwnd, tmp_windows):
#                 if win32gui.IsWindowVisible(tmp_hwnd) and win32gui.GetWindowText(tmp_hwnd):
#                     tmp_windows.append((tmp_hwnd, win32gui.GetWindowText(tmp_hwnd)))
#                 return True
#
#             windows_list = []
#             win32gui.EnumWindows(callback, windows_list)
#             return windows_list
#
#         @staticmethod
#         def run_cmd(tmp_cmd):
#             result = subprocess.run(tmp_cmd, capture_output=True, text=True, shell=True)
#             return result.stdout
#
#         @staticmethod
#         def _get_installed_programs():
#             installed_programs = []
#             reg_flags = winreg.KEY_READ | winreg.KEY_WOW64_32KEY  # 64位系统下访问32位注册表需要加上 winreg.KEY_WOW64_32KEY 标志
#             try:
#                 reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
#                 with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, reg_flags) as key:
#                     for i in range(winreg.QueryInfoKey(key)[0]):
#                         sub_key_name = winreg.EnumKey(key, i)
#                         with winreg.OpenKey(key, sub_key_name) as sub_key:
#                             try:
#                                 program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
#                                 installed_programs.append(program_name)
#                             except FileNotFoundError:
#                                 continue
#             except Exception as e:
#                 print(f"Error accessing HKEY_LOCAL_MACHINE: {e}")
#             try:
#                 reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
#                 with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, reg_flags) as key:
#                     for i in range(winreg.QueryInfoKey(key)[0]):
#                         sub_key_name = winreg.EnumKey(key, i)
#                         with winreg.OpenKey(key, sub_key_name) as sub_key:
#                             try:
#                                 program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
#                                 if program_name not in installed_programs:
#                                     installed_programs.append(program_name)
#                             except FileNotFoundError:
#                                 continue
#             except Exception as e:
#                 print(f"Error accessing HKEY_CURRENT_USER: {e}")
#             return installed_programs
#
#         @staticmethod
#         def is_admin():  # 判断是否为管理员，因非管理员打开会导致程序无效
#             try:
#                 return ctypes.windll.shell32.IsUserAnAdmin()
#             except OSError:  # 未测试 OSError
#                 return False
#
#         @staticmethod
#         def kill_processes(processes_name):  # 关闭程序进程
#             running_processes = psutil.process_iter()
#             for process in running_processes:
#                 if process.name() == processes_name:  # Photos.exe
#                     process.terminate()  # 发送终止信号
#                     process.wait()  # 等待进程终止
#
#         @staticmethod
#         def switch_to_windows(name_like):
#             time.sleep(1)  # SET_FOCUS应该等待一秒，不然容易出现问题——No error message is available——最好别动，不着急那一两秒
#             windows = MyFun.System._get_running_windows()
#             temp = []
#             for hwnd, title in windows:
#                 temp.append(title)
#             my_logger.info(f"{get_language('找到程序窗口')} : {temp}")
#             for hwnd, title in windows:
#                 if name_like in title:  # 模糊搜索，其实也可以精准搜索，只要字足够多
#                     my_logger.info(f"{get_language('切换到程序窗口')} : {title}")  # 多了一个大括号。。
#                     win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 原设置
#                     win32gui.SetForegroundWindow(hwnd)  # 执行操作
#                     # TODO 尝试使用新方法，这个可能遇到系统权限限制
#                     # shell = win32com.client.Dispatch("WScript.Shell")
#                     # shell.SendKeys('%')  # 按下Alt键
#                     # win32gui.SetForegroundWindow(hwnd)  # 执行操作
#                     time.sleep(1)  # 给点延迟，防止下一步时程序没有反应过来
#                     return False  # 正常返回False，终止循环
#             return True
#
#         @staticmethod
#         def switch_to_windows_full(name_like):
#             windows = MyFun.System._get_running_windows()
#             for hwnd, title in windows:
#                 if name_like in title:  # 模糊搜索
#                     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 最大化
#                     win32gui.SetForegroundWindow(hwnd)  # 执行操作
#                     return False  # 正常返回False，终止循环
#             return True
#
#         @staticmethod
#         def open_web(target_url):  # 以默认方式打开浏览器
#             webbrowser.open(target_url)
#
#         @staticmethod
#         def open_chrome(target_url):  # 打开Chrome浏览器
#             MyFun.Fun._open_chrome(target_url)
#
#         @staticmethod
#         def open_downloaded(target_exe):  # 下载安装程序
#             downloads_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Downloads')
#             if os.path.exists(downloads_path):  # 检查下载文件夹是否存在
#                 for item in os.listdir(downloads_path):  # 遍历下载文件夹中的所有项
#                     # if target_exe in item:  # ChromeSetup.exe
#                     if target_exe == item:  # ChromeSetup.exe
#                         target_path = os.path.join(downloads_path, item)
#                         os.startfile(target_path)  # 这个更具通用性 Nice
#                         break
#
#         @staticmethod
#         def open_installed(target_exe):  # 快速打开程序，自带SetFocus
#             programs = MyFun.System.get_all_programs_from_start_menu()
#             for program in programs:
#                 if target_exe in program:
#                     os.startfile(program)
#                     break
#
#         @staticmethod
#         def open_system(target_exe):
#             if target_exe == 'UserAccountControlSettings':
#                 subprocess.Popen(r'C:\Windows\System32\UserAccountControlSettings.exe')  # 可以先写个检测程序检测这些路径是否存在
#                 time.sleep(0.2)  # 时间不确定，等待实战测试
#                 MyFun.System.switch_to_windows(get_language('用户帐户控制设置'))  # 切换焦点，稳妥起见
#             # 默认在下载位置，所以遍历下载文件查找
#             elif target_exe == 'ProgramAndFunction':
#                 subprocess.call('appwiz.cpl', shell=True)  # 这个是打开卸载，比系统自带的好用
#                 time.sleep(0.2)
#                 MyFun.System.switch_to_windows(get_language('程序和功能'))  # 已验证
#
#         @staticmethod
#         def check_exe_exists(target):  # 检查文件是否存在
#             exist_exe_list = MyFun.System._get_installed_programs()
#             if target in exist_exe_list:
#                 # TODO 未测试
#                 print(f'{target} Exists!')
#
#         @staticmethod
#         def finish():
#             my_logger.info(f"{get_language('程序已结束')}")
#             MyFun.System.kill_processes('Photos.exe')  # 推荐使用精准关闭
#
#         @staticmethod
#         def _move_file(target):
#             _from = target.split(',')[0]  # cudnn-windows-x86_64-8.9.7.29_cuda12-archive\\include
#             _to = target.split(',')[1]  # C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6
#             # 源 include 文件夹的完整路径
#             source_dir = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Downloads\\{_from}')
#             # 目标路径，直接复制 include 文件夹到此路径下
#             dest_dir = os.path.join(_to, os.path.basename(_from))
#             # 确保目标路径存在
#             os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
#             # 移动 include 文件夹到目标路径
#             try:
#                 shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)  # 文件存在则直接覆盖
#             except Exception as e:  # 移动不成功会报错，所以可信度比较高
#                 print(f"{get_language('转移文件夹时发生错误')} {e}")
#
#     class Init:  # 程序预处理
#
#         @staticmethod
#         def create_directories(base_dir, sub_dirs):  # 这里不使用log，因为还没有新建文件夹
#             desktop_path = Path.home() / "Desktop"
#             base_dir_path = desktop_path / base_dir
#             if not os.path.exists(base_dir_path):  # 创建基础文件夹
#                 os.makedirs(base_dir_path)
#             for sub_dir in sub_dirs:  # 创建子文件夹
#                 dir_path = base_dir_path / sub_dir
#                 if not os.path.exists(dir_path):
#                     os.makedirs(dir_path)
#
#         @staticmethod
#         def _draw_bg_img(path):  # 绘制背景图片
#             width, height = pyautogui.size()
#             background_color = (64, 64, 64)  # 深灰色
#             image = Image.new('RGB', (width, height), background_color)
#             draw = ImageDraw.Draw(image)
#             text = "WindowsAi"
#             font_size = 200
#             font_color = (255, 255, 255)  # 白色
#             font = ImageFont.truetype("arial.ttf", font_size)
#             bbox = draw.textbbox((0, 0), text, font=font)
#             text_width = bbox[2] - bbox[0]
#             text_height = bbox[3] - bbox[1]
#             text_x = (width - text_width) // 2
#             text_y = (height - text_height) // 2
#             draw.text((text_x, text_y), text, fill=font_color, font=font)
#             image.save(path)
#
#         @staticmethod
#         def show_bg():  # 打开背景图像
#             img_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Configs\\BG_WindowsAi.png')  # 路径错误，所以打开不对
#             time.sleep(1)
#             subprocess.Popen(['explorer', img_path])  # 使用explorer打开图片
#             time.sleep(3)  # 给几秒让他加载会——因为不确定打开时间——要不要写个程序专门监听——不行，尝试失败
#             pyautogui.hotkey('F11')  # 虚拟机没有全屏快捷键，只在最右下角有
#
#     class Input:
#         @staticmethod
#         def average_position(points):
#             sum_x = 0
#             sum_y = 0
#             for point in points:
#                 sum_x += point[0]
#                 sum_y += point[1]
#             avg_x = sum_x / len(points)
#             avg_y = sum_y / len(points)
#             return avg_x, avg_y
#
#         @staticmethod
#         def _smooth_move_win32(x, y, duration=1, steps=100):  # 平滑移动——最快一秒，你自己看着办吧
#             start_x, start_y = win32api.GetCursorPos()
#             x_distance = x - start_x
#             y_distance = y - start_y
#             for i in range(steps):
#                 progress = i / steps
#                 if progress < 0.5:
#                     easing_progress = 2 * progress * progress
#                 else:
#                     easing_progress = -1 + (4 - 2 * progress) * progress
#                 move_to_x = round(start_x + x_distance * easing_progress)
#                 move_to_y = round(start_y + y_distance * easing_progress)
#                 win32api.SetCursorPos((move_to_x, move_to_y))
#                 time.sleep(duration / steps)
#
#         @staticmethod
#         def click(x, y):  # 点击位置
#             pyautogui.click(x, y)
#
#         @staticmethod
#         def click_right():  # 右键
#             pyautogui.rightClick()
#
#         @staticmethod
#         def mouse_slide_down():
#             Controller().scroll(0, -10)
#
#         @staticmethod
#         def press(key):  # 按键
#             pyautogui.press(key)
#
#         @staticmethod
#         def hot_key(keys):  # 按键
#             pyautogui.hotkey(keys)
#
#         @staticmethod
#         def click_text_auto(target_text):  # 平滑点击文字
#             __flag = True
#             while __flag:
#                 time.sleep(1)  # 忘记给延迟了
#                 language_result = MyFun.Fun._detect_language_status([target_text])
#                 if language_result == 'ZH':
#                     temp_results = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     temp_results = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 text_list = []
#                 pos_list = []
#                 for item in temp_results:
#                     text_list.append(item['text'])
#                     ave_pos = MyFun.Input.average_position(item['position'])  # 别忘了
#                     pos_list.append(ave_pos)
#                 for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
#                     # 应该加一个模糊匹配才对
#                     if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
#                         MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
#                         MyFun.Input.click(pos_list[index][0], pos_list[index][1])
#                         __flag = False
#                         break
#
#         @staticmethod
#         def click_text_all(target_text):
#             __flag = True
#             while __flag:
#                 time.sleep(1)
#                 language_result = MyFun.Fun._detect_language_status([target_text])
#                 if language_result == 'ZH':
#                     temp_results = MyFun.Fun.once_ocr_zh()
#                 elif language_result == 'EN':
#                     temp_results = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 text_list = []
#                 pos_list = []
#                 for item in temp_results:
#                     text_list.append(item['text'])
#                     ave_pos = MyFun.Input.average_position(item['position'])
#                     pos_list.append(ave_pos)
#                 for index, value in enumerate(text_list):
#                     if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):
#                         MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
#                         MyFun.Input.click(pos_list[index][0], pos_list[index][1])
#                         __flag = False
#                         # break # 注释 break 以连续点击多个相同的文字
#
#         @staticmethod
#         def click_text_up(target_text):  # 平滑点击文字
#             temp = target_text.split(',')  # 文本,50
#             target_text = temp[0]
#             offset = temp[1]  # 向上为UP，向下为DOWN
#             __flag = True
#             while __flag:
#                 time.sleep(1)  # 忘记给延迟了
#                 language_result = MyFun.Fun._detect_language_status([target_text])
#                 if language_result == 'ZH':
#                     temp_results = MyFun.Fun.once_ocr_zh()  # 获取画面信息
#                 elif language_result == 'EN':
#                     temp_results = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 text_list = []
#                 pos_list = []
#                 for item in temp_results:
#                     text_list.append(item['text'])
#                     ave_pos = MyFun.Input.average_position(item['position'])  # 别忘了
#                     pos_list.append(ave_pos)
#                 for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
#                     if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):  # 应该加一个模糊匹配才对
#                         MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
#                         MyFun.Input.click(pos_list[index][0], pos_list[index][1] - int(offset))
#                         __flag = False
#                         break
#
#         @staticmethod
#         def click_text_down(target_text):  # 平滑点击文字
#             temp = target_text.split(',')  # 文本,50
#             target_text = temp[0]
#             offset = temp[1]
#             __flag = True
#             while __flag:
#                 time.sleep(1)  # 忘记给延迟了
#                 language_result = MyFun.Fun._detect_language_status([target_text])
#                 if language_result == 'ZH':
#                     temp_results = MyFun.Fun.once_ocr_zh()  # 获取画面信息
#                 elif language_result == 'EN':
#                     temp_results = MyFun.Fun.once_ocr_en()
#                 else:
#                     raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
#                 text_list = []
#                 pos_list = []
#                 for item in temp_results:
#                     text_list.append(item['text'])
#                     ave_pos = MyFun.Input.average_position(item['position'])  # 别忘了
#                     pos_list.append(ave_pos)
#                 for index, value in enumerate(text_list):  # 注意点击文字是没有模糊匹配的
#                     if MyFun.Fun.fuzzy_search(target_text.lower(), value.lower()):  # 应该加一个模糊匹配才对
#                         MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
#                         MyFun.Input.click(pos_list[index][0], pos_list[index][1] + int(offset))
#                         __flag = False
#                         break
#
#         @staticmethod
#         def click_position(position):  # 点击坐标
#             x, y = position.split(',')
#             x = int(x)  # 没有转换类型导致错误
#             y = int(y)
#             MyFun.Input._smooth_move_win32(x, y)
#             MyFun.Input.click(x, y)
#
#         @staticmethod
#         def click_text_area(space, target_text, text_list, pos_list):  # 平滑点击文字
#             if space == 'ProgramAndFunction':  # 这里应该使用数据库，但前期简单一点就直接写坐标
#                 x1, x2, y1, y2 = 250, 1375, 270, 1000  # x应该在x1-x2之间，y同理
#             else:
#                 # TODO 等待测试
#                 raise ModuleNotFoundError('找不到区域程序!')
#             for index, value in enumerate(text_list):
#                 if target_text in value:  # 这里使用in，因为限制了区域
#                     if pos_list[index][0] in range(x1, x2) and pos_list[index][1] in range(y1, y2):
#                         MyFun.Input._smooth_move_win32(pos_list[index][0], pos_list[index][1])
#                         MyFun.Input.click(pos_list[index][0], pos_list[index][1])
#                         break
#
#         @staticmethod
#         def input_content(target_text):
#             old_clip = pyperclip.paste()
#             pyperclip.copy(target_text)
#             pyautogui.hotkey('ctrl', 'a')  # 新增全选
#             pyautogui.hotkey('ctrl', 'v')
#             pyperclip.copy(old_clip)  # 恢复之前的剪切数据
#
#         @staticmethod
#         def input_param_content(target_text):  # 这次一定行
#             pattern = re.compile(r'\{(\w+)}')
#
#             def replace_variable(match):
#                 key = match.group(1)  # 提取变量名
#                 if key in MapValue:
#                     return MapValue[key]  # 返回字典中对应的值
#                 else:
#                     my_logger.error(f"未找到参数 : {{{key}}}")
#                     raise ValueError(f"未找到参数 : {{{key}}}")
#
#             # 替换字符串中的变量
#             result_text = pattern.sub(replace_variable, target_text)
#             my_logger.info(f"已替换参数 : {result_text}")
#             MyFun.Input.input_content(result_text)
#
#         @staticmethod
#         def input_download(target):  # 传入文件夹名称，默认在 MyWindowsAi/Program
#             downloads_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Programs\\{target}')
#             MyFun.Input.input_content(downloads_path)
#
#         @staticmethod
#         def input_project(target):  # 传入文件夹名称，默认在 MyWindowsAi/Projects
#             project_path = os.path.join(os.path.expanduser('~'), f'Desktop\\MyWindowsAi\\Projects\\{target}')
#             MyFun.Input.input_content(project_path)
#
#         @staticmethod
#         def click_text_accuracy(target_text, accuracy_info):  # 平滑点击精确文字
#             pos_list = []
#             for temp_result in accuracy_info:
#                 text = temp_result['text']
#                 text_word = temp_result['text_word']
#                 text_word_region = temp_result['text_word_region']
#                 if target_text in text:
#                     full_string = ''.join(text_word)
#                     start_index = full_string.find(target_text)
#                     if start_index != -1:
#                         end_index = start_index + len(target_text)
#                         for i in range(start_index, end_index):
#                             pos_list.append(text_word_region[i])
#                         ave_list = []
#                         for item_position in pos_list:
#                             ave_pos = MyFun.Input.average_position(item_position)
#                             ave_list.append(ave_pos)
#                         ave_x = 0
#                         ave_y = 0
#                         for item in ave_list:
#                             ave_x += item[0]
#                             ave_y += item[1]
#                         x, y = ave_x / len(ave_list), ave_y / len(ave_list)
#                         MyFun.Input._smooth_move_win32(x, y)  # 移动后要点击呢
#                         MyFun.Input.click(x, y)
#                         break
#
#         @staticmethod
#         def _click_center():
#             # 获取屏幕的宽度和高度
#             screen_width, screen_height = pyautogui.size()
#             # 计算屏幕中心的坐标
#             center_x, center_y = screen_width // 2, screen_height // 2
#             # 移动鼠标到屏幕中心并点击
#             MyFun.Input._smooth_move_win32(center_x, center_y)
#             MyFun.Input.click(center_x, center_y)
#
#     class Fun:
#         @staticmethod
#         def _run_cmd(cmd):
#             return subprocess.run(cmd, shell=True, capture_output=True, text=True)
#
#         @staticmethod
#         def start_inner_fun(target_fun):
#             if target_fun == 'GET_WIFI_PASSWORD':
#                 names, passwords = MyFun.Fun._get_wifi_status()
#                 tmp_list = []
#                 for name, password in zip(names, passwords):
#                     tmp_list.append(f'{name} : {password}')
#                 write_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Statics')
#                 with open(f'{write_path}/wifi_result.txt', 'w', encoding='utf-8') as f:
#                     for item in tmp_list:
#                         f.write(item + '\n\n')
#                     f.close()  # 关闭文件
#                 os.startfile(f'{write_path}/wifi_result.txt')
#                 time.sleep(1.5)
#                 MyFun.System.switch_to_windows_full('wifi_result.txt')  # 切换焦点
#             elif target_fun == 'CHECK_SYSTEM_VISION':
#                 check = MyFun.Fun._get_windows_version()
#                 if not check:
#                     text = get_language('请升级为 Windows 10/11 家庭版以上版本')
#                     my_logger.error(text)
#                     raise ValueError(text)
#             elif target_fun == 'CHECK_SYSTEM_GPU':
#                 check = MyFun.Fun._is_gpu_available()
#                 if not check:
#                     text = get_language('未检测到GPU')
#                     my_logger.error(text)
#                     raise ValueError(text)
#             elif target_fun == 'START_HYPER_V':
#                 MyFun.Fun._start_hyper_v()
#             # TODO 再给一个关闭Hyper-V的函数
#             elif target_fun == 'CLICK_CENTER':
#                 MyFun.Input._click_center()
#             elif target_fun == 'INIT_GIT':
#                 MyFun.Fun._init_git()
#             elif target_fun == 'BK_REPLACE_TEXT':
#                 MyFun.Fun._bk_replace_text()
#             elif target_fun == 'BK_INIT_DB':
#                 MyFun.Fun._bk_init_db()
#             elif target_fun == 'ADD_HOST':
#                 MyFun.Fun._add_host()
#             else:
#                 text = f"{get_language('未知函数')} : {target_fun}"
#                 my_logger.error(text)
#                 raise ValueError(text)
#
#         @staticmethod
#         def _get_wifi_status():  # 获取所有连接过的WIFI的密码
#             output = MyFun.System.run_cmd('netsh wlan show profiles')
#             wifi_name_list = []
#             wifi_password_list = []
#             lines = output.strip().split('\n')
#             user_profiles = [line.strip().split(' : ')[-1] for line in lines if get_language('所有用户配置文件') in line]
#             for profile in user_profiles:
#                 wifi_name_list.append(profile)
#             for item in wifi_name_list:
#                 output = MyFun.System.run_cmd(f'netsh wlan show profile name="{item}" key=clear')
#                 if output is not None:  # 安全防护
#                     match = re.search(r"关键内容\s*:\s*(\S+)", output)
#                     if match:
#                         password = match.group(1)
#                         wifi_password_list.append(password)
#                     else:
#                         wifi_password_list.append('检索失败')
#                 else:
#                     wifi_password_list.append('检索失败')
#             return wifi_name_list, wifi_password_list
#
#         @staticmethod  # 基于字符串的模糊搜索
#         def fuzzy_search(string1, string2):  # str1 == %s%
#             if string1.startswith('%') and string1.endswith('%'):  # %s% 表示模糊搜索
#                 regex_pattern = string1.replace('%', '.*')
#             elif string1.startswith('%'):  # %s 表示前置模糊搜索
#                 regex_pattern = string1.replace('%', '.*') + '$'
#             elif string1.endswith('%'):  # s% 表示后置模糊搜索
#                 regex_pattern = '^' + string1.replace('%', '.*')
#             else:  # s 表示原文搜索
#                 regex_pattern = '^' + string1 + '$'
#             return bool(re.search(regex_pattern, string2, re.IGNORECASE))  # 使用正则表达式进行搜索
#
#         @staticmethod
#         def delay(target):  # 小睡一会
#             delay_time = float(target)
#             time.sleep(delay_time)
#
#         @staticmethod
#         def close_windows(target):  # 关闭程序进程，用于卸载预处理
#             temp = MyFun.Fun._run_cmd(f'''wmic process where "name='{target}'" delete''').stdout
#             # wmic process get caption,CSName,ProcessID 查看正在运行的进程
#             return get_language('删除实例') in temp  # 删除成功就会return True
#
#         @staticmethod
#         def once_ocr_zh():
#             ImageGrab.grab().save(last_img, format='JPEG')
#             return start_ocr_zh(last_img)
#
#         @staticmethod
#         def once_ocr_en():
#             ImageGrab.grab().save(last_img, format='JPEG')
#             return start_ocr_en(last_img)
#
#         @staticmethod
#         def _get_windows_version():
#             # 执行 WMIC 命令并读取输出
#             output = os.popen('wmic os get Caption').read().strip()
#             # 判定 Windows 10 和 Windows 11 的不同版本
#             if get_language('Windows 11 专业工作站版') in output:
#                 return True
#             elif get_language('Windows 11 专业版') in output:
#                 return True
#             elif get_language('Windows 11 家庭版') in output:
#                 return False
#             elif get_language('Windows 11 企业版') in output:
#                 return True
#             elif get_language('Windows 11 教育版') in output:
#                 return True
#             elif get_language('Windows 10 专业工作站版') in output:
#                 return True
#             elif get_language('Windows 10 专业版') in output:
#                 return True
#             elif get_language('Windows 10 家庭版') in output:
#                 return False
#             elif get_language('Windows 10 企业版') in output:
#                 return True
#             elif get_language('Windows 10 教育版') in output:
#                 return True
#             else:
#                 return False
#
#         @staticmethod
#         def _is_gpu_available():
#             geforce_gpu_list = [
#                 "NVIDIA GeForce RTX 4090",
#                 "NVIDIA GeForce RTX 4080",
#                 "NVIDIA GeForce RTX 4070 Ti",
#                 "NVIDIA GeForce RTX 3090 Ti",
#                 "NVIDIA GeForce RTX 3090",
#                 "NVIDIA GeForce RTX 3080 Ti",
#                 "NVIDIA GeForce RTX 3080",
#                 "NVIDIA GeForce RTX 3070 Ti",
#                 "NVIDIA GeForce RTX 3070",
#                 "NVIDIA GeForce RTX 3060 Ti",
#                 "NVIDIA GeForce RTX 3060",
#                 "NVIDIA GeForce GTX 1650 Ti",
#                 "NVIDIA TITAN RTX",
#                 "NVIDIA GeForce RTX 2080 Ti",
#                 "NVIDIA GeForce RTX 2080",
#                 "NVIDIA GeForce RTX 2070",
#                 "NVIDIA GeForce RTX 2060",
#                 "NVIDIA TITAN V",
#                 "NVIDIA TITAN Xp",
#                 "NVIDIA TITAN X",
#                 "NVIDIA GeForce GTX 1080 Ti",
#                 "NVIDIA GeForce GTX 1080",
#                 "NVIDIA GeForce GTX 1070 Ti",
#                 "NVIDIA GeForce GTX 1070",
#                 "NVIDIA GeForce GTX 1060",
#                 "NVIDIA GeForce GTX 1050",
#                 "NVIDIA GeForce GTX TITAN X",
#                 "NVIDIA GeForce GTX TITAN Z",
#                 "NVIDIA GeForce GTX TITAN Black",
#                 "NVIDIA GeForce GTX TITAN",
#                 "NVIDIA GeForce GTX 980 Ti",
#                 "NVIDIA GeForce GTX 980",
#                 "NVIDIA GeForce GTX 970",
#                 "NVIDIA GeForce GTX 960",
#                 "NVIDIA GeForce GTX 950",
#                 "NVIDIA GeForce GTX 780 Ti",
#                 "NVIDIA GeForce GTX 780",
#                 "NVIDIA GeForce GTX 770",
#                 "NVIDIA GeForce GTX 760",
#                 "NVIDIA GeForce GTX 750 Ti",
#                 "NVIDIA GeForce GTX 750",
#                 "NVIDIA GeForce GTX 690",
#                 "NVIDIA GeForce GTX 680",
#                 "NVIDIA GeForce GTX 670",
#                 "NVIDIA GeForce GTX 660 Ti",
#                 "NVIDIA GeForce GTX 660",
#                 "NVIDIA GeForce GTX 650 Ti BOOST",
#                 "NVIDIA GeForce GTX 650 Ti",
#                 "NVIDIA GeForce GTX 650",
#                 "NVIDIA GeForce GTX 560 Ti",
#                 "NVIDIA GeForce GTX 550 Ti",
#                 "NVIDIA GeForce GTX 460",
#                 "NVIDIA GeForce GTS 450",
#                 "NVIDIA GeForce GT 740",
#                 "NVIDIA GeForce GT 730",
#                 "NVIDIA GeForce GT 730 DDR3 128位",
#                 "NVIDIA GeForce GT 720",
#                 "NVIDIA GeForce GT 705",
#                 "NVIDIA GeForce GT 640 (GDDR5)",
#                 "NVIDIA GeForce GT 640 GDDR3",
#                 "NVIDIA GeForce GT 630",
#                 "NVIDIA GeForce GT 620",
#                 "NVIDIA GeForce GT 610",
#                 "NVIDIA GeForce GT 520",
#                 "NVIDIA GeForce GT 440"
#             ]
#
#             geforce_laptop_gpu_list = [
#                 "NVIDIA GeForce RTX 4090 Laptop GPU",
#                 "NVIDIA GeForce RTX 4080 Laptop GPU",
#                 "NVIDIA GeForce RTX 4070 Laptop GPU",
#                 "NVIDIA GeForce RTX 4060 Laptop GPU",
#                 "NVIDIA GeForce RTX 4050 Laptop GPU",
#                 "NVIDIA GeForce RTX 3080 Ti Laptop GPU",
#                 "NVIDIA GeForce RTX 3080 Laptop GPU",
#                 "NVIDIA GeForce RTX 3070 Ti Laptop GPU",
#                 "NVIDIA GeForce RTX 3070 Laptop GPU",
#                 "NVIDIA GeForce RTX 3060 Ti Laptop GPU",
#                 "NVIDIA GeForce RTX 3060 Laptop GPU",
#                 "NVIDIA GeForce RTX 3050 Ti Laptop GPU",
#                 "NVIDIA GeForce RTX 3050 Laptop GPU",
#                 "NVIDIA GeForce RTX 2080 Laptop GPU",
#                 "NVIDIA GeForce RTX 2070 Laptop GPU",
#                 "NVIDIA GeForce RTX 2060 Laptop GPU",
#                 "NVIDIA GeForce GTX 1080 Laptop GPU",
#                 "NVIDIA GeForce GTX 1070 Laptop GPU",
#                 "NVIDIA GeForce GTX 1060 Laptop GPU",
#                 "NVIDIA GeForce GTX 980 Laptop GPU",
#                 "NVIDIA GeForce GTX 980M Laptop GPU",
#                 "NVIDIA GeForce GTX 970M Laptop GPU",
#                 "NVIDIA GeForce GTX 965M Laptop GPU",
#                 "NVIDIA GeForce GTX 960M Laptop GPU",
#                 "NVIDIA GeForce GTX 950M Laptop GPU",
#                 "NVIDIA GeForce 940M Laptop GPU",
#                 "NVIDIA GeForce 930M Laptop GPU",
#                 "NVIDIA GeForce 920M Laptop GPU",
#                 "NVIDIA GeForce 910M Laptop GPU",
#                 "NVIDIA GeForce GTX 880M Laptop GPU",
#                 "NVIDIA GeForce GTX 870M Laptop GPU",
#                 "NVIDIA GeForce GTX 860M Laptop GPU",
#                 "NVIDIA GeForce GTX 850M Laptop GPU",
#                 "NVIDIA GeForce 840M Laptop GPU",
#                 "NVIDIA GeForce 830M Laptop GPU",
#                 "NVIDIA GeForce 820M Laptop GPU",
#                 "NVIDIA GeForce 800M Laptop GPU",
#                 "NVIDIA GeForce GTX 780M Laptop GPU",
#                 "NVIDIA GeForce GTX 770M Laptop GPU",
#                 "NVIDIA GeForce GTX 765M Laptop GPU",
#                 "NVIDIA GeForce GTX 760M Laptop GPU",
#                 "NVIDIA GeForce GTX 680MX Laptop GPU",
#                 "NVIDIA GeForce GTX 680M Laptop GPU",
#                 "NVIDIA GeForce GTX 675MX Laptop GPU",
#                 "NVIDIA GeForce GTX 675M Laptop GPU",
#                 "NVIDIA GeForce GTX 670MX Laptop GPU",
#                 "NVIDIA GeForce GTX 670M Laptop GPU",
#                 "NVIDIA GeForce GTX 660M Laptop GPU",
#                 "NVIDIA GeForce GT 755M Laptop GPU",
#                 "NVIDIA GeForce GT 750M Laptop GPU",
#                 "NVIDIA GeForce GT 650M Laptop GPU",
#                 "NVIDIA GeForce GT 745M Laptop GPU",
#                 "NVIDIA GeForce GT 645M Laptop GPU",
#                 "NVIDIA GeForce GT 740M Laptop GPU",
#                 "NVIDIA GeForce GT 730M Laptop GPU",
#                 "NVIDIA GeForce GT 640M Laptop GPU",
#                 "NVIDIA GeForce GT 640M LE Laptop GPU",
#                 "NVIDIA GeForce GT 735M Laptop GPU",
#                 "NVIDIA GeForce GT 635M Laptop GPU",
#                 "NVIDIA GeForce GT 730M DDR3 128-bit Laptop GPU",
#                 "NVIDIA GeForce GT 730M DDR3 64-bit Laptop GPU"
#             ]
#
#             try:
#                 # 获取 GPU 信息
#                 result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], capture_output=True,
#                                         text=True)
#                 info = result.stdout
#             except FileNotFoundError:
#                 return "wmic command not found. Make sure you are using a compatible Windows version."
#             # 解析 GPU 信息
#             lines = info.strip().split('\n')
#             if len(lines) < 2:
#                 return False
#             gpu_names = [line.strip() for line in lines[1:] if line.strip()]
#             # 检查是否支持 GPU
#             return any(gpu_name in geforce_gpu_list or gpu_name in geforce_laptop_gpu_list for gpu_name in gpu_names)
#
#         # @staticmethod
#         # # 要不重复，直到成功
#         # def _start_hyper_v():
#         #     # 定义 PowerShell 命令
#         #     powershell_command = """
#         #     Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
#         #     """
#         #     # 执行 PowerShell 命令
#         #     try:
#         #         result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True,
#         #                                 check=True)
#         #         my_logger.info(f"Hyper-V 已成功启用，输出日志 {result.stdout}")
#         #     except subprocess.CalledProcessError as e:
#         #         my_logger.error(f"启用 Hyper-V 时出现错误: {e.stderr}")
#         @staticmethod
#         def _start_hyper_v(max_retries=10):
#             powershell_command = """
#             Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
#             """
#             attempt = 0
#             while attempt < max_retries:
#                 try:
#                     result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True,
#                                             check=True)
#                     my_logger.info(f"Hyper-V 已成功启用，输出日志 {result.stdout}")
#                     return  # 成功后退出函数
#                 except subprocess.CalledProcessError as e:
#                     attempt += 1
#                     my_logger.error(f"启用 Hyper-V 时出现错误: {e.stderr}")
#                     if attempt < max_retries:  # 如果不是最后一次尝试
#                         my_logger.info(f"重试 {attempt}/{max_retries}...")
#                     else:
#                         my_logger.error("已达到最大重试次数，启用 Hyper-V 失败")
#
#         @staticmethod
#         def _detect_language_status(text_list):
#             """
#             对字符串列表中的每个字符串进行语言检测，并输出统一的状态。
#
#             :param text_list: 字符串列表
#             :return: 统一的语言状态，'ZH'（中文）、'EN'（英文）、'MIX'（混合）、'UNKNOWN'（未知）
#             """
#
#             def is_chinese(char):
#                 """判断一个字符是否是中文字符"""
#                 return '\u4e00' <= char <= '\u9fff'
#
#             def is_english(char):
#                 """判断一个字符是否是英文字符"""
#                 return 'a' <= char.lower() <= 'z'
#
#             def detect_language(text):
#                 """
#                 检测字符串是中文还是英文。
#
#                 :param text: 输入的字符串
#                 :return: 返回 'Chinese' 或 'English' 或 'Mixed'（混合）
#                 """
#                 has_chinese = any(is_chinese(char) for char in text)
#                 has_english = any(is_english(char) for char in text)
#
#                 if has_chinese and has_english:
#                     return 'Mixed'
#                 elif has_chinese:
#                     return 'Chinese'
#                 elif has_english:
#                     return 'English'
#                 else:
#                     return 'Unknown'
#
#             # 检测每个字符串的语言
#             statuses = {detect_language(text) for text in text_list}
#             if 'Mixed' in statuses:
#                 return 'MIX'
#             elif 'Chinese' in statuses:
#                 return 'ZH'
#             elif 'English' in statuses:
#                 return 'EN'
#             else:
#                 return 'UNKNOWN'
#
#         @staticmethod
#         def _add_system_path(target):
#             # PowerShell 命令更新环境变量
#             powershell_command = f"""
#                $existingPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
#                if (-not $existingPath.Contains("{target}")) {{
#                    $newPath = "$existingPath;{target}"
#                    [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
#                    Write-Output "PATH 环境变量已更新"
#                }} else {{
#                    Write-Output "路径已在 PATH 环境变量中"
#                }}
#                """
#             try:  # 使用 PowerShell 执行命令
#                 result = subprocess.run(['powershell', '-Command', powershell_command],
#                                         capture_output=True, text=True, check=True)
#                 my_logger.info(f"环境变量已更新，输出日志 {result.stdout}")
#             except subprocess.CalledProcessError as e:
#                 my_logger.error(f"更新环境变量时出现错误: {e.stderr}")
#                 raise SystemExit(f"更新环境变量时出现错误: {e.stderr}")
#
#         @staticmethod
#         def _open_chrome(target_url):
#             chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
#             webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
#             webbrowser.get('chrome').open(target_url)
#
#         @staticmethod
#         def _init_git():  # 定制函数，不需要参数
#             # 获取用户桌面路径
#             work_dir = os.path.join(os.path.expanduser("~"), "Desktop", "MyWindowsAi", "Projects", "BlueKingProject")
#
#             # 定义 Git 命令
#             commands = [
#                 f'git config --global user.name "{user_name}"',  # YOUR_NAME
#                 f'git config --global user.email "{user_email}"',  # YOUR_EMAIL
#                 'git init',
#                 'git add .',
#                 'git commit -m "WindowsAi First Commit"',
#                 f'git remote add origin https://gitee.com/{gitee_user_name}/windows-ai-blue-king-project.git',
#                 'git push -u origin master'
#             ]
#
#             # 执行命令
#             for command in commands:
#                 my_logger.info(f"执行命令: {command}")
#                 process = subprocess.Popen(command, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                 if command == 'git push -u origin master':  # 防止最后一步阻塞线程
#                     return  # 成功后退出函数，同时避免阻塞线程
#                 output, error = process.communicate()
#
#                 # 尝试不同的编码格式
#                 try:
#                     if output:
#                         output_decoded = output.decode('utf-8')  # 尝试UTF-8编码
#                         my_logger.info(f"输出日志: {output_decoded}")
#                 except UnicodeDecodeError:
#                     try:
#                         output_decoded = output.decode('gbk')  # 尝试GBK编码
#                         my_logger.info(f"输出日志: {output_decoded}")
#                     except UnicodeDecodeError:
#                         my_logger.error("无法解码输出日志")
#
#                 try:
#                     if error:
#                         error_decoded = error.decode('utf-8')  # 尝试UTF-8编码
#                         my_logger.error(f"错误日志: {error_decoded}")
#                         raise SystemExit(f"错误日志: {error_decoded}")
#                 except UnicodeDecodeError:
#                     try:
#                         error_decoded = error.decode('gbk')  # 尝试GBK编码
#                         my_logger.error(f"错误日志: {error_decoded}")
#                         raise SystemExit(f"错误日志: {error_decoded}")
#                     except UnicodeDecodeError:
#                         my_logger.error("无法解码错误日志")
#                         raise SystemExit(f"错误日志: 无法解码错误日志")
#
#         @staticmethod
#         def _replace_file_content(old_string, new_string):
#             # 获取用户主目录路径，并构建桌面文件夹路径——完全跨平台
#             file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'MyWindowsAi', 'Projects', 'BlueKingProject',
#                                      'manage.py')
#             try:
#                 # 读取文件内容
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     content = file.read()
#                 # 检查是否有需要替换的内容
#                 if old_string in content:
#                     # 替换内容
#                     new_content = content.replace(old_string, new_string)
#                     # 将替换后的内容写回文件
#                     with open(file_path, 'w', encoding='utf-8') as file:
#                         file.write(new_content)
#                     my_logger.info(f"已成功将 '{old_string}' 替换为 '{new_string}'，并保存至文件 '{file_path}'")
#                 else:
#                     my_logger.error(f"文件中未找到 '{old_string}'")
#                     raise SystemExit(f"文件中未找到 '{old_string}'")
#             except FileNotFoundError:
#                 my_logger.error(f"文件 '{file_path}' 不存在")
#                 raise SystemExit(f"文件 '{file_path}' 不存在")
#             except Exception as e:
#                 my_logger.error(f"出现错误：{e}")
#                 raise SystemExit(f"出现错误：{e}")
#
#         @staticmethod
#         def _bk_replace_text():  # 替换 ID 与 SECRET
#             MyFun.Fun._replace_file_content('{BKPAAS_APP_ID}', BKPAAS_APP_ID)
#             MyFun.Fun._replace_file_content('{BKPAAS_APP_SECRET}', BKPAAS_APP_SECRET)
#
#         @staticmethod
#         def _bk_init_db():  # 初始化数据库
#             mysql_command = 'mysql -u root -p000000'
#             create_db_command = f'CREATE DATABASE `{BKPAAS_APP_ID}` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;'
#             try:
#                 process = subprocess.Popen([mysql_command], stdin=subprocess.PIPE, shell=True, text=True)
#                 process.communicate(input=create_db_command)
#                 my_logger.info(f"命令执行成功: {create_db_command}")
#             except subprocess.CalledProcessError as e:
#                 my_logger.error(f"命令执行失败: {e}")
#                 raise SystemExit(f"命令执行失败: {e}")
#
#         @staticmethod
#         def _add_host():
#             entry = "127.0.0.1 appdev.ce.bktencent.com"
#             hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
#             # 检查是否有管理员权限才能修改系统文件
#             if not os.access(hosts_file, os.W_OK):
#                 my_logger.error("没有权限写入 hosts 文件，请以管理员身份运行该脚本")
#                 raise PermissionError("没有权限写入 hosts 文件，请以管理员身份运行该脚本")
#             # 将新条目追加到 hosts 文件末尾
#             try:
#                 with open(hosts_file, 'a') as file:
#                     file.write(f"\n{entry}\n")
#                 my_logger.info(f"已成功添加条目 '{entry}' 到 hosts 文件 '{hosts_file}'")
#             except Exception as e:
#                 my_logger.error(f"修改 hosts 文件时出现错误: {e}")
#                 raise SystemExit(f"修改 hosts 文件时出现错误: {e}")
