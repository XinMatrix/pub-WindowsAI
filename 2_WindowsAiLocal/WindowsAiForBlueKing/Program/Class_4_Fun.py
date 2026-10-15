import os
import re
import subprocess
import time
import webbrowser

from PIL import ImageGrab

from OCR import start_ocr_zh, start_ocr_en
from config import get_language, last_img, my_logger

# 预定义所需变量
MapValue = {}


def get_data(key):
    MapValue.clear()  # 清空之前的变量
    with open('user_info.txt', 'r', encoding='utf-8') as file:  # 这个文件需要一起打包给用户
        for line in file:
            line = line.strip()  # 去掉行末的换行符
            if '=' in line and line.split('=')[1]:  # 确保该行包含一个等号且不为空 检查是否有等号，并确保右侧有值
                temp_key, temp_value = line.split('=')
                MapValue[temp_key] = temp_value
    return MapValue.get(key, 'None')


# 每次都会重新从文件读取，就不考虑问题了
user_name = get_data('user_name')
user_email = get_data('user_email')
gitee_user_name = get_data('gitee_user_name')
gitee_user_password = get_data('gitee_user_password')
BKPAAS_APP_ID = get_data('BKPAAS_APP_ID')
# BKPAAS_APP_SECRET = get_data('BKPAAS_APP_SECRET')
BKPAAS_APP_NAME = get_data('BKPAAS_APP_NAME')


def _run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def start_inner_fun(target_fun):
    if target_fun == 'GET_WIFI_PASSWORD':
        from Class_1_System import switch_to_windows_full
        names, passwords = _get_wifi_status()
        tmp_list = []
        for name, password in zip(names, passwords):
            tmp_list.append(f'{name} : {password}')
        write_path = os.path.join(os.path.expanduser('~'), 'Desktop\\MyWindowsAi\\Statics')
        with open(f'{write_path}/wifi_result.txt', 'w', encoding='utf-8') as f:
            for item in tmp_list:
                f.write(item + '\n\n')
            f.close()  # 关闭文件
        os.startfile(f'{write_path}/wifi_result.txt')
        time.sleep(1.5)
        switch_to_windows_full('wifi_result.txt')  # 切换焦点
    elif target_fun == 'CHECK_SYSTEM_VISION':
        check = _get_windows_version()
        if not check:
            text = get_language('请升级为 Windows 10/11 家庭版以上版本')
            my_logger.error(text)
            raise ValueError(text)
    elif target_fun == 'CHECK_SYSTEM_GPU':
        check = _is_gpu_available()
        if not check:
            text = get_language('未检测到GPU')
            my_logger.error(text)
            raise ValueError(text)
    elif target_fun == 'START_HYPER_V':
        _start_hyper_v()
    # TODO 再给一个关闭Hyper-V的函数
    elif target_fun == 'CLICK_CENTER':
        from Class_3_Input import _click_center
        _click_center()
    elif target_fun == 'INIT_GIT':
        _init_git()
    elif target_fun == 'BK_REPLACE_TEXT':
        _bk_replace_text()
    elif target_fun == 'BK_INIT_DB':
        _bk_init_db()
    elif target_fun == 'ADD_HOST':
        _add_host()
    else:
        text = f"{get_language('未知函数')} : {target_fun}"
        my_logger.error(text)
        raise ValueError(text)


def _get_wifi_status():  # 获取所有连接过的WIFI的密码
    from Class_1_System import switch_to_windows_full, run_cmd
    output = run_cmd('netsh wlan show profiles')
    wifi_name_list = []
    wifi_password_list = []
    lines = output.strip().split('\n')
    user_profiles = [line.strip().split(' : ')[-1] for line in lines if get_language('所有用户配置文件') in line]
    for profile in user_profiles:
        wifi_name_list.append(profile)
    for item in wifi_name_list:
        output = run_cmd(f'netsh wlan show profile name="{item}" key=clear')
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


def delay(target):  # 小睡一会
    delay_time = float(target)
    time.sleep(delay_time)


