from ultralytics import YOLO


def process_images(filename_list):
    temp_model = YOLO('../resources/yolov8x.pt', task='detect')  # 使用官方模型
    # temp_model = YOLO('runs/detect/train/weights/best.onnx', task='detect')  # 使用训练好的模型
    total_confidence = 0
    total_boxes = 0
    for filename in filename_list:
        temp_results = temp_model(filename)
        boxes = temp_results[0].boxes
        for i in range(len(boxes.xyxy)):
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            confidence = round(boxes.conf[i].item(), 2)
            total_confidence += confidence
            print("  Box {}: ".format(i + 1))
            print("  Center Point (x, y): ", (center_x.item(), center_y.item()))
            print("  Confidence: ", confidence)
            total_boxes += 1
        temp_results[0].show()  # 打开图片并显示预测结果

    if total_boxes > 0:  # 计算平均置信度
        average_confidence = total_confidence / total_boxes
        print("Average Confidence: ", average_confidence)


if __name__ == '__main__':
    process_images(['../data/images/test/001.jpg'])  # 加载预测图片
