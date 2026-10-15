import cv2
from ultralytics import YOLO  # 假设您使用的是ultralytics库

temp_model = YOLO('best_50.onnx', task='detect')


def load_model_and_execute(filename):
    # 对图像进行YOLO检测
    output = temp_model(filename)
    # 读取原始图像
    image = cv2.imread(filename)
    # 处理每一个检测结果
    for result in output:
        boxes = result.boxes  # 获取边界框
        for box in boxes:
            # 从box中提取信息
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 边界框坐标
            conf = box.conf[0]  # 置信度
            # 绘制检测框
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'{conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    # 保存处理后的图像
    output_filename = 'output_image.jpg'
    cv2.imwrite(output_filename, image)
