import random
import string

import pandas as pd
from datetime import datetime, timedelta


def date_to_key(date_str):
    """
    生成密钥的函数（与之前的相同）。
    """
    random.seed(date_str)
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return key


def key_to_date(key):
    """
    解析密钥并返回对应的日期字符串。
    """
    # 假设密钥正确且能够反向生成日期
    # 用日期字符串生成密钥
    for date in pd.date_range(start="20030403", end="20990403"):
        if date_to_key(date.strftime("%Y%m%d")) == key:
            return date.strftime("%Y%m%d")
    return None


def is_key_valid(key, current_date_str):
    """
    判断密钥是否正确且在有效期内。
    """
    date_str = key_to_date(key)
    if date_str is None:
        return False, "无效的密钥"

    key_date = datetime.strptime(date_str, "%Y%m%d")
    current_date = datetime.strptime(current_date_str, "%Y%m%d")
    expiration_date = key_date + timedelta(days=2)

    if key_date <= current_date <= expiration_date:
        return True, "密钥有效"
    else:
        return False, "密钥过期"


# 测试函数
test_key = date_to_key("20230827")  # T-2 密钥有效期，即今天，昨天，前天都可以用
print(is_key_valid(test_key, "20230827"))  # 直接测试当日的有效性
