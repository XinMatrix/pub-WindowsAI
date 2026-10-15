import numpy as np
import winsound
from PIL import ImageGrab, Image
from paddleocr import PaddleOCR
# from config import my_logger

# 初始化 OCR
ocr = PaddleOCR(lang='ch')

def grab_screen():
    return ImageGrab.grab()

def start_ocr_from_image(image, ratio=2, min_confidence=0.1):
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)
    temp_result = ocr.ocr(image_np)

    text_info_list = []

    if not temp_result:
        return text_info_list

    for line in temp_result[0]:
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]
        text = line[1][0]
        confidence = line[1][1]
        if confidence > min_confidence:
            text_info_list.append({"text": text, "confidence": confidence, "position": box})

    return text_info_list

if __name__ == "__main__":

    screenshot = grab_screen()
    result = start_ocr_from_image(screenshot)

    winsound.Beep(700, 300)

    for item in result:
        print(f"文本：{item['text']}，置信度：{item['confidence']:.2f}")