def close_windows(target):  # 关闭程序进程，用于卸载预处理
    temp = _run_cmd(f'''wmic process where "name='{target}'" delete''').stdout
    # wmic process get caption,CSName,ProcessID 查看正在运行的进程
    return get_language('删除实例') in temp  # 删除成功就会return True


def once_ocr_zh():
    ImageGrab.grab().save(last_img, format='JPEG')
    return start_ocr_zh(last_img)


def once_ocr_en():
    ImageGrab.grab().save(last_img, format='JPEG')
    return start_ocr_en(last_img)


def _get_windows_version():
    # 执行 WMIC 命令并读取输出
    output = os.popen('wmic os get Caption').read().strip()
    # 判定 Windows 10 和 Windows 11 的不同版本
    if get_language('Windows 11 专业工作站版') in output:
        return True
    elif get_language('Windows 11 专业版') in output:
        return True
    elif get_language('Windows 11 家庭版') in output:
        return False
    elif get_language('Windows 11 企业版') in output:
        return True
    elif get_language('Windows 11 教育版') in output:
        return True
    elif get_language('Windows 10 专业工作站版') in output:
        return True
    elif get_language('Windows 10 专业版') in output:
        return True
    elif get_language('Windows 10 家庭版') in output:
        return False
    elif get_language('Windows 10 企业版') in output:
        return True
    elif get_language('Windows 10 教育版') in output:
        return True
    else:
        return False


