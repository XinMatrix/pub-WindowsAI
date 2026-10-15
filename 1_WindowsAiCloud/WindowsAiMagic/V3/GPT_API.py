import os
import re

import openai

# 僵尸引用：看来还是要引用的，可以预防很多错误
import matplotlib.pyplot as plt  # 绘图
import plotly.express as px  # 绘图
import plotly.graph_objects as go  # 绘图
import pandas as pd  # 数据处理
import subprocess  # 运行命令
import numpy as np  # 数据处理

gpt_api = "YOUR_OPENAI_API_KEY"


def create_python_file(is_code, format_input, file_name):
    folder_path = os.path.join(os.path.join(os.path.expanduser("~"), "Desktop"), 'MyWindowsAi', 'Statics')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    if is_code:  # 保留源代码
        with open(file_path, 'w') as f:
            f.write(format_input)
    else:  # 将 temp_raw_output 注释内容写入文件
        with open(file_path, 'w') as f:
            f.write(r"'''")
            f.write('\n')
            f.write(format_input)
            f.write('\n')
            f.write(r"'''")
    return file_path


def format_code(text, insert_text):
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)  # 使用正则表达式匹配```python包裹的内容
    max_length = 0  # 初始化最大长度和最大内容
    largest_block = ""
    for block in code_blocks:  # 遍历所有匹配的代码块，查找字数最多的区域
        block_length = len(block)
        if block_length > max_length:
            max_length = block_length
            largest_block = block
    if largest_block:  # 如果找到了最大代码块，则在其第一行插入文本
        lines = largest_block.splitlines()
        lines.insert(0, insert_text)  # 在第一行插入指定文本
        largest_block = '\n'.join(lines)
    return largest_block


def format_text(raw_output):
    while '*' in raw_output:  # 去除所有*
        raw_output = raw_output.replace('*', '')
    while '`' in raw_output:  # 去除所有*
        raw_output = raw_output.replace('`', '')
    return raw_output


def get_openai_response(temp_input_text):
    openai.api_key = gpt_api
    openai.base_url = "https://api.gpt.ge/v1/"
    openai.default_headers = {"x-foo": "true"}
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Windows系统\n"
                           "优先使用代码运行而非回复信息\n"
                           "如果是Python相关的问题，请直接生成Python代码，无需任何其他说明，注意写成一个完整函数！\n"
                           "如果要绘制图表，请使用Plotly库，使用外引线表示\n"
                           "如果可以使用CMD运行请直接在代码中调用CMD\n"
                           "如果有数字显示请确保数字足够直观，不易混淆\n"
                           "如果运行代码有结果请同时保存到本地txt文件，并打开\n"
                           "如果是一般非编程类问题，请直接回复相关内容\n"
            },
            {
                "role": "user",
                "content": temp_input_text
            },
        ],
        temperature=0.3,  # 温度越低越稳定，推荐0.3，默认为1
        n=1,
    )
    return completion.choices[0].message.content


def exec_code(temp_text):
    file_name = f"WindowsAiMagic {re.sub(r'[\\/*?:"<>|]', " ", temp_text)[:100]}.py"
    raw_output = get_openai_response(temp_text)  # 源输出
    if '```python' in raw_output:  # 如果源输出中有代码块，则只保留最大代码块
        formatted_output = format_code(raw_output, '# ' + file_name[:-3])
        is_code = True
    else:
        formatted_output = format_text(raw_output)
        is_code = False
    # print('-------------------------------Raw output--------------------------------------')
    # print(raw_output)
    print('------------------------------Formatted output---------------------------------')
    print(formatted_output)
    print('-------------------------------------------------------------------------------')
    exec(formatted_output)
    # file_path = create_python_file(is_code, formatted_output, file_name)
    # print(f"内容已备份: {file_path}")
    # if is_code:  # 如果是源代码，则执行代码
    #     try:
    #         exec(formatted_output)
    #     except SyntaxError as e:
    #         print(f"代码有语法错误，请检查代码 {e}")
    # TODO 这里应该重新尝试并提示用户
    # Traceback
    # else:  # 如果是文本，则打印输出
    #     os.startfile(file_path)  # 打开文件


if __name__ == "__main__":
    # input_text = "怎么才能每天都开开心心"  # 一般问题已测试
    # input_text = r"帮我给每个文件名前加上序号 C:\Users\USER\Desktop\Images"  # 文件重命名问题已测试
    # input_text = r'输出文件夹大小并绘制饼图，只绘制大于100MB文件夹，C:\Users\USER\Desktop'  # 存储查询问题已测试
    # input_text = r"转化图片格式为webp C:\Users\USER\Pictures\自拍 - 副本.jpg"  # 图像格式转化问题已测试
    # input_text = r"图片裁剪成正方形 C:\Users\USER\Pictures\自拍 - 副本.jpg"  # 图像裁剪问题已测试
    # input_text = r"查看回环地址端口占用情况"  # 系统信息问题已测试
    input_text = r"查看本地ip地址"  # 系统信息问题已测试
    # input_text = input("请输入问题：")
    exec_code(input_text)
    # TODO 现在的问题是它怎么结合我的OCR及函数库处理

# pyinstaller --onefile GPT_API.py
# 打包好慢，要十分钟左右
