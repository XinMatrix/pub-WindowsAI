import cv2

# 读取大图和小图标
large_image = cv2.imread('NewBig.jpg', 0)
template = cv2.imread('NewSmall.jpg', 0)

# 初始化 ORB 检测器
orb = cv2.ORB_create()

# 检测并计算特征点和描述符
keypoints1, descriptors1 = orb.detectAndCompute(template, None)
keypoints2, descriptors2 = orb.detectAndCompute(large_image, None)

# 使用 BFMatcher 进行特征匹配
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)

# 根据匹配距离进行排序
matches = sorted(matches, key=lambda x: x.distance)

print(matches)

# 绘制匹配结果
result = cv2.drawMatches(template, keypoints1, large_image, keypoints2, matches[:10], None, flags=2)
cv2.imwrite('result_orb.png', result)
print("ORB 匹配完成，结果已保存为 'result_orb.png'")