def _is_gpu_available():
    geforce_gpu_list = [
        "NVIDIA GeForce RTX 4090",
        "NVIDIA GeForce RTX 4080",
        "NVIDIA GeForce RTX 4070 Ti",
        "NVIDIA GeForce RTX 3090 Ti",
        "NVIDIA GeForce RTX 3090",
        "NVIDIA GeForce RTX 3080 Ti",
        "NVIDIA GeForce RTX 3080",
        "NVIDIA GeForce RTX 3070 Ti",
        "NVIDIA GeForce RTX 3070",
        "NVIDIA GeForce RTX 3060 Ti",
        "NVIDIA GeForce RTX 3060",
        "NVIDIA GeForce GTX 1650 Ti",
        "NVIDIA TITAN RTX",
        "NVIDIA GeForce RTX 2080 Ti",
        "NVIDIA GeForce RTX 2080",
        "NVIDIA GeForce RTX 2070",
        "NVIDIA GeForce RTX 2060",
        "NVIDIA TITAN V",
        "NVIDIA TITAN Xp",
        "NVIDIA TITAN X",
        "NVIDIA GeForce GTX 1080 Ti",
        "NVIDIA GeForce GTX 1080",
        "NVIDIA GeForce GTX 1070 Ti",
        "NVIDIA GeForce GTX 1070",
        "NVIDIA GeForce GTX 1060",
        "NVIDIA GeForce GTX 1050",
        "NVIDIA GeForce GTX TITAN X",
        "NVIDIA GeForce GTX TITAN Z",
        "NVIDIA GeForce GTX TITAN Black",
        "NVIDIA GeForce GTX TITAN",
        "NVIDIA GeForce GTX 980 Ti",
        "NVIDIA GeForce GTX 980",
        "NVIDIA GeForce GTX 970",
        "NVIDIA GeForce GTX 960",
        "NVIDIA GeForce GTX 950",
        "NVIDIA GeForce GTX 780 Ti",
        "NVIDIA GeForce GTX 780",
        "NVIDIA GeForce GTX 770",
        "NVIDIA GeForce GTX 760",
        "NVIDIA GeForce GTX 750 Ti",
        "NVIDIA GeForce GTX 750",
        "NVIDIA GeForce GTX 690",
        "NVIDIA GeForce GTX 680",
        "NVIDIA GeForce GTX 670",
        "NVIDIA GeForce GTX 660 Ti",
        "NVIDIA GeForce GTX 660",
        "NVIDIA GeForce GTX 650 Ti BOOST",
        "NVIDIA GeForce GTX 650 Ti",
        "NVIDIA GeForce GTX 650",
        "NVIDIA GeForce GTX 560 Ti",
        "NVIDIA GeForce GTX 550 Ti",
        "NVIDIA GeForce GTX 460",
        "NVIDIA GeForce GTS 450",
        "NVIDIA GeForce GT 740",
        "NVIDIA GeForce GT 730",
        "NVIDIA GeForce GT 730 DDR3 128位",
        "NVIDIA GeForce GT 720",
        "NVIDIA GeForce GT 705",
        "NVIDIA GeForce GT 640 (GDDR5)",
        "NVIDIA GeForce GT 640 GDDR3",
        "NVIDIA GeForce GT 630",
        "NVIDIA GeForce GT 620",
        "NVIDIA GeForce GT 610",
        "NVIDIA GeForce GT 520",
        "NVIDIA GeForce GT 440"
    ]

    geforce_laptop_gpu_list = [
        "NVIDIA GeForce RTX 4090 Laptop GPU",
        "NVIDIA GeForce RTX 4080 Laptop GPU",
        "NVIDIA GeForce RTX 4070 Laptop GPU",
        "NVIDIA GeForce RTX 4060 Laptop GPU",
        "NVIDIA GeForce RTX 4050 Laptop GPU",
        "NVIDIA GeForce RTX 3080 Ti Laptop GPU",
        "NVIDIA GeForce RTX 3080 Laptop GPU",
        "NVIDIA GeForce RTX 3070 Ti Laptop GPU",
        "NVIDIA GeForce RTX 3070 Laptop GPU",
        "NVIDIA GeForce RTX 3060 Ti Laptop GPU",
        "NVIDIA GeForce RTX 3060 Laptop GPU",
        "NVIDIA GeForce RTX 3050 Ti Laptop GPU",
        "NVIDIA GeForce RTX 3050 Laptop GPU",
        "NVIDIA GeForce RTX 2080 Laptop GPU",
        "NVIDIA GeForce RTX 2070 Laptop GPU",
        "NVIDIA GeForce RTX 2060 Laptop GPU",
        "NVIDIA GeForce GTX 1080 Laptop GPU",
        "NVIDIA GeForce GTX 1070 Laptop GPU",
        "NVIDIA GeForce GTX 1060 Laptop GPU",
        "NVIDIA GeForce GTX 980 Laptop GPU",
        "NVIDIA GeForce GTX 980M Laptop GPU",
        "NVIDIA GeForce GTX 970M Laptop GPU",
        "NVIDIA GeForce GTX 965M Laptop GPU",
        "NVIDIA GeForce GTX 960M Laptop GPU",
        "NVIDIA GeForce GTX 950M Laptop GPU",
        "NVIDIA GeForce 940M Laptop GPU",
        "NVIDIA GeForce 930M Laptop GPU",
        "NVIDIA GeForce 920M Laptop GPU",
        "NVIDIA GeForce 910M Laptop GPU",
        "NVIDIA GeForce GTX 880M Laptop GPU",
        "NVIDIA GeForce GTX 870M Laptop GPU",
        "NVIDIA GeForce GTX 860M Laptop GPU",
        "NVIDIA GeForce GTX 850M Laptop GPU",
        "NVIDIA GeForce 840M Laptop GPU",
        "NVIDIA GeForce 830M Laptop GPU",
        "NVIDIA GeForce 820M Laptop GPU",
        "NVIDIA GeForce 800M Laptop GPU",
        "NVIDIA GeForce GTX 780M Laptop GPU",
        "NVIDIA GeForce GTX 770M Laptop GPU",
        "NVIDIA GeForce GTX 765M Laptop GPU",
        "NVIDIA GeForce GTX 760M Laptop GPU",
        "NVIDIA GeForce GTX 680MX Laptop GPU",
        "NVIDIA GeForce GTX 680M Laptop GPU",
        "NVIDIA GeForce GTX 675MX Laptop GPU",
        "NVIDIA GeForce GTX 675M Laptop GPU",
        "NVIDIA GeForce GTX 670MX Laptop GPU",
        "NVIDIA GeForce GTX 670M Laptop GPU",
        "NVIDIA GeForce GTX 660M Laptop GPU",
        "NVIDIA GeForce GT 755M Laptop GPU",
        "NVIDIA GeForce GT 750M Laptop GPU",
        "NVIDIA GeForce GT 650M Laptop GPU",
        "NVIDIA GeForce GT 745M Laptop GPU",
        "NVIDIA GeForce GT 645M Laptop GPU",
        "NVIDIA GeForce GT 740M Laptop GPU",
        "NVIDIA GeForce GT 730M Laptop GPU",
        "NVIDIA GeForce GT 640M Laptop GPU",
        "NVIDIA GeForce GT 640M LE Laptop GPU",
        "NVIDIA GeForce GT 735M Laptop GPU",
        "NVIDIA GeForce GT 635M Laptop GPU",
        "NVIDIA GeForce GT 730M DDR3 128-bit Laptop GPU",
        "NVIDIA GeForce GT 730M DDR3 64-bit Laptop GPU"
    ]

    try:
        # 获取 GPU 信息
        result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], capture_output=True,
                                text=True)
        info = result.stdout
    except FileNotFoundError:
        return "wmic command not found. Make sure you are using a compatible Windows version."
    # 解析 GPU 信息
    lines = info.strip().split('\n')
    if len(lines) < 2:
        return False
    gpu_names = [line.strip() for line in lines[1:] if line.strip()]
    # 检查是否支持 GPU
    return any(gpu_name in geforce_gpu_list or gpu_name in geforce_laptop_gpu_list for gpu_name in gpu_names)


