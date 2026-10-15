import multiprocessing

from ultralytics import YOLO

from utils import reset_running_status


def train_model(epochs=10):  # 默认训练10轮
    multiprocessing.freeze_support()  # Windows需要开启子线程(Jupyter中不需要)
    model = YOLO('../resources/yolov8x.pt')  # 更大的模型效果可能更好，n<s<m<l<x
    model.train(data='../config/train_config.yaml', epochs=epochs)  # 训练模型，data.yaml文件是训练集和验证集的路径
    model.export(format='onnx')  # 将模型导出为onnx格式，可以用onnxruntime等库进行推理，onnx无法指定导出地址
    # 注意，以下方法使用yolov8n.pt时会报错，原因未知
    val_results = model.val()  # Val 验证集评估模型效果
    test_results = model.eval()  # Test 训练集评估模型效果
    print(f'---------------------------\nVal Results: \n{val_results}\n---------------------------')
    print(f'---------------------------\nTest Results: \n{test_results}\n---------------------------')


if __name__ == '__main__':
    reset_running_status()  # 重置运行状态，如创建yaml文件、清除旧的训练结果
    train_model(10)  # 训练模型
