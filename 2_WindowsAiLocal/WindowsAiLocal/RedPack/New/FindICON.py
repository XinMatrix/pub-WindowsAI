import cv2
import numpy as np


def find_icon(lst):  # small是我要找的东西 large是截屏
    small = lst[0]
    large = lst[1]
    small = cv2.imread(small)
    large_image = cv2.imread(large)
    result = cv2.matchTemplate(large_image, small, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # 设置匹配阈值
    locations = np.where(result >= threshold)
    if locations[0].size > 0:
        point = locations[1].item(), locations[0].item()
        return point
    else:
        return -1, -1


if __name__ == '__main__':
    lst = ['game.jpg', 'raw.jpg']
    point = find_icon(lst)
    print(point)