def _start_hyper_v(max_retries=10):
    powershell_command = """
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
    """
    attempt = 0
    while attempt < max_retries:
        try:
            result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True,
                                    check=True)
            my_logger.info(f"Hyper-V 已成功启用，输出日志 {result.stdout}")
            return  # 成功后退出函数
        except subprocess.CalledProcessError as e:
            attempt += 1
            my_logger.error(f"启用 Hyper-V 时出现错误: {e.stderr}")
            if attempt < max_retries:  # 如果不是最后一次尝试
                my_logger.info(f"重试 {attempt}/{max_retries}...")
            else:
                my_logger.error("已达到最大重试次数，启用 Hyper-V 失败")


def _detect_language_status(text_list):
    """
    对字符串列表中的每个字符串进行语言检测，并输出统一的状态。

    :param text_list: 字符串列表
    :return: 统一的语言状态，'ZH'（中文）、'EN'（英文）、'MIX'（混合）、'UNKNOWN'（未知）
    """

    def is_chinese(char):
        """判断一个字符是否是中文字符"""
        return '\u4e00' <= char <= '\u9fff'

    def is_english(char):
        """判断一个字符是否是英文字符"""
        return 'a' <= char.lower() <= 'z'

    def detect_language(text):
        """
        检测字符串是中文还是英文。

        :param text: 输入的字符串
        :return: 返回 'Chinese' 或 'English' 或 'Mixed'（混合）
        """
        has_chinese = any(is_chinese(char) for char in text)
        has_english = any(is_english(char) for char in text)

        if has_chinese and has_english:
            return 'Mixed'
        elif has_chinese:
            return 'Chinese'
        elif has_english:
            return 'English'
        else:
            return 'Unknown'

    # 检测每个字符串的语言
    statuses = {detect_language(text) for text in text_list}
    if 'Mixed' in statuses:
        return 'MIX'
    elif 'Chinese' in statuses:
        return 'ZH'
    elif 'English' in statuses:
        return 'EN'
    else:
        return 'UNKNOWN'


