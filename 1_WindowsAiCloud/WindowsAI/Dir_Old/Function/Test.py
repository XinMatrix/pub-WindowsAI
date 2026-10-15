import pyautogui
import requests
from PIL import ImageGrab

ocr_url = 'http://127.0.0.1:5000/ocr_accuracy'
screenshot_save_path = 'last_img.jpg'


def calculate_average_coordinates(coordinates_list):
    if not coordinates_list:  # 检查列表是否为空
        return []  # 如果列表为空，直接返回空列表
    total_x = 0
    total_y = 0
    for coordinates in coordinates_list:
        for coord in coordinates:
            total_x += coord[0]
            total_y += coord[1]
    average_x = total_x / len(coordinates_list * 4)
    average_y = total_y / len(coordinates_list * 4)
    return [round(average_x), round(average_y)]


def find_continuous_sequence(tmp_lst, tmp_sequence):
    full_string = ''.join(tmp_lst)
    start_index = full_string.find(tmp_sequence)
    if start_index != -1:
        end_index = start_index + len(tmp_sequence)
        return start_index, end_index
    else:
        return None


def parse_ocr_results(ocr_results, t):  # 我需要最终返回一个平均pos
    pos_list = []
    for result in ocr_results:
        text = result['text']  # 您的下载任务将会自动开始。如果无法正常下载，手动下载Chrome
        text_word = result['text_word']
        text_word_region = result['text_word_region']
        if t in text:
            tmp = find_continuous_sequence(text_word, t)
            if tmp is not None:  # 说明找到了
                for i in range(tmp[0], tmp[1]):
                    pos_list.append(text_word_region[i])
    print(pos_list)
    return calculate_average_coordinates(pos_list)


# Nice
if __name__ == '__main__':
    # 这个完全可以替换掉OCR，这个是它的融合升级版
    pyautogui.click(624, 310)
    ImageGrab.grab().save(screenshot_save_path, format='JPEG')
    outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
    ave_x, ave_y = parse_ocr_results(outputs, '我不')  # 测试效果还行，就是不要有重复内容，容易出问题
    print(ave_x, ave_y)
    '''
    您的下载任务将会自动开始。如果无法正常下载，手动下载 Chrome
    这是一行奇怪的文本，上完课我就好，要去上课了，哇哇哇，我不太想上课呀
    '''
