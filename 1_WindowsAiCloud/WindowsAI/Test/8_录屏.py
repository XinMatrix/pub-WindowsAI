# import cv2
# import pyautogui
# import numpy as np
#
# # 获取屏幕分辨率
# width, height = pyautogui.size()
#
# # 设置输出视频的分辨率和帧率
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('log_install_qq.mp4', fourcc, 90, (width, height))
# # 正常视频30帧每秒，如果写60就是二倍速，90是三倍速，15是0.5倍速
#
# while True:
#     img = pyautogui.screenshot()
#     frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     out.write(frame)
#
# # 保存视频文件
# out.release()
# cv2.destroyAllWindows()
# import threading
# import time
#
# if __name__ == '__main__':
#     myScreenRecording = MyScreenRecording()
#     threading.Thread(target=myScreenRecording.startScreenRecording).start()  # 这样才行呀
#     time.sleep(3)
#     myScreenRecording.stopScreenRecording()
