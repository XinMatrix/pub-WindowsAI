import os
from PIL import Image
from io import BytesIO

# 设置路径和参数
input_dir = r"E:\xwechat_files\wxid_z9wrrwcf37tu22_71df\msg\file\2025-06\图\图"
output_dir = os.path.join(input_dir, "压缩后")
target_size_mb = 20
img_extensions = ['.jpg', '.jpeg', '.png']

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

# 获取所有图片文件
img_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir)
             if os.path.splitext(f)[1].lower() in img_extensions]

# 估算初始压缩质量（从85开始）
quality = 85
step = 5

# 循环直到压缩后的总大小小于目标
while True:
    total_size = 0
    for path in img_paths:
        img = Image.open(path)
        img = img.convert("RGB")  # 避免P模式、RGBA出错
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        total_size += buffer.tell()

    if total_size <= target_size_mb * 1024 * 1024 or quality < 20:
        break
    else:
        quality -= step  # 继续降低质量压缩

# 最终保存压缩图片
for path in img_paths:
    img = Image.open(path)
    img = img.convert("RGB")
    filename = os.path.basename(path)
    save_path = os.path.join(output_dir, filename)
    img.save(save_path, format="JPEG", quality=quality)

print(f"压缩完成，图片保存在：{output_dir}，压缩质量：{quality}")
