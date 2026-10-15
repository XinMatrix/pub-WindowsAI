import logging
import os

# 暂时不需要
# if not os.path.exists(os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs")):
#     os.makedirs(os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs"))

# 创建logger
# log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running.log")
log_path = os.path.join("running.log")
my_logger = logging.getLogger('WindowsAiLogger')  # 还必须得写点东西。。
my_logger.setLevel(logging.INFO)
# 创建formatter
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# 创建FileHandler并设置日志文件路径
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setFormatter(formatter)
# 将FileHandler添加到logger
my_logger.addHandler(file_handler)

# 创建StreamHandler以输出到控制台——新增的，之前还可以的，怎么现在得加这些代码才能输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
my_logger.addHandler(console_handler)


def get_language(input_text):
    return input_text
