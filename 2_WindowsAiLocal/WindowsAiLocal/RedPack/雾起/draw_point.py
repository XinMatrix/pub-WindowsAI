from PIL import Image, ImageDraw


def draw_point_on_image(image_path, output_path, point, radius=10, color=(255, 0, 0)):
    """
    在图像上绘制一个点，并保存或显示修改后的图像。

    参数:
    - image_path: 输入图像的路径。
    - output_path: 保存修改后图像的路径。
    - point: 一个(x, y)元组，指定点的位置。
    - radius: 点的半径，默认值为10。
    - color: 点的颜色，默认值为红色 (255, 0, 0)。
    """
    # 打开图像
    img = Image.open(image_path)

    # 创建一个可绘制对象
    draw = ImageDraw.Draw(img)

    # 绘制圆形作为点
    x, y = point
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # 保存修改后的图像
    img.save(output_path)


# 示例使用
image_path = "l1.jpg"
# image_path = "2.png"
output_path = "output_image_2.png"
# point = (137, 120)  # 在 (100, 100) 位置绘制一个点
# point = (137, 140)  # 在 (100, 100) 位置绘制一个点
# point = (281, 501)  # 在 (100, 100) 位置绘制一个点
point = (501, 281)  # 在 (100, 100) 位置绘制一个点
# point = (97, 237)  # 在 (100, 100) 位置绘制一个点
# (281, 501)(501, 281)

draw_point_on_image(image_path, output_path, point)
