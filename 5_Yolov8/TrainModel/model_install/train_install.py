import yaml
import multiprocessing
from ultralytics import YOLO


def read_yaml():
    with open('data.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data.get('names', [])


def train_model(epochs=100):
    multiprocessing.freeze_support()  # Windows需要开启子线程(Jupyter中不需要)
    model = YOLO(r'C:\Users\USER\Desktop\yolov8x.pt')  # 更大的模型效果可能更好
    model.train(data='data.yaml', epochs=epochs, patience=0)  # patience=0
    model.export(format='onnx')
    # results = model.val()


def process_images():
    yaml_data = read_yaml()
    # filename_list = ['images/train/1.jpg', 'images/train/2.jpg', 'images/train/3.jpg', 'images/train/4.jpg', 'images/train/5.jpg']
    filename_list = [r'C:\Users\USER\Desktop\1.jpg']  # 0.4471428571428571
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
            print("  Label: ", yaml_data[int(boxes.cls[i].item())])
        temp_results[0].show()

    if total_boxes > 0:
        average_confidence = total_confidence / total_boxes
        print("Average Confidence: ", average_confidence)  # 0.7254545454545455


if __name__ == '__main__':
    # train_model()
    process_images()
