import cv2
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# img_path = '../img/5.jpg'
# img_path = '../img/sample_1.jpg'
img_path = r'C:\Users\USER\Desktop\test.jpg'

result = ocr.ocr(img_path, cls=True)

# 显示OCR结果并在原图上标记文本位置
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
texts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]

# 打印OCR识别的文本信息
# '''
# for i in range(len(texts)):
# print(f"文本: {texts[i]}，置信度: {scores[i]}，位置: {boxes[i]}")
# print(f"{texts[i]} {boxes[i]}")
# print(f"text: {texts[i]}，pos: {boxes[i][0]}")  # 假定用第一个位置
# print(f"{texts[i]} {boxes[i][0]}")  # 假定用第一个位置
# print(f"{texts[i]}")  # 假定用第一个位置
# if texts[i] == '在文件夹中显示' and scores[i] > 0.9:
#     x1, y1 = boxes[i][0]  # 左上角坐标
#     x2, y2 = boxes[i][2]  # 右下角坐标
#     position = [(x1 + x2) / 2, (y1 + y2) / 2]
#     print(f"文本: {texts[i]}，置信度: {scores[i]}，位置: {position}")
# '''

# 在原图上绘制红色框
draw = ImageDraw.Draw(image)
for box in boxes:
    box = [tuple(map(int, point)) for point in box]  # 将坐标转换为整数类型
    draw.polygon(box, outline="red")  # 绘制红色矩形框

image.show()

# 记录详细信息
# im_show = draw_ocr(image, boxes, texts, scores)
# im_show = Image.fromarray(im_show)
# im_show.save(r'../img/result_3.jpg')
