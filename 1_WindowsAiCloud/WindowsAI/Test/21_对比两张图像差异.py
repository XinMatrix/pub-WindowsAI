# 对比两张图像差异，以百分比呈现
import cv2
import numpy as np


def check_image_difference(old_img, new_img):
    image1 = cv2.imread(old_img)
    image2 = cv2.imread(new_img)
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray_image1, gray_image2)
    different_pixels = np.count_nonzero(diff)
    total_pixels = gray_image1.shape[0] * gray_image1.shape[1]
    return (different_pixels / total_pixels) * 100


if __name__ == '__main__':
    print(check_image_difference(r'C:\Users\USER\Desktop\d1.jpg', r'C:\Users\USER\Desktop\d2.jpg'))
