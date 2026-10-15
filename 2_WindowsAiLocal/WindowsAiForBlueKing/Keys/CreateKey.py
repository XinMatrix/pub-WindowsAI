import random
import string
import pandas as pd
from datetime import datetime, timedelta

import pyperclip


def ten_minute_to_key(datetime_str):
    random.seed(datetime_str)
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return key


def key_to_ten_minute(key):
    for datetime_obj in pd.date_range(start="2024-09-01 00:00", end="2024-10-01 23:50", freq='min'):
        if ten_minute_to_key(datetime_obj.strftime("%Y%m%d%H%M")) == key:
            return datetime_obj.strftime("%Y%m%d%H%M")
    return None


def is_ten_minute_key_valid(key, current_datetime_str):
    datetime_str = key_to_ten_minute(key)
    if datetime_str is None:
        return False, "无效的密钥"
    key_datetime = datetime.strptime(datetime_str, "%Y%m%d%H%M")
    current_datetime = datetime.strptime(current_datetime_str, "%Y%m%d%H%M")
    expiration_datetime = key_datetime + timedelta(minutes=10)

    if key_datetime <= current_datetime < expiration_datetime:
        return True, "密钥有效"
    else:
        return False, "密钥无效"


def get_now_time():
    return datetime.now().strftime("%Y%m%d%H%M")


# 生成当前时间的密钥
new_key = ten_minute_to_key(get_now_time())  # 以当前时间生成密钥，如202409061510
print('新密钥:', new_key)
pyperclip.copy(new_key)

# 验证当前时间的密钥有效性
is_valid = is_ten_minute_key_valid(new_key, get_now_time())
print(is_valid)  # 直接测试当前时间的有效性

print('已粘贴到剪贴板')
input('按任意键退出...')
# pyinstaller --onefile CreateKey.py
