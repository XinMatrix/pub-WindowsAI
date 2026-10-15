import cv2
import numpy as np


def find_icon(small, large):  # small是我要找的东西 large是截屏
    # 读取大图和小图
    large_image = cv2.imread(large)
    small = cv2.imread(small)
    # 在大图中搜索小图
    result = cv2.matchTemplate(large_image, small, cv2.TM_CCOEFF_NORMED)
    # 设置匹配阈值
    threshold = 0.8
    # 获取匹配结果中的位置信息
    locations = np.where(result >= threshold)
    # 如果找到了小图，则返回 True
    if locations[0].size > 0:
        point = locations[1].item(), locations[0].item()
        return point
    else:
        return -1, -1


# 调用函数并传入路径
print(find_icon("111.jpg", "2.jpg"))
