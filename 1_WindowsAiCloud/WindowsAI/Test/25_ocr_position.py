import time

import pyautogui

if __name__ == '__main__':
    # 左上 右上 右下 左下
    lst = [[960.0, 643.0], [1036.0, 643.0], [1036.0, 673.0], [960.0, 673.0]]
    # lst = [[1794.0, 1050.0], [1868.0, 1050.0], [1868.0, 1070.0], [1794.0, 1070.0]]
    # print(lst[0])
    # print(lst[3])
    left_point = lst[0][0], (lst[0][1] + lst[3][1]) / 2
    print(left_point)
    # 960,658
    # for i in lst:
    #     time.sleep(1)
    #     pyautogui.click(i)
