import io
import re
import sys
import openai
from config import my_logger

# ----------------------------------------------------------------------------------------
# 僵尸引用：看来还是要引用的，可以预防很多错误
import os
import matplotlib.pyplot as plt  # 绘图
import plotly.express as px  # 绘图
import plotly.graph_objects as go  # 绘图
import plotly.offline as pyo  # 绘图
import pandas as pd  # 数据处理
import subprocess  # 运行命令
import numpy as np  # 数据处理
import psutil  # 系统监控
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageFont  # 图像处理
import chardet  # 编码格式识别
import shutil  # 文件操作
# from sklearn.model_selection import train_test_split  # 训练集测试集划分

# 科学计算
import math  # 数学函数
import random  # 随机数生成
import scipy as sp  # 科学计算库，简写为 sp
import sympy  # 符号运算库
import collections  # 容器数据类型
import itertools  # 迭代器
import functools  # 高阶函数

# 时间处理
# import datetime  # 日期和时间
from datetime import datetime, timedelta
import time  # 时间处理

# 文件处理和解析
import json  # JSON解析
import csv  # CSV文件读写
import h5py  # HDF5 文件格式处理库
import yaml  # 处理YAML格式的库
import pyaml  # 解析 YAML 文件（与 PyYAML 类似）
import zipfile  # 压缩和解压缩 ZIP 文件
import tarfile  # 处理 tar.gz 文件
import glob  # 匹配文件

# 图像处理
import skimage  # 图像处理库
import imageio  # 读取和保存图像

# 办公文档处理
import openpyxl  # 处理 Excel 文件 (.xlsx)
import xlsxwriter  # 创建和写入 Excel 文件
import xlrd  # 读取 .xls 格式的 Excel 文件
import PyPDF2  # 处理 PDF 文件
from pdfminer.layout import LAParams  # 处理 PDF 文本
from fpdf import FPDF  # 创建 PDF 文件
from reportlab.pdfgen import canvas  # 创建复杂 PDF 文件
import docx2txt  # 提取 Word 文件中的文本
import docx2pdf  # 转换 Word 文件为 PDF 文件
import docx  # 处理 Word 文件
from docx import Document
import string  # 字符串处理

# 网络和请求
import requests  # HTTP 请求库
import socket  # 网络通信库
import websockets  # WebSocket 通信库

# Web 开发
from flask import Flask, request  # Web 开发框架
import fastapi  # 构建 Web API
import selenium  # 自动化测试库
import scrapy  # 爬虫框架

# 数据库操作
import pymysql  # 连接 MySQL 数据库
import sqlite3  # 连接 SQLite 数据库
import mysql
import mysql.connector

# SSH 和远程管理
import paramiko  # 连接 SSH 服务器
import fabric  # 远程执行命令

# 数据序列化和反序列化
import marshmallow  # 数据序列化和反序列化库

# 图形和多媒体处理
import cv2  # 计算机视觉库
import pyglet  # 图形渲染库
import pygame  # 图形渲染库
import moviepy.editor as mpe  # 视频处理库
import seaborn as sns  # 数据可视化库
import reportlab  # 创建 PDF 报告

# 语音和文本处理
import pyttsx3  # 语音合成库
import speech_recognition as sr

# Windows 特定库
import win32com  # 访问 Windows COM 对象
import win32com.client as win32
import win32gui  # Windows 窗口管理库
import win32con  # Windows 常量
from win32com import client

# 系统和工具库
import subprocess  # 运行系统命令
from pathlib import Path

# 文档生成和自动化
import sphinx  # 文档生成工具
import tox  # 自动化测试工具
import pytest  # 测试框架
import pypandoc  # 文档格式转换

# 虚拟数据和测试数据生成
import faker  # 生成假数据的库
from faker import Faker

# 其他库
import mimetypes  # 文件类型识别
import moviepy.editor as mp
import ffmpeg  # 为什么报错啊？！——因为没有下载环境——需要测试
from PIL import ImageGrab
# from paddleocr import PaddleOCR  # 图像文字识别库，可以识别中文库
import pyautogui
from pydub import AudioSegment  # 音频处理库

