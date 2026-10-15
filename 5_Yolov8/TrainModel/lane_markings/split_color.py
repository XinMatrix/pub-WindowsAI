# 要不要计算背景RGB，对图像进行颜色分类，导出分类后颜色的斜率
# 读取车道线图像

# 增强算法
import cv2
import numpy as np


def split_color(i, index, file):
    # 读取图片
    image = cv2.imread(file)
    # 将图像转换为RGB颜色空间
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 将图像转换为一维数组
    pixels = image_rgb.reshape((-1, 3))
    # 设定K值为2，即要将图像分成两种颜色
    K = 2
    # 定义终止条件
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    # 使用K均值聚类算法
    _, labels, centers = cv2.kmeans(pixels.astype(np.float32), K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # 将中心颜色转换为整数类型
    centers = np.uint8(centers)
    centers[0] = [0, 0, 0]  # 黑色
    centers[1] = [0, 255, 0]  # 绿色
    # 根据每个像素的标签，将其分配到对应的中心颜色
    segmented_image = centers[labels.flatten()]
    # 将一维数组转换回图像形状
    segmented_image = segmented_image.reshape(image_rgb.shape)
    file_path = f'yolo_split_color/sp_{index}_{i}.jpg'
    cv2.imwrite(file_path, segmented_image)
    return file_path
    # 显示原始图像和分割后的图像
    # cv2.imshow('Original Image', image_rgb)
    # cv2.imshow('Segmented Image', segmented_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
