import os
import yaml

# 读取环境变量
username = os.getenv('USERNAME')

# 构建路径
train_path = f'C:\\Users\\{username}\\PycharmProjects\\WindowsAI\\TrainModel\\Sample_YOLOv8\\images\\train'
val_path = f'C:\\Users\\{username}\\PycharmProjects\\WindowsAI\\TrainModel\\Sample_YOLOv8\\images\\val'
test_path = f'C:\\Users\\{username}\\PycharmProjects\\WindowsAI\\TrainModel\\Sample_YOLOv8\\images\\test'

# 定义类别
categories = ['nose']

# 定义data.yaml文件路径
output_path = '../../../5_Yolov8/TrainModel/Sample_YOLOv8/data_new.yaml'  # 可以替换为你想要保存的路径

# 创建data.yaml文件内容
data = {
    'train': train_path,
    'val': val_path,
    'test': test_path,
    'names': categories
}

# 将内容写入data.yaml文件
with open(output_path, 'w') as file:
    yaml.safe_dump(data, file)

print("data.yaml 文件已创建并写入内容")
