import multiprocessing
from ultralytics import YOLO


def train_model(epochs=3):
    multiprocessing.freeze_support()  # Windows需要开启子线程(Jupyter中不需要)
    model = YOLO(r'C:\Users\USER\Desktop\yolov8x.pt')  # 更大的模型效果可能更好
    model.train(data='data.yaml', epochs=epochs, patience=0)  # patience=0
    model.export(format='onnx')


def process_images():
    filename_list = ['images/train/1.jpg']
    temp_model = YOLO('best.onnx', task='detect')
    for filename in filename_list:
        temp_results = temp_model(filename)
        temp_results[0].show()


# 记得删除 increase (133) 这是个gif
# 一轮15分钟

if __name__ == '__main__':
    train_model()
    # process_images()
