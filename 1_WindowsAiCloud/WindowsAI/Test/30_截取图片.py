from PIL import Image, ImageDraw


def get_image_average_color(image_path):
    # 打开图片
    img = Image.open(image_path)
    # 将图片转换为RGB模式（如果不是）
    img = img.convert("RGB")
    # 获取图片的像素数据
    pixels = img.load()
    # 初始化颜色累加值
    total_red = 0
    total_green = 0
    total_blue = 0
    total_pixels = img.width * img.height
    # 遍历所有像素，并累加颜色值
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            total_red += r
            total_green += g
            total_blue += b
    # 计算颜色均值
    average_red = total_red // total_pixels
    average_green = total_green // total_pixels
    average_blue = total_blue // total_pixels
    return average_red, average_green, average_blue


def crop_and_save(image_path, center_x, center_y, output_path):
    # 打开图片
    img = Image.open(image_path)
    value = 5  # 5*5
    # 计算截取区域的左上角和右下角坐标
    left = max(0, center_x - value)
    top = max(0, center_y - value)
    right = min(img.width, center_x + value)
    bottom = min(img.height, center_y + value)
    # 截取图片
    cropped_img = img.crop((left, top, right, bottom))
    # 保存截取后的图片
    cropped_img.save(output_path)


# 示例用法
image_path = r'C:\Users\USER\PycharmProjects\WindowsAI\Function\temp_file.jpg'
# image_path = r'C:\Users\USER\Desktop\Snipaste_2024-05-13_22-33-57.jpg'
center_x, center_y = 500, 842
output_path = r'temp_option.jpg'

crop_and_save(image_path, center_x, center_y, output_path)

# 示例用法
image_path = "temp_option.jpg"  # 替换为你的图片路径
# Average Color (R, G, B): (253, 253, 253)
# Average Color (R, G, B): (48, 171, 235)
# 每个通道做差值就好了，偏向于认为255或0是边界，即未勾选状态
average_color = get_image_average_color(image_path)
print("Average Color (R, G, B):", average_color)
