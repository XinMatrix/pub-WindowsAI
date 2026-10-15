import cv2
import yaml
import multiprocessing
from ultralytics import YOLO

from TrainModel.lane_markings.draw_line import execute_data


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
    # filename_list = ['images/train/tu (1).jpg', 'images/train/tu (2).jpg', 'images/train/tu (3).jpg']
    filename_list = ['images/train/tu (1).jpg']
    # filename_list = ['temp_frame.jpg']  # 起码还可以检测哈
    # temp_model = YOLO('best_20_new.onnx', task='detect')
    # total_confidence = 0
    # total_boxes = 0
    temp_model = YOLO('best_50.onnx', task='detect')
    output = temp_model(filename)
    for filename in filename_list:  # 这里是循环每个文件
        temp_results = temp_model(filename)
        # 应该存入image而非temp_results[0]
        image = cv2.imread(file)  # 示例数据
        # cv2.imwrite('show_results.jpg', temp_results[0])
        cv2.imwrite('show_results.jpg', image)
        # boxes = temp_results[0].boxes
        # temp_results[0].show()
        # 效果还行，应该是函数的问题，调调参数试试
        # execute_data(boxes, total_boxes, filename)
        # total_boxes += 1

    # if total_boxes > 0:
    #     average_confidence = total_confidence / total_boxes
    #     print("Average Confidence: ", average_confidence)  # 0.749375


if __name__ == '__main__':
    # train_model(50)
    process_images()
