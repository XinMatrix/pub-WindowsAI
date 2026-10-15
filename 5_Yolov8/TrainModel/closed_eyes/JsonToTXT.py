import json
import tkinter as tk
from tkinter import filedialog

# 标签类别映射
label_map = {
    "open_eyes": 0,
    "close_mouth": 1
}


# 计算多边形的边界框
def get_bbox(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)
    return x_min, y_min, x_max, y_max


# 转换为YOLOv8格式
def convert_to_yolo_format(shape, img_width, img_height):
    label = shape['label']
    points = shape['points']

    # 获取边界框
    x_min, y_min, x_max, y_max = get_bbox(points)

    # 计算边界框的中心点，宽度和高度
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    width = x_max - x_min
    height = y_max - y_min

    # 归一化
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height

    # 获取标签类别
    class_id = label_map[label]

    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


# 打开文件选择对话框
def select_json_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title="选择JSON文件", filetypes=[("JSON Files", "*.json")])
    return file_path


# 主程序
def main():
    # 选择JSON文件
    json_file_path = select_json_file()

    if not json_file_path:
        print("未选择任何文件！")
        return

    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 将所有标记转换为YOLO格式
    yolo_annotations = []
    for shape in data['shapes']:
        yolo_annotation = convert_to_yolo_format(shape, data['imageWidth'], data['imageHeight'])
        yolo_annotations.append(yolo_annotation)

    # 输出转换后的YOLO格式标注
    output_file = json_file_path.replace(".json", ".txt")
    with open(output_file, "w") as f:
        for annotation in yolo_annotations:
            f.write(annotation + "\n")

    print(f"转换完成，结果已保存为 {output_file}")


# 执行主程序
if __name__ == "__main__":
    main()
