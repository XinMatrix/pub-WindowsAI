import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取较大图像和较小图标（模板）
large_image = cv2.imread('big.jpg')
template = cv2.imread('small.jpg')

# 获取模板的宽高
w, h = template.shape[1], template.shape[0]

# 使用模板匹配
res = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)

# 设置匹配的阈值，值越接近 1 越准确
threshold = 0.8
loc = np.where(res >= threshold)

# 在较大图像中绘制匹配结果的矩形框
for pt in zip(*loc[::-1]):  # loc[::-1] 将 loc 的结果对调顺序
    cv2.rectangle(large_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

# 保存结果到文件
# cv2.imwrite('result.png', large_image)

# 保存并展示结果
plt.imshow(cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB))
plt.title('Detected Icons')
plt.axis('off')  # 隐藏坐标轴
plt.show()
