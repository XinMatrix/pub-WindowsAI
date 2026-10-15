# 因为要获取素材，所以先重试一遍

import cv2
import numpy as np
import matplotlib.pyplot as plt

for i in range(4 - 1):
    # 读取两张图片
    image1 = cv2.imread(fr'C:\Users\USER\Desktop\Img_{i + 1}.jpg')
    image2 = cv2.imread(fr'C:\Users\USER\Desktop\Img_{i + 2}.jpg')

    # 转换为灰度图像
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算两张灰度图像的差异
    diff = cv2.absdiff(gray1, gray2)

    # 设定一个阈值，将差异图像转换为二值图像
    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # 可选步骤：对二值图像进行一些形态学处理，去除噪声等
    kernel = np.ones((3, 3), np.uint8)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    # 显示差异图像
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    plt.title('Image 1')

    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    plt.title('Image 2')

    plt.subplot(1, 3, 3)
    plt.imshow(threshold, cmap='gray')
    plt.title('Difference')

    plt.tight_layout()
    plt.show()
