# 读取图像
import math

import cv2
import numpy as np


def calculate_slope(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 将图像转换为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用Canny边缘检测算法检测边缘
    edges = cv2.Canny(gray, 20, 150, apertureSize=3)

    # 使用霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    slopes = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # 计算直线斜率
            slope = (y2 - y1) / (x2 - x1)
            slopes.append(slope)

    return slopes


# 这个函数有很大问题，想办法多写几个测试
def get_linear_k(file):
    # 加载图像
    image = cv2.imread(file)
    # 将图像转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 进行边缘检测
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # edges = cv2.Canny(gray, 20, 150, apertureSize=3)
    para = 50
    edges = cv2.Canny(gray, para, para * 2, apertureSize=5)
    # 进行霍夫变换检测直线
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 200) # 50
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=85)  # threshold阈值低一点更好检测
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    # 60 - 6
    # 85 - 6
    # 100 - 6
    # 150 - 7
    # 200 - 7
    # print(lines)
    # print('lines = ', lines)
    # 使用列表推导式计算为None的元素个数
    # 对每个框内的物体进行检测
    # count_none = sum(1 for item in lines if item is None)
    # print('Count_None = ', count_none)
    # 阈值的多少会直接影响结果
    tmp_k = []
    # 计算直线的斜率
    if lines is None:
        print('None--')
        # return 90  # 为空的情况
        return 0  # 为空的情况
    for line in lines:  # 这里是循环这个框中的直线
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        if x2 == x1:
            return 90
        slope = (y2 - y1) / (x2 - x1)
        return slope
        tmp_k.append(slope)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # cv2.imshow('Detected Lines', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return sum(tmp_k) / 2


if __name__ == '__main__':
    # 能不能直接用四个坐标点画一个叉叉
    # temp_k = get_linear_k(r'C:\Users\USER\Desktop\test.jpg')
    # path = r'C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\lane_markings\yolo_split_color\sp_0_1.jpg'
    path = r'C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\lane_markings\yolo_detected\mid_0_0.jpg'
    # temp_k = get_linear_k(r'C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\lane_markings\yolo_detected\mid_0_0.jpg')  # -14.28
    temp_k = get_linear_k(path)  # -43.6
    # print(calculate_slope(path))
    theta_degrees = math.degrees(math.atan(temp_k))
    print('K = ', temp_k)  # -0.8
    print('Degree = ', theta_degrees)
