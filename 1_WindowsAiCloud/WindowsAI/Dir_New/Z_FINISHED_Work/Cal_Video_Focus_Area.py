import cv2
import numpy as np
import os

from PIL import Image, ImageDraw
from moviepy.video.io.VideoFileClip import VideoFileClip


def draw_points_on_image(image_path, points, output_path=None):
    """
    在图像上绘制点

    :param image_path: 输入图像的路径
    :param points: 要绘制的点的列表，格式为 [(x1, y1), (x2, y2), ...]
    :param output_path: 输出图像的路径。如果未指定，则显示图像而不保存
    """
    # 打开图像
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 绘制点
    for point in points:
        x, y = point
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='red', outline='red')  # 在每个点上画一个小圆点

    # 显示或保存图像
    if output_path:
        image.save(output_path)
        print(f"图像已保存到 {output_path}")
    else:
        image.show()


def trim_video(input_path, output_path, start_time=1, end_time=None):
    """
    Trim a video from start_time to end_time and save it to output_path.

    Parameters:
    - input_path (str): Path to the input video file.
    - output_path (str): Path to save the trimmed video file.
    - start_time (float): Start time in seconds (default is 1).
    - end_time (float): End time in seconds (default is None, meaning end of video).
    """
    clip = VideoFileClip(input_path)
    if end_time is None:
        end_time = clip.duration - 1
    trimmed_clip = clip.subclip(start_time, end_time)
    trimmed_clip.write_videofile(output_path)
    clip.close()


def extract_frames(tmp_video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(tmp_video_path)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    cap.release()
    return frame_count


def read_images(image_folder, frame_count):
    images = []
    for i in range(frame_count):
        img = cv2.imread(os.path.join(image_folder, f'frame_{i:04d}.png'), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images.append(img)
    return images


def compute_variance(images):
    image_stack = np.stack(images, axis=-1)
    variance_image = np.var(image_stack, axis=-1)
    return variance_image


def detect_significant_changes(variance_image, threshold):
    _, binary_variance = cv2.threshold(variance_image, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_variance.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_bounding_boxes(contours):
    tmp_bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        tmp_bounding_boxes.append((x, y, w, h))
    return tmp_bounding_boxes


def main(tmp_video_path, threshold=400):  # 30点更多，50,80,100正常，200,300只剩一个点了，400就很完美了
    output_folder = 'Sample'
    frame_count = extract_frames(tmp_video_path, output_folder)
    images = read_images(output_folder, frame_count)
    variance_image = compute_variance(images)
    contours = detect_significant_changes(variance_image, threshold)
    tmp_bounding_boxes = get_bounding_boxes(contours)

    # 点集测试
    # point_list = []
    # for item in tmp_bounding_boxes:
    #     x = item[0]
    #     y = item[1]
    #     point_list.append((x, y))
    # draw_points_on_image(r'C:\Users\USER\PycharmProjects\WindowsAI\Dir_New\Work\Sample\frame_0000.png', point_list, 'image_with_points.jpg')

    # 计算所有边界框的整体范围
    if len(tmp_bounding_boxes) > 0:
        min_x = min([bbox[0] for bbox in tmp_bounding_boxes])
        min_y = min([bbox[1] for bbox in tmp_bounding_boxes])
        max_x = max([bbox[0] + bbox[2] for bbox in tmp_bounding_boxes])
        max_y = max([bbox[1] + bbox[3] for bbox in tmp_bounding_boxes])

        # 计算平均矩形区域的四个顶点坐标
        avg_top_left = (min_x, min_y)
        avg_top_right = (max_x, min_y)
        avg_bottom_left = (min_x, max_y)
        avg_bottom_right = (max_x, max_y)

        # 绘制平均矩形
        display_image = cv2.imread(os.path.join(output_folder, f'frame_0000.png'))
        display_image_with_boxes = draw_bounding_boxes(display_image, [avg_top_left, avg_top_right, avg_bottom_left, avg_bottom_right])

        # 显示结果
        cv2.namedWindow('Average Bounding Box', cv2.WINDOW_NORMAL)
        cv2.imshow('Average Bounding Box', display_image_with_boxes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 返回平均矩形区域的四个顶点坐标
        avg_bounding_box_points = [avg_top_left, avg_top_right, avg_bottom_left, avg_bottom_right]
    else:
        avg_bounding_box_points = []

    return avg_bounding_box_points


def draw_bounding_boxes(image, points):
    cv2.rectangle(image, points[0], points[3], (0, 255, 0), 2)
    return image


# 裁剪视频前后一秒内容
video_path = 'RawVideo.mp4'
output_video_path = 'ClippedVideo.mp4'
trim_video(video_path, output_video_path)  # 裁剪视频很快，但分帧很慢，不过是开发过程所以无所谓
average_bounding = main(output_video_path)
print(average_bounding)
print('Succeed!')
# 现在我拿到内容焦点区域了，应该指定为内容焦点区域里的文字，仅在点击文字时生效，非1即0
# 内容焦点区域——不同的地方
# 控制器焦点区域——相同的地方
# 话说我能不能直接人工标注呀，这样其实简单一些，也很容易，截图记坐标就好了
# 这个代码适合动态小剂量未标记内容的区域鉴定
# IDEA 直接人工标记不就好了
