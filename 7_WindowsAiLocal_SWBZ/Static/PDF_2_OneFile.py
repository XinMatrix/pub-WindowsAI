import os
import shutil

# 源文件夹路径
source_dir = r"C:\Users\USER\Downloads\【APP】AI心理健康"

# 目标文件夹路径（用于存放提取出的PDF文件）
target_dir = r"C:\Users\USER\Downloads\AI心理健康PDF汇总"

# 如果目标文件夹不存在，先创建
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 遍历所有子目录，查找PDF文件
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith('.pdf'):
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)
            # 如果目标文件夹中已有同名文件，可选择是否改名或跳过（这里自动重命名）
            if os.path.exists(target_file):
                base, ext = os.path.splitext(file)
                count = 1
                while os.path.exists(os.path.join(target_dir, f"{base}_{count}{ext}")):
                    count += 1
                target_file = os.path.join(target_dir, f"{base}_{count}{ext}")
            shutil.copy2(source_file, target_file)
            print(f"已复制：{source_file} -> {target_file}")

print("全部PDF文件提取完成。")
