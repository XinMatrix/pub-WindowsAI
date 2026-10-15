# 这个文件主要用于导出、保存、绘制上传图像信息
import os
import shutil
from datetime import datetime

from PIL import ImageDraw
from PIL import Image

from tools.infer.utility import draw_ocr


def _get_now_time():
    now = datetime.now()
    milliseconds = now.microsecond // 1000  # 除以1000将微秒转换为毫秒
    return now.strftime(f"%Y年%m月%d日%H时%M分%S秒{milliseconds:03d}毫秒")


# noinspection PyTypeChecker
def save_and_draw_image(image, result, uuid):
    parent_directory = '../user_outputs'
    new_folder_path = os.path.join(parent_directory, uuid)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        new_folder_path = os.path.join(f'../user_outputs/{uuid}', '1_raw')
        os.makedirs(new_folder_path)
        new_folder_path = os.path.join(f'../user_outputs/{uuid}', '2_simple')
        os.makedirs(new_folder_path)
        new_folder_path = os.path.join(f'../user_outputs/{uuid}', '3_official')
        os.makedirs(new_folder_path)
    image.save(rf'../user_outputs/{uuid}/1_raw/{_get_now_time()}.jpg')  # 保存图像到本地
    result = result[0]
    boxes = [line[0] for line in result]
    texts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    draw = ImageDraw.Draw(image)  # Draw Simple
    for box in boxes:
        box = [tuple(map(int, point)) for point in box]
        draw.polygon(box, outline="red")
    image.save(rf'../user_outputs/{uuid}/2_simple/{_get_now_time()}.jpg')  # 仅绘制
    im_show = draw_ocr(image, boxes, texts, scores)  # Draw Official
    im_show = Image.fromarray(im_show)
    im_show.save(rf'../user_outputs/{uuid}/3_official/{_get_now_time()}.jpg')  # 绘制加输出详细信息


def clear_content():
    # 指定要清空的文件夹路径
    dir_path = '../user_outputs/'
    shutil.rmtree(dir_path)
    os.mkdir(dir_path)
