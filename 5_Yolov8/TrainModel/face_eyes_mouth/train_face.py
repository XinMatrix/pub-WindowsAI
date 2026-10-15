import yaml
import multiprocessing
from ultralytics import YOLO


def train_model(epochs=20):
    multiprocessing.freeze_support()  # Windows需要开启子线程(Jupyter中不需要)
    model = YOLO(r'C:\Users\USER\Desktop\yolov8x.pt')  # 好像必须要有n才能用x
    model.train(data='data.yaml', epochs=epochs, patience=0)  # patience=0
    model.export(format='onnx')
    # results = model.val()


def read_yaml():
    with open('data.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data.get('names', [])


def process_images():
    # yaml_data = read_yaml()
    filename_list = [
        'images/train/003.jpg',
    ]
    temp_model = YOLO('best.onnx', task='detect')
    total_confidence = 0
    total_boxes = 0
    for filename in filename_list:
        temp_results = temp_model(filename)
        boxes = temp_results[0].boxes
        for i in range(len(boxes.xyxy)):
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            print("Box {}: ".format(i + 1))
            print("  Center Point (x, y): ", (center_x.item(), center_y.item()))
            confidence = round(boxes.conf[i].item(), 2)
            print("  Confidence: ", confidence)
            total_confidence += confidence
            total_boxes += 1
            # print("  Label: ", yaml_data[int(boxes.cls[i].item())])
        temp_results[0].show()

    if total_boxes > 0:
        average_confidence = total_confidence / total_boxes
        print("Average Confidence: ", average_confidence)  # 0.749375


if __name__ == '__main__':
    # 在MediaPipe项目中过滤正脸
    # train_model()
    # Labels选点有点问题，因为可能是斜的(会变得非常小)
    process_images()
