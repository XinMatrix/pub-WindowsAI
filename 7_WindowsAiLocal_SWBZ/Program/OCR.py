import io

import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

# import paddleocr.ppocr.utils.logging as ppocr_logging  # 添加此行

from config import my_logger

# IDEA 已在 paddleocr.ppocr.utils.logging 中将日志等级设置为 ERROR

# ocr = PaddleOCR(use_angle_cls=True, lang="ch")
ocr = PaddleOCR(lang='ch')  # ch/en


# def start_ocr(image_path, ratio=3, min_confidence=0.1):  # 0.75检测不到Hyper-V，尝试0.5，还是不行，试试0.1
def start_ocr(image_path, ratio=2, min_confidence=0.1):  # 0.75检测不到Hyper-V，尝试0.5，还是不行，试试0.1
    # 读取图像文件
    with open(image_path, 'rb') as image_file:
        image = Image.open(io.BytesIO(image_file.read()))

    # 缩放图像
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)

    # 执行OCR识别
    temp_result = ocr.ocr(image_np)  # 如果使用的是不同的OCR库，请修改此行

    text_info_list = []

    text_list = []

    if not temp_result:  # 如果没有识别到内容
        return text_info_list

    for line in temp_result[0]:
        # 根据缩放比例调整位置
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]
        text = line[1][0]
        confidence = line[1][1]
        if confidence > min_confidence:
            text_list.append(text)
            text_info_list.append({"text": text, "confidence": confidence, "position": box})

    my_logger.info(text_list)

    return text_info_list