def _add_system_path(target):
    # PowerShell 命令更新环境变量
    powershell_command = f"""
       $existingPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
       if (-not $existingPath.Contains("{target}")) {{
           $newPath = "$existingPath;{target}"
           [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
           Write-Output "PATH 环境变量已更新"
       }} else {{
           Write-Output "路径已在 PATH 环境变量中"
       }}
       """
    try:  # 使用 PowerShell 执行命令
        result = subprocess.run(['powershell', '-Command', powershell_command],
                                capture_output=True, text=True, check=True)
        my_logger.info(f"环境变量已更新，输出日志 {result.stdout}")
    except subprocess.CalledProcessError as e:
        my_logger.error(f"更新环境变量时出现错误: {e.stderr}")
        raise SystemExit(f"更新环境变量时出现错误: {e.stderr}")


def _open_chrome(target_url):
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(target_url)


# def _init_git():  # 定制函数，不需要参数
#     # 获取用户桌面路径
#     work_dir = os.path.join(os.path.expanduser("~"), "Desktop", "MyWindowsAi", "Projects", "BlueKingProject")
#
#     # 定义 Git 命令
#     commands = [
#         f'git config --global core.autocrlf true',  # 设置为自动转换换行符
#         f'git config --global user.name "{user_name}"',  # YOUR_NAME
#         f'git config --global user.email "{user_email}"',  # YOUR_EMAIL
#         'git init',
#         'git add .',
#         'git commit -m "WindowsAi First Commit"',
#         # 麻中麻，没有删除就的git仓库，原来这里还有，藏得很深
#         # f'git remote add origin https://gitee.com/{gitee_user_name}/windows-ai-blue-king-project.git',
#         f'git remote add origin https://gitee.com/{gitee_user_name}/blue-king-project.git',
#         'git push -u origin master'
#     ]
#
#     # 执行命令
#     for command in commands:
#         my_logger.info(f"执行命令: {command}")
#         process = subprocess.Popen(command, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         if command == 'git push -u origin master':  # 防止最后一步阻塞线程
#             return  # 成功后退出函数，同时避免阻塞线程
#         output, error = process.communicate()
#
#         # 尝试不同的编码格式
#         try:
#             if output:
#                 output_decoded = output.decode('utf-8')  # 尝试UTF-8编码
#                 my_logger.info(f"输出日志: {output_decoded}")
#         except UnicodeDecodeError:
#             try:
#                 output_decoded = output.decode('gbk')  # 尝试GBK编码
#                 my_logger.info(f"输出日志: {output_decoded}")
#             except UnicodeDecodeError:
#                 my_logger.error("无法解码输出日志")
#
#         try:
#             if error:
#                 error_decoded = error.decode('utf-8')  # 尝试UTF-8编码
#                 my_logger.error(f"错误日志: {error_decoded}")
#                 raise SystemExit(f"错误日志: {error_decoded}")
#         except UnicodeDecodeError:
#             try:
#                 error_decoded = error.decode('gbk')  # 尝试GBK编码
#                 my_logger.error(f"错误日志: {error_decoded}")
#                 raise SystemExit(f"错误日志: {error_decoded}")
#             except UnicodeDecodeError:
#                 my_logger.error("无法解码错误日志")
#                 raise SystemExit(f"错误日志: 无法解码错误日志")


# def _init_git():
#     # 获取用户桌面路径
#     work_dir = os.path.join(os.path.expanduser("~"), "Desktop", "MyWindowsAi", "Projects", "BlueKingProject")
#
#     # 定义 Git 命令
#     commands = f"""
#     git config --global core.autocrlf true &&
#     git config --global user.name "{user_name}" &&
#     git config --global user.email "{user_email}" &&
#     git init &&
#     git add . &&
#     git commit -m "WindowsAi First Commit" &&
#     git remote add origin https://gitee.com/{gitee_user_name}/blue-king-project.git &&
#     git push -u origin master
#     """
#
#     # 执行命令
#     my_logger.info(f"执行命令: {commands}")
#     result = subprocess.run(commands, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#
#     if result.returncode != 0:
#         my_logger.error(f"命令执行失败: {result.stderr}")
#         raise SystemExit(f"命令执行失败: {result.stderr}")
#     else:
#         my_logger.info(f"命令执行成功: {result.stdout}")

