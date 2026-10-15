import json
import re

from PIL import ImageDraw, ImageFont
from PIL import Image
import os


def generate_cover_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        text_content = json.load(file).get('title')

    font_path = r'/7_WindowsAiLocal_SWBZ/Static/alimama_dongfangdakai_regular.ttf'

    # 创建白色背景图片 (1920×1080)
    width, height = 1920, 1080
    background_color = (255, 255, 255)  # 白色
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    main_font = ImageFont.truetype(font_path, 100)  # 主文字大小
    sub_font = ImageFont.truetype(font_path, 40)  # 副文字大小

    # new_text = text_content.split('，')
    # print("text_content=",text_content)
    text_list = re.split(r'[，。！：？,.:?!]', text_content)
    first_two_punctuation = re.findall(r'[，。！：？,.:?!]', text_content)[:2]
    if first_two_punctuation[0] in ['！', '？']:
        text_list[0] = text_list[0] + first_two_punctuation[0]
    if first_two_punctuation[1] in ['！', '？']:
        text_list[1] = text_list[1] + first_two_punctuation[1]

    # print("first_two_punctuation=", first_two_punctuation)
    print(text_list)
    if len(text_list) == 1:
        text_list.append('')
    # else:
    #     raise ValueError("标题错误！")

    # 主文本（居中）
    main_text = text_list[0]
    main_text_width = draw.textlength(main_text, font=main_font)
    main_text_x = (width - main_text_width) / 2
    main_text_y = height / 2 - 260  # 稍微偏上

    second_text = text_list[1]
    second_text_width = draw.textlength(second_text, font=main_font)
    second_text_x = (width - second_text_width) / 2
    second_text_y = height / 2 - 120  # 稍微偏上

    # 副文本（固定内容，较小字号）
    sub_text = "楚门世界指南"
    sub_text_width = draw.textlength(sub_text, font=sub_font)
    sub_text_x = (width - sub_text_width) / 2
    sub_text_y = height / 2 + 300  # 主文本下方

    # 绘制文本（黑色）
    text_color = (0, 0, 0)  # 黑色
    draw.text((main_text_x, main_text_y), main_text, fill=text_color, font=main_font)
    draw.text((second_text_x, second_text_y), second_text, fill=text_color, font=main_font)
    draw.text((sub_text_x, sub_text_y), sub_text, fill=text_color, font=sub_font)

    # 保存图片
    output_file = os.path.join(r'/7_WindowsAiLocal_SWBZ/临时制作', '封面.png')
    image.save(output_file, "PNG")
    print(f"封面已生成: {output_file}")


if __name__ == '__main__':
    generate_cover_from_json(r'/7_WindowsAiLocal_SWBZ/临时制作/middle.json')
