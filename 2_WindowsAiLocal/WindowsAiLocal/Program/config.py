import locale
import logging
import os

# 创建logger
log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running.log")
my_logger = logging.getLogger('WindowsAiLogger')  # 还必须得写点东西。。
my_logger.setLevel(logging.INFO)
# 创建formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# 创建FileHandler并设置日志文件路径
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setFormatter(formatter)
# 将FileHandler添加到logger
my_logger.addHandler(file_handler)

last_img = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/last_img.jpg")

# 定于脚本语言
language = 'undefined'  # en/zh

# 获取当前系统的语言设置
system_language, _ = locale.getlocale()
# 转换为小写以避免大小写不一致的影响
system_language_lower = system_language.lower()
# 判断系统语言
if "chinese" in system_language_lower:
    language = 'zh'
    my_logger.info('系统语言为中文')
elif "english" in system_language_lower:
    language = 'en'
    my_logger.info('The system language is English')  # 系统语言为中文
else:
    language = 'unknown'
    # 系统语言暂不支持，请于评论区提交反馈
    text = 'The system language is not supported at the moment. Please submit feedback in the comments section'
    my_logger.error(text)
    raise ValueError(text)


def get_language(input_text):
    if language == 'zh':
        return input_text
    # elif language == 'en':
    else:  # 默认使用英语
        return language_dict[input_text]


# dict的好处是便于使用，但是只能放两种数据，不适用冒号
language_dict = {
    '获取所有WIFI密码': 'Retrieve saved Wi-Fi networks and passwords',
    '关闭用户帐户控制': 'Disable User Account Control',
    '恢复用户帐户控制': 'Enable User Account Control',
    '配置Python入门环境': 'Set up a Python development environment',
    '配置CUDA环境': 'Set up CUDA environment',
    '未知命令': 'Unknown command',
    '执行完成': 'Execution complete',
    '请输入任务编号': 'Enter task number',
    '发 送': 'Send',
    '我是WindowsAi，很高兴见到你': 'I\'m WindowsAi, nice to meet you',
    '目前支持功能如下，输入对应数字即可\n0. 获取历史WIFI及密码\n1. 关闭用户帐户控制\n2. 恢复用户帐户控制\n3. 配置Python入门环境\n4. 配置Hyper-V\n5. 配置CUDA环境': 'Currently supported functions are as follows, enter the corresponding number to proceed\n1. Disable User Account Control\n2. Enable User Account Control\n3. Set up a Python development environment\n4. Set up Hyper-V\n5. Set up CUDA environment',
    '即将执行': 'Starting',
    '抱歉哦，我还没有学会': 'Sorry, I haven\'t learned',
    '用户强行停止程序': 'User force stop program',
    '权限不足，请使用管理员权限运行': 'Permission not allowed, please use administrator permission to run',
    '添加强制停止快捷键': 'Add Stop Hotkey',
    '按任意键退出': 'Press any key to exit',
    '错误': 'Error',
    'WindowsAi识别失败': 'OCR Not Found \"WindowsAi\"',
    '删除压缩包': 'Delete compressed package',
    '匹配操作 按键': 'Match operation KEY',
    '匹配操作 输入': 'Match operation INPUT',
    '匹配操作 热键': 'Match operation HOTKEY',
    '匹配操作 点击文本': 'Match operation CLICK_TEXT',
    '匹配操作 点击区域文本': 'Match operation CLICK_TEXT_AREA',
    '匹配操作 点击精确文本': 'Match operation CLICK_TEXT_ACCURACY',
    '匹配操作 打开浏览器': 'Match operation WEB_BROWSER',
    '匹配操作 打开下载内容': 'Match operation OPEN_DOWNLOADED',
    '匹配操作 打开安装程序': 'Match operation OPEN_INSTALLED',
    '匹配操作 打开系统程序': 'Match operation OPEN_SYSTEM',
    '匹配操作 检查程序是否存在': 'Match operation CHECK_EXE_EXIST',
    '匹配操作 设置焦点': 'Match operation SET_FOCUS',
    '匹配操作 设置焦点并全屏': 'Match operation SET_FOCUS_FULL',
    '匹配操作 执行函数': 'Match operation FUN',
    '匹配操作 睡眠': 'Match operation SLEEP',
    '匹配操作 关闭程序窗口': 'Match operation CLOSE_WINDOWS',
    '匹配操作 下载内容': 'Match operation DOWNLOAD',
    '匹配操作 输入安装地址': 'Match operation INPUT_DOWNLOAD',
    '匹配操作 输入项目地址': 'Match operation INPUT_PROJECT',
    '匹配操作 跳转': 'Match operation GOTO',
    '匹配操作 等待文本出现': 'Match operation WAIT_OCR',
    '匹配操作 等待文本出现并消失': 'Match operation WAIT_OCR_END',
    '匹配操作 特征文本转操作': 'Match operation SELECT_OCR',
    '匹配操作 右键': 'Match operation CLICK_RIGHT',
    '匹配操作 程序结束': 'Match operation FINISH',
    '匹配操作 移动文件': 'Match operation MOVE_FILE',
    '操作未定义': 'Action not found',
    '找到程序窗口': 'Founded program windows',
    '切换到程序窗口': 'Switch to program windows',
    '用户帐户控制设置': 'User Account Control Settings',
    '程序和功能': '',  # TODO 新增
    '程序已结束': 'Program finished!',
    '未知函数': 'Unknown function',
    '所有用户配置文件': '',  # TODO 新增
    '删除实例': '',  # TODO 新增
    # TODO _get_wifi_status 函数需要使用英文版本
    # TODO close_windows 也是
    '系统语言': 'System Language',
    '关闭日志队列监听器': 'Close log queue listener',
    '重启后打开 Hyper-V 管理器 即可创建使用虚拟机': 'Restart and open Hyper-V Manager to create virtual machines',
    '配置Hyper-V': 'Set up Hyper-V',
    'Windows 11 专业工作站版': 'Windows 11 Pro for Workstations',
    'Windows 11 专业版': 'Windows 11 Pro',
    'Windows 11 家庭版 ': 'Windows 11 Home',
    'Windows 11 企业版': 'Windows 11 Enterprise',
    'Windows 11 教育版': 'Windows 11 Education',
    'Windows 10 专业工作站版': 'Windows 10 Pro for Workstations',
    'Windows 10 专业版': 'Windows 10 Pro',
    'Windows 10 家庭版 ': 'Windows 10 Home',
    'Windows 10 企业版': 'Windows 10 Enterprise',
    'Windows 10 教育版': 'Windows 10 Education',
    '请升级为 Windows 10/11 家庭版以上版本': 'Please upgrade to Windows 10/11 Pro or higher editions',
    '未检测到GPU': 'No GPU detected',
    '转移文件夹时发生错误': 'An error occurred while moving the directory',
    '无效的密钥': 'Invalid key',
    '密钥有效': 'Key valid',
    '密钥过期': 'Key expired',
    'WindowsAi产品验证': 'WindowsAi Product Verification',
    '请输入密钥': 'Please enter the key',
    '粘贴': 'Paste',
    '验证': 'Validate',
    '成功': 'Succeed',
    '激活成功，请重启软件': 'Validation succeed, please restart the software',
    '警告': 'Warning',
    '': '',
}
