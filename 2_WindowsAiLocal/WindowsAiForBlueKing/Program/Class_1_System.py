import ctypes
import os
import shutil
import subprocess
import time
import webbrowser
import winreg

import psutil
import win32com.client
import win32con
import win32gui

from config import get_language, my_logger


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


def _get_running_windows():  # 枚举当前正在运行的所有窗口
    def callback(tmp_hwnd, tmp_windows):
        if win32gui.IsWindowVisible(tmp_hwnd) and win32gui.GetWindowText(tmp_hwnd):
            tmp_windows.append((tmp_hwnd, win32gui.GetWindowText(tmp_hwnd)))
        return True

    windows_list = []
    win32gui.EnumWindows(callback, windows_list)
    return windows_list


def run_cmd(tmp_cmd):
    result = subprocess.run(tmp_cmd, capture_output=True, text=True, shell=True)
    return result.stdout


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


def is_admin():  # 判断是否为管理员，因非管理员打开会导致程序无效
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except OSError:  # 未测试 OSError
        return False


def kill_processes(processes_name):  # 关闭程序进程
    running_processes = psutil.process_iter()
    for process in running_processes:
        if process.name() == processes_name:  # Photos.exe
            process.terminate()  # 发送终止信号
            process.wait()  # 等待进程终止


def switch_to_windows(name_like):
    time.sleep(1)  # SET_FOCUS应该等待一秒，不然容易出现问题——No error message is available——最好别动，不着急那一两秒
    windows = _get_running_windows()
    temp = []
    for hwnd, title in windows:
        temp.append(title)
    my_logger.info(f"{get_language('找到程序窗口')} : {temp}")
    for hwnd, title in windows:
        if name_like in title:  # 模糊搜索，其实也可以精准搜索，只要字足够多
            my_logger.info(f"{get_language('切换到程序窗口')} : {title}")  # 多了一个大括号。。
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 原设置
            win32gui.SetForegroundWindow(hwnd)  # 执行操作
            # TODO 尝试使用新方法，这个可能遇到系统权限限制
            # shell = win32com.client.Dispatch("WScript.Shell")
            # shell.SendKeys('%')  # 按下Alt键
            # win32gui.SetForegroundWindow(hwnd)  # 执行操作
            time.sleep(1)  # 给点延迟，防止下一步时程序没有反应过来
            return False  # 正常返回False，终止循环
    return True


def switch_to_windows_full(name_like):
    windows = _get_running_windows()
    for hwnd, title in windows:
        if name_like in title:  # 模糊搜索
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # 最大化
            win32gui.SetForegroundWindow(hwnd)  # 执行操作
            return False  # 正常返回False，终止循环
    return True


def open_web(target_url):  # 以默认方式打开浏览器
    webbrowser.open(target_url)


def open_chrome(target_url):  # 打开Chrome浏览器
    from Class_4_Fun import _open_chrome
    _open_chrome(target_url)


def open_downloaded(target_exe):  # 下载安装程序
    downloads_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Downloads')
    if os.path.exists(downloads_path):  # 检查下载文件夹是否存在
        for item in os.listdir(downloads_path):  # 遍历下载文件夹中的所有项
            # if target_exe in item:  # ChromeSetup.exe
            if target_exe == item:  # ChromeSetup.exe
                target_path = os.path.join(downloads_path, item)
                os.startfile(target_path)  # 这个更具通用性 Nice
                break


def open_installed(target_exe):  # 快速打开程序，自带SetFocus
    programs = get_all_programs_from_start_menu()
    for program in programs:
        if target_exe in program:
            os.startfile(program)
            break


def open_system(target_exe):
    if target_exe == 'UserAccountControlSettings':
        subprocess.Popen(r'C:\Windows\System32\UserAccountControlSettings.exe')  # 可以先写个检测程序检测这些路径是否存在
        time.sleep(0.2)  # 时间不确定，等待实战测试
        switch_to_windows(get_language('用户帐户控制设置'))  # 切换焦点，稳妥起见
    # 默认在下载位置，所以遍历下载文件查找
    elif target_exe == 'ProgramAndFunction':
        subprocess.call('appwiz.cpl', shell=True)  # 这个是打开卸载，比系统自带的好用
        time.sleep(0.2)
        switch_to_windows(get_language('程序和功能'))  # 已验证


def check_exe_exists(target):  # 检查文件是否存在
    exist_exe_list = _get_installed_programs()
    if target in exist_exe_list:
        # TODO 未测试
        print(f'{target} Exists!')


def finish():
    my_logger.info(f"{get_language('程序已结束')}")
    kill_processes('Photos.exe')  # 推荐使用精准关闭


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
        print(f"{get_language('转移文件夹时发生错误')} {e}")
