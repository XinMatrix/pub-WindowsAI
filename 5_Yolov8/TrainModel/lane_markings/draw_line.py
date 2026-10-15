import math

import cv2
import numpy as np
from PIL import Image

from TrainModel.lane_markings.get_linear_k import get_linear_k
from TrainModel.lane_markings.new import get_degree
from TrainModel.lane_markings.split_color import split_color


def calculate_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


# def crop_rectangle(i, index, image_path, point1, point2):
def crop_rectangle(i, index, img, point1, point2):
    # 打开图片
    # img = Image.open(image_path)
    # 计算矩形的左上角和右下角坐标
    x1, y1 = point1
    x2, y2 = point2
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    # 截取矩形区域
    print('CheckPoints 7')
    # 为什么不行呢，我想实时显示而非使用图片一个个生成
    cropped_img = img.crop((left, top, right, bottom))
    print('CheckPoints 8')
    path = f'yolo_detected/mid_{index}_{i}.jpg'
    # 保存截取后的图片
    cropped_img.save(path)
    return path


def test_fun(p):
    # 读取黑白图片
    image = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
    # 阈值化处理
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # 寻找图像中的直线
    lines = cv2.HoughLines(binary_image, 1, np.pi / 180, 200)
    # 输出每条直线的角度或斜率
    if lines is None:
        print('Is None')
        return
    for line in lines:
        rho, theta = line[0]
        angle_in_degrees = np.degrees(theta)
        print("Angle in degrees:", angle_in_degrees)


# def execute_data(boxes, index, file):
def execute_data(boxes, index, image):
    # image = cv2.imread(file)  # 示例数据
    for i in range(len(boxes.xyxy)):  # 这里是循环每个框
        # 每个框的信息 Nice
        print('CheckPoints 3')
        detections = [(boxes.xyxy[i][0], boxes.xyxy[i][1], boxes.xyxy[i][2], boxes.xyxy[i][3])]  # 示例数据
        # 根据两个点截图导出Jpg Nice
        # new_file = crop_rectangle(i, index, file, (boxes.xyxy[i][0].item(), boxes.xyxy[i][1].item()),
        print('CheckPoints 4')
        new_file = crop_rectangle(i, index, image, (boxes.xyxy[i][0].item(), boxes.xyxy[i][1].item()),
                                  (boxes.xyxy[i][2].item(), boxes.xyxy[i][3].item()), )
        # 二分类颜色 Nice
        # file_path = split_color(i, index, new_file) # 感觉不需要这个
        # temp_k = -1 / get_linear_k(file_path)
        # test_fun(file_path)
        # continue
        # temp_k = get_linear_k(file_path)  # TODO 好好看看这个，最可能出问题的地方
        # theta_radians = math.atan(temp_k)
        # theta_degrees = math.degrees(theta_radians)
        print('CheckPoints 5')
        theta_degrees = get_degree(new_file)
        print('CheckPoints 6')
        print('角度 = ', theta_degrees)
        # print('Degree = ', theta_degrees)
        angles = [theta_degrees]  # 示例数据，单位为度，正数表示顺时针旋转，负数表示逆时针旋转
        # angles = [-23]
        # angles = [30]  # 示例数据，单位为度，正数表示顺时针旋转，负数表示逆时针旋转
        # angles = [20]  # 示例数据，单位为度，正数表示顺时针旋转，负数表示逆时针旋转
        # if theta_degrees < 0:
        #     tmp = -abs(90 - theta_degrees)
        # else:
        #     tmp = abs(90 - theta_degrees)
        # angles = [tmp]  # 示例数据，单位为度，正数表示顺时针旋转，负数表示逆时针旋转
        # -60 -> -30
        # 70 -> 20
        # -43 ->
        # if theta_degrees == 0:  # 度数为0时不显示——检查错误
        #     print(theta_degrees)
        #     break
        # 加载图像，假设你已经加载了检测到的图像，存储在image变量中
        # 绘制直线
        for detection, angle in zip(detections, angles):
            x_min, y_min, x_max, y_max = detection
            center_x = int((x_min + x_max) / 2)
            center_y = int((y_min + y_max) / 2)
            # length = min(x_max - x_min, y_max - y_min) + 500  # 直线长度取框的最小边长
            length = min(x_max - x_min, y_max - y_min)  # 直线长度取框的最小边长
            angle_rad = np.deg2rad(angle)  # 将角度转换为弧度

            # 计算直线斜率
            slope = (y_max - y_min) / (x_max - x_min)
            # 根据斜率调整直线长度
            # print('Length 1 = ', length)
            length /= 0.3 * abs(slope)
            # print('Length 2 = ', length)

            # TODO 下一步——增强图像，避免0度

            # 计算直线的端点坐标
            x1 = int(center_x - length * np.cos(angle_rad) / 2)
            y1 = int(center_y + length * np.sin(angle_rad) / 2)
            x2 = int(center_x + length * np.cos(angle_rad) / 2)
            y2 = int(center_y - length * np.sin(angle_rad) / 2)

            # 绘制直线
            # cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 5)  # 在图像上绘制直线，颜色为白色，粗细为2像素
            # cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 5)  # 在图像上绘制直线，颜色为白色，粗细为2像素
            cv2.line(image, (x1, y2), (x2, y1), (0, 0, 255), 5)  # TODO 为什么这个效果反而比较好

    # 保存绘制直线后的图像到本地
    # cv2.imwrite(f'outputs/file_{index}.jpg', image)
    print('Image = ',image)
    cv2.imshow('Name', image)
    # cv2.imwrite(f'temp_file_{index}.jpg', image)
    # cv2.imwrite('show_results.jpg', image)
    # cv2.imshow('temp', image)
    # cv2.imshow('Name', image)
