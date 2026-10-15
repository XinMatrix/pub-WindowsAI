import cv2
import numpy as np


def get_degree(p):
    # 读取图片
    # image = cv2.imread('yolo_detected/mid_0_1.jpg')
    image = cv2.imread(p)
    # 将图像转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用Canny边缘检测算法来检测边缘
    edges = cv2.Canny(gray, 0, 250, apertureSize=3)
    # 使用概率霍夫变换来检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=100)
    # 计算直线的角度并累加
    total_angle = 0
    num_lines = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        total_angle += angle
        num_lines += 1
        # print(f"角度：{angle} 度")
    # 计算平均角度
    average_angle = total_angle / num_lines
    return average_angle
    # print(f"平均角度：{average_angle} 度")
    # 可视化直线
    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # 显示图像和直线
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    print(get_degree('yolo_detected/mid_0_1.jpg'))
    # print(get_degree('yolo_split_color/s_0_0.jpg'))