def _init_git():
    # 获取用户桌面路径
    work_dir = os.path.join(os.path.expanduser("~"), "Desktop", "MyWindowsAi", "Projects", "BlueKingProject")

    # Git 命令列表
    commands = [
        "git config --global core.autocrlf true",
        "git config --global user.name 'YOUR_NAME'",
        "git config --global user.email 'YOUR_EMAIL'",
        "git init",
        "git add .",
        "git commit -m \"WindowsAi First Commit\"",
        f"git remote add origin https://gitee.com/{gitee_user_name}/blue-king-project.git",
        # "git push https://aYOUR_PHONE:YOUR_EMAIL/aYOUR_PHONE/blue-king-project.git"
        f"git push https://{gitee_user_name}:{gitee_user_password}@gitee.com/{gitee_user_name}/blue-king-project.git"
    ]

    for command in commands:
        my_logger.info(f"正在执行命令: {command}")
        result = subprocess.run(command, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            my_logger.error(f"命令执行失败: {result.stderr}")
            raise SystemExit(f"命令执行失败: {result.stderr}")
        else:
            my_logger.info(f"命令执行成功\n")


def _replace_file_content(old_string, new_string):
    # 获取用户主目录路径，并构建桌面文件夹路径——完全跨平台
    file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'MyWindowsAi', 'Projects', 'BlueKingProject',
                             'manage.py')
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        # 检查是否有需要替换的内容
        if old_string in content:
            # 替换内容
            new_content = content.replace(old_string, new_string)
            # 将替换后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            my_logger.info(f"已成功将 '{old_string}' 替换为 '{new_string}'，并保存至文件 '{file_path}'")
        else:
            my_logger.error(f"文件中未找到 '{old_string}'")
            raise SystemExit(f"文件中未找到 '{old_string}'")
    except FileNotFoundError:
        my_logger.error(f"文件 '{file_path}' 不存在")
        raise SystemExit(f"文件 '{file_path}' 不存在")
    except Exception as e:
        my_logger.error(f"出现错误：{e}")
        raise SystemExit(f"出现错误：{e}")


def _bk_replace_text():  # 替换 ID 与 SECRET
    _replace_file_content('{BKPAAS_APP_ID}', BKPAAS_APP_ID)
    # _replace_file_content('{BKPAAS_APP_SECRET}', BKPAAS_APP_SECRET)# 用户手动填写


def _bk_init_db():  # 初始化数据库
    mysql_command = f'mysql -u root -p000000 -e "CREATE DATABASE `{BKPAAS_APP_ID}` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"'
    try:
        result = subprocess.run(mysql_command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            my_logger.info(f"命令执行成功: {mysql_command}")
            # 输出日志为空——正常，其实本来就没有
        else:
            my_logger.error(f"命令执行失败: {mysql_command}")
            my_logger.error(f"错误日志: {result.stderr}")
    except Exception as e:
        my_logger.error(f"命令执行失败: {e}")
        raise SystemExit(f"执行过程中发生异常: {e}")


def _add_host():
    entry = "127.0.0.1 appdev.ce.bktencent.com"
    hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
    # 检查是否有管理员权限才能修改系统文件
    if not os.access(hosts_file, os.W_OK):
        my_logger.error("没有权限写入 hosts 文件，请以管理员身份运行该脚本")
        raise PermissionError("没有权限写入 hosts 文件，请以管理员身份运行该脚本")
    # 将新条目追加到 hosts 文件末尾
    try:
        with open(hosts_file, 'a') as file:
            file.write(f"\n{entry}\n")
        my_logger.info(f"已成功添加条目 '{entry}' 到 hosts 文件 '{hosts_file}'")
    except Exception as e:
        my_logger.error(f"修改 hosts 文件时出现错误: {e}")
        raise SystemExit(f"修改 hosts 文件时出现错误: {e}")
