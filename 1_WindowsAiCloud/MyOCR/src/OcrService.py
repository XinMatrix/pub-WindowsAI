import io

import numpy as np
from PIL import Image
from flask import Flask, request, jsonify

from src.FileExecutor import save_and_draw_image, clear_content
from src.PaddleOCR_Main import PaddleOCR

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang="ch")


@app.route('/ocr', methods=['POST'])
def ocr_image_raw():
    ratio = 2  # 3——ChromeSetup.exe和打开文件无法识别到就离谱
    user_uuid = request.form['uuid']
    image_file = request.files['image']
    image_stream = image_file.stream
    image = Image.open(io.BytesIO(image_stream.read()))  # 重设大小
    image = image.resize((image.width * ratio, image.height * ratio), Image.LANCZOS)
    image_np = np.array(image)
    result = ocr.ocr(image_np)  # 不需要180度检测
    text_info_list = []
    print('result = ', result)
    if not result:  # 为什么这个不能
        return jsonify(text_info_list)
    for line in result[0]:
        box = [(round(x / ratio), round(y / ratio)) for x, y in line[0]]  # 因为前面乘了，所以现在要除
        text = line[1][0]
        confidence = line[1][1]
        if confidence > 0.75:  # 原来是这里的问题，不准确导致无法识别 0.9改为0.75 因为模糊搜索的原因
            # 应该有两层判定，confidence和包含，不需要取消字符串
            text_info_list.append({"text": text, "confidence": confidence, "position": box})
            print(text, box[0], confidence)
    # logging.info('OcrServiceResults = ', text_info_list)
    save_and_draw_image(image, result, user_uuid)  # 保存并绘制结果
    return jsonify(text_info_list)


@app.route('/', methods=['GET'])
def showHello():
    return 'Hello, This is OcrService!'


if __name__ == '__main__':
    clear_content()  # 清空信息——后期改为剪切到其他地方以确保安全性
    app.run('0.0.0.0')  # 可以访问了 YYDS # http://10.94.135.55:5000  其他电脑连接热点可以使用