import winreg as reg  # 注册表操作库，配置环境变量
import winreg
import markdown
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.oxml import OxmlElement

from weasyprint import HTML  # md文件转PDF出问题了，说没有一个库gobject-2.0-0——需要安装程序
# 教程 https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
from pptx import Presentation  # ppt转pdf
from pptx.enum.shapes import MSO_SHAPE_TYPE
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
# from googletrans import Translator  # 使用这个会和openai冲突
from bs4 import BeautifulSoup

from matplotlib.animation import FuncAnimation

# 第一次运行时可以安装这些包，用隐藏式安装，给用户说明第一次运行需要配置环境，会比较慢
errorTimes = 0

# ----------------------------------------------------------------------------------------


gpt_api = "YOUR_OPENAI_API_KEY"
gpt_url = "https://api.gpt.ge/v1/"
gpt_model = "gpt-4o-mini"

# messages = [
#     {
#         "role": "system",
#         "content": "Windows系统\n"
#                    "优先使用代码运行而非回复信息\n"
#                    "默认使用UTF-8编码\n"
#                    "如果是Python相关的问题，优先直接生成Python代码，无需任何其他说明，注意写成一个完整函数！\n"
#                    "注意使用完整引用如math.pi，因为我只导入了根引用\n"  # 新增，希望有用
#                    "如果要绘制图表，请使用Plotly库，使用外引线表示\n"
#                    "如果有数字显示请确保数字足够直观，不易混淆\n"
#                    "不要生成本地文件而是直接打开\n"
#                    "如果是一般非编程类问题，请直接回复相关内容\n"
#         # "如果要处理视频请使用ffmpeg库\n"
#     }
# ]
messages = [
    {
        "role": "system",
        "content": "如果是Python相关的问题请优先生成Python代码并写成一个完整函数，无需任何其他说明；"
                   "如果是一般非编程类问题，请直接回复相关内容；"
                   "电脑是Windows系统，默认使用UTF-8编码；"
                   "如果要绘制图表，请使用Plotly库，使用外引线表示；"
    }
]


def reset_messages():
    global messages
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "Windows系统\n"
    #                    "优先使用代码运行而非回复信息\n"
    #                    "默认使用UTF-8编码\n"
    #                    "如果是Python相关的问题，优先直接生成Python代码，无需任何其他说明，注意写成一个完整函数！\n"
    #         # "处理视频优先使用ffmpeg库而非cv2库\n"  # 加这个好像没用
    #                    "注意使用完整引用如math.pi，因为我只导入了根引用\n"  # 新增，希望有用
    #                    "如果要绘制图表，请使用Plotly库，使用外引线表示"
    #                    "如果有数字显示请确保数字足够直观，不易混淆\n"
    #                    "不要生成本地文件而是直接打开\n"
    #                    "如果是一般非编程类问题，请直接回复相关内容\n"
    #         # "如果要处理视频请使用ffmpeg库\n"
    #     }
    # ]
    messages = [
        {
            "role": "system",
            "content": "如果是Python相关的问题请优先生成Python代码并写成一个完整函数，无需任何其他说明；"
                       "如果是一般非编程类问题，请直接回复相关内容；"
                       "电脑是Windows系统，默认使用UTF-8编码；"
                       "如果要绘制图表，请使用Plotly库，使用外引线表示；"
        }
    ]


def calculate_cost(completion, prompt_cost_per_1000=0.00015, completion_cost_per_1000=0.0006):  # 这里是原成本
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    total_tokens = prompt_tokens + completion_tokens
    total_cost = (prompt_tokens / 1000) * prompt_cost_per_1000 + (completion_tokens / 1000) * completion_cost_per_1000
    return total_tokens, total_cost


