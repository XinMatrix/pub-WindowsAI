import pandas as pd
import random
import string
from datetime import datetime, timedelta


def date_to_key(date_str):
    """
    输入一个日期字符串（格式: YYYYMMDD），返回一个20位的密钥。
    """
    # 通过日期字符串生成唯一的数字值
    random.seed(date_str)
    # 生成20位随机字符串
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return key


def generate_all_keys(start_date_str, end_date_str):
    """
    生成从 start_date_str 到 end_date_str 范围内所有日期的密钥，并返回 DataFrame。
    """
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")
    date_generated = []
    keys = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        key = date_to_key(date_str)
        date_generated.append(date_str)
        keys.append(key)
        current_date += timedelta(days=1)

    # 创建 DataFrame
    df = pd.DataFrame({
        'Date': date_generated,
        'Key': keys
    })
    return df


# 日期范围——选用历史时间，提高安全性
start_date = "20030403"
end_date = "20990403"

# 生成密钥并保存到 Excel
df_keys = generate_all_keys(start_date, end_date)
df_keys.to_excel('keys.xlsx', index=True)

print("所有密钥已保存到 'keys.xlsx' 文件中。")
