import time

from PIL import ImageGrab, ImageOps, ImageFilter
import cv2
import numpy as np

time.sleep(2)

# 获取屏幕截图
screenshot = ImageGrab.grab()

# 转换为OpenCV的BGR格式
screenshot_cv2 = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 转换为灰度图像
gray = cv2.cvtColor(screenshot_cv2, cv2.COLOR_BGR2GRAY)

# 使用Canny边缘检测
# edges = cv2.Canny(gray, threshold1=50, threshold2=150)  # 低于这个阈值的像素会被认为不是边缘 高于这个阈值的像素会被认为是强边缘像素 50 100
edges = cv2.Canny(gray, threshold1=20, threshold2=60)

# 查找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # <class 'tuple'>

# 绘制轮廓
cv2.drawContours(screenshot_cv2, contours, -1, (0, 255, 0), 2)

# 显示结果
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
cv2.imshow('Contours', screenshot_cv2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 感觉可以按面积分类给大小
# 改下参数
# 我想要的应该是清晰有效的边界