def process_and_execute(temp_input_text):
    # def create_python_file(is_code, format_input, file_name):
    #     folder_path = os.path.join(os.path.join(os.path.expanduser("~"), "Desktop"), 'MyWindowsAi', 'Statics')
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)
    #     file_path = os.path.join(folder_path, file_name)
    #     if is_code:
    #         my_logger.info(f"源代码已保存: {file_path}")
    #         with open(file_path, 'w') as f:
    #             f.write(format_input)
    #     else:
    #         my_logger.info(f"内容已保存: {file_path}")
    #         with open(file_path, 'w') as f:
    #             f.write(r"'''")
    #             f.write('\n')
    #             f.write(format_input)
    #             f.write('\n')
    #             f.write(r"'''")
    #     return file_path

    def reset_error_times():
        global errorTimes
        errorTimes = 0

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

    def get_openai_response(input_content):
        messages.append({"role": "user", "content": input_content})
        openai.api_key = gpt_api
        openai.base_url = gpt_url
        completion = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=0.3,  # 温度越低越稳定，推荐0.3，默认为1
            n=1,
        )
        total_tokens, total_cost = calculate_cost(completion)
        my_logger.info(f"Token:{total_tokens}\t\t费用:{total_cost:.6f}$")
        return completion.choices[0].message.content

    def exec_code(temp_text):
        formatted_output = re.sub(r'[\\/*?:"<>|]', ' ', temp_text).replace('\n', ' ')[:100]
        file_name = f"WindowsAiMagic {formatted_output}.py"
        raw_output = get_openai_response(temp_text)  # 源输出
        if '```python' in raw_output:  # 如果源输出中有代码块，则只保留最大代码块
            formatted_output = format_code(raw_output, '# ' + file_name[:-3])
            is_code = True
        else:
            formatted_output = format_text(raw_output)
            is_code = False
        my_logger.info("-------------------------------------------------------------------------------")
        # my_logger.info(f"格式化输出:\n{formatted_output}")
        my_logger.info(f"\n{formatted_output}")
        my_logger.info("-------------------------------------------------------------------------------")
        # print("-------------------------------------------------------------------------------")
        # print(f"格式化输出: {formatted_output}")
        # print("-------------------------------------------------------------------------------")
        # file_path = create_python_file(is_code, formatted_output, file_name)
        # my_logger.info(f"内容已备份: {file_path}")
        # print(f"内容已备份: {file_path}")
        if is_code:
            try:
                output_capture = io.StringIO()
                original_stdout = sys.stdout
                try:
                    sys.stdout = output_capture
                    exec(formatted_output)
                    output = output_capture.getvalue()
                    messages.append({"role": "user", "content": '运行结果：\n' + output})
                    my_logger.info(f'结果：\n{output}')
                    # print(f'结果：\n{output}')
                finally:
                    sys.stdout = original_stdout
                if output:
                    return f"完成\n{output}"
                else:
                    return "完成"
            except Exception as e:  # 使用更加通用的错误信息
                my_logger.error(f"执行失败\n{e}")
                # print(f"执行失败\n{e}")
                # if 'No module named' in e.args[0]:
                #     return f"执行失败\n{e}"
                global errorTimes
                retryTimes = 3
                # 记得把报错信息发过去，可以让用户自定义重试次数，默认3，范围0 - 10
                if errorTimes < retryTimes:
                    errorTimes += 1
                    messages.append({"role": "user", "content": f"遇到问题：\n{e}"})
                    my_logger.info(f"重试中： {errorTimes} / {retryTimes}")  # 放在这里就能实时显示了
                    exec_code('')  # 因为message已经添加了，所以这里直接输入空字符串
                else:
                    # process_and_execute(input_text)
                    # exec_code(input_text)
                    my_logger.error(f"执行失败\n{e}")
                    return f"执行失败\n{e}"
            # except SyntaxError as e:
            #     my_logger.error(f"代码有误\n{e}")
            #     return f"代码有误\n{e}"
        else:
            return formatted_output  # WindowsAi Magic直接输出即可

    reset_error_times()

    return exec_code(temp_input_text)


if __name__ == "__main__":
    input_text = input("请输入问题：")
    my_logger.info(process_and_execute(input_text))
    # print(process_and_execute(input_text))
