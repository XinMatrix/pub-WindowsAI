from datetime import datetime

import cv2
import numpy as np
import pyautogui

__check = False


def startScreenRecording(operation_name):  # 开始时设置为False
    global __check
    __check = False
    width, height = pyautogui.size()
    # 设置输出视频的分辨率和帧率
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 来个时间
    date = datetime.now()
    time = f'{date.year}_{date.month}_{date.day}'
    out = cv2.VideoWriter(f'WAL_{time}_{operation_name}.mp4', fourcc, 90, (width, height))
    # out = cv2.VideoWriter(f'Video_Install_{exe_name}.mp4', fourcc, 90, (width, height))
    # out = cv2.VideoWriter('log_install_qq.mp4', fourcc, 90, (width, height))
    # 正常视频30帧每秒，如果写60就是二倍速，90是三倍速，15是0.5倍速
    while True:
        if __check:
            break
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)
    # 保存视频文件
    out.release()
    cv2.destroyAllWindows()


def stopScreenRecording():  # 结束时设置为True
    global __check
    __check = True
