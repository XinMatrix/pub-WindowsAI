from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import os


def save_font_characters_as_images(temp_font_path, temp_output_directory):
    font = TTFont(temp_font_path)
    if 'cmap' in font:
        cmap = font['cmap'].getBestCmap()
        if cmap is not None:
            if not os.path.exists(temp_output_directory):
                os.makedirs(temp_output_directory)

            # 遍历字体中的每个字符
            for codepoint, glyph_id in cmap.items():
                if 0x4E00 <= codepoint <= 0x9FFF:  # 中文字符范围
                    character = chr(codepoint)
                    # 创建一个新的图像
                    image = Image.new('RGB', (40, 40), color='white')

                    # 使用PIL的ImageDraw和ImageFont来绘制字符
                    font_obj = ImageFont.truetype(temp_font_path, size=40)
                    draw = ImageDraw.Draw(image)
                    draw.text((0, -7), character, fill='black', font=font_obj)

                    # 构建输出文件名，使用中文字符的unicode码点作为文件名
                    output_file = os.path.join(temp_output_directory, f'{character}.png')

                    # 保存图像文件
                    image.save(output_file)
                    try:
                        print(f"Saved character '{character}' as {output_file}")
                    except UnicodeEncodeError:
                        print(f"Saved character (UnicodeEncodeError) as {output_file.encode('utf-8')}")
                else:
                    continue
        else:
            print(f"Font: {temp_font_path} has no valid cmap table")
    else:
        print(f"Font: {temp_font_path} has no cmap table")


# 指定单个字体文件的路径
font_path = r'C:\Users\USER\AppData\Local\Microsoft\FontCache\4\CloudFonts\Microsoft YaHei\46325076421.ttf'  # 微软雅黑

# 指定输出目录的路径
output_directory = 'font_character_images'

# 保存指定字体文件中包含的所有中文字符为图像文件
save_font_characters_as_images(font_path, output_directory)

print(f"The Chinese characters have been saved as images in {output_directory}")
