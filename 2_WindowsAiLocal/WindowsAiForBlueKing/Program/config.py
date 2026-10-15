import logging
import os

'''
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
'''


class ReverseFileHandler(logging.FileHandler):
    def emit(self, record):
        # 先获取原有的日志内容
        if os.path.exists(self.baseFilename):
            with open(self.baseFilename, 'r', encoding='utf-8') as f:
                original_content = f.read()
        else:
            original_content = ''

        # 将新的记录格式化后放在内容前面
        new_record = self.format(record) + '\n' + original_content

        # 写回文件
        with open(self.baseFilename, 'w', encoding='utf-8') as f:
            f.write(new_record)


# 使用自定义的ReverseFileHandler
log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running.log")
my_logger = logging.getLogger('WindowsAiLogger')
my_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
reverse_file_handler = ReverseFileHandler(log_path, mode='w')
reverse_file_handler.setFormatter(formatter)

my_logger.addHandler(reverse_file_handler)

last_img = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/last_img.jpg")


def get_language(input_text):
    return input_text
