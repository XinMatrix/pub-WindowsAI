import logging
import os

logging.basicConfig(               # ⬅️ 一定放到所有库 import 之前
    level=logging.INFO,
    format=' %(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

# 禁用 ppocr 日志
logging.getLogger('ppocr').disabled = True

# 创建logger
if not os.path.exists(os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/")):
    os.makedirs(os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/"))
log_path = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running.log")
my_logger = logging.getLogger('WindowsAiLogger')  # 还必须得写点东西。。
my_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('%(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setFormatter(formatter)
my_logger.addHandler(file_handler)

last_img = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/last_img.jpg")
