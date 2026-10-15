import io

import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

# import paddleocr.ppocr.utils.logging as ppocr_logging  # 添加此行

from config import language, my_logger

# IDEA 已在 paddleocr.ppocr.utils.logging 中将日志等级设置为 ERROR

# ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# if language == 'zh':
#     lan = 'ch'  # Paddle的怪习惯
# else:
#     lan = 'en'
# ocr = PaddleOCR(lang=lan)
# ocr = PaddleOCR(lang='en')  # 使用en，因为这次是检测英文
ocr = PaddleOCR(lang='en')  # Hyper-V，CUDA


def start_ocr(image_path, ratio=2, min_confidence=0.1):  # 0.75检测不到Hyper-V，尝试0.5，还是不行，试试0.1
    """
    对指定路径的图像文件进行OCR识别。

    :param image_path: 图像文件的路径
    :param ratio: 在进行OCR之前对图像进行缩放的比例（默认为2）
    :param min_confidence: 识别结果的最低置信度阈值（默认为0.75），低于此阈值的结果将被忽略
    :return: 包含识别出的文本、置信度和位置的字典列表
    """
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
            # text_info_list.append({get_language('文本'): text, get_language('置信度'): confidence, get_language('位置'): box})

    my_logger.info(text_list)

    return text_info_list
