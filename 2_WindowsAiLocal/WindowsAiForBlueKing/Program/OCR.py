import io

import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from config import my_logger

ocr_en = PaddleOCR(lang='en')  # Hyper-V，CUDA
ocr_zh = PaddleOCR(lang='ch')


def start_ocr_en(image_path, ratio=2, min_confidence=0.80):  # 0.75检测不到Hyper-V，尝试0.5，还是不行，试试0.1
    # 读取图像文件
    with open(image_path, 'rb') as image_file:
        image = Image.open(io.BytesIO(image_file.read()))
    # 缩放图像
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)
    # 执行OCR识别
    temp_result = ocr_en.ocr(image_np)  # 如果使用的是不同的OCR库，请修改此行
    text_info_list = []
    text_list = []
    if not temp_result:  # 如果没有识别到内容
        return text_info_list
    for line in temp_result[0]:
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]  # 根据缩放比例调整位置
        text = line[1][0]
        confidence = line[1][1]
        if confidence > min_confidence:
            text_list.append(text)
            text_info_list.append({"text": text, "confidence": confidence, "position": box})
            # text_info_list.append({get_language('文本'): text, get_language('置信度'): confidence, get_language('位置'): box})
    my_logger.info(text_list)
    return text_info_list


def start_ocr_zh(image_path, ratio=2, min_confidence=0.80):  # 0.75检测不到Hyper-V，尝试0.5，还是不行，试试0.1
    # 读取图像文件
    with open(image_path, 'rb') as image_file:
        image = Image.open(io.BytesIO(image_file.read()))
    # 缩放图像
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)
    # 执行OCR识别
    temp_result = ocr_zh.ocr(image_np)  # 如果使用的是不同的OCR库，请修改此行
    text_info_list = []
    text_list = []
    if not temp_result:  # 如果没有识别到内容
        return text_info_list
    for line in temp_result[0]:
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]  # 根据缩放比例调整位置
        text = line[1][0]
        confidence = line[1][1]
        if confidence > min_confidence:
            text_list.append(text)
            text_info_list.append({"text": text, "confidence": confidence, "position": box})
    my_logger.info(text_list)
    return text_info_list
