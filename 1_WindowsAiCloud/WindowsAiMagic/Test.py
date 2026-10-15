import os
import plotly.graph_objects as go


# 函数：计算目录的总大小
def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # 跳过无法访问的文件
            try:
                total_size += os.path.getsize(fp)
            except Exception as e:
                print(f"Error getting size of {fp}: {e}")
    return total_size


# 获取 C 盘根目录下的文件夹
# drive = "C:\\"
drive = r'C:\Users\USER'
folders = [os.path.join(drive, f) for f in os.listdir(drive) if os.path.isdir(os.path.join(drive, f))]

# 计算每个文件夹的大小，并筛选大于100MB的目录
folder_sizes = {}
total_folders = len(folders)  # 文件夹总数

for i, folder in enumerate(folders):
    print(f"Processing folder {i + 1}/{total_folders}: {folder}")

    # 计算当前文件夹的大小
    folder_size = get_directory_size(folder)

    # 如果文件夹大小大于 100MB，则加入结果集
    if folder_size > 100 * 1024 ** 2:
        folder_sizes[folder] = folder_size

    # 显示当前进度百分比
    progress = (i + 1) / total_folders * 100
    print(f"Progress: {progress:.2f}%")

# 根据文件夹大小排序
sorted_folder_sizes = dict(sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True))

# 提取文件夹名称和对应的大小（以GB为单位）
folder_names = [os.path.basename(folder) for folder in sorted_folder_sizes.keys()]
folder_sizes_gb = [size / (1024 ** 3) for size in sorted_folder_sizes.values()]

# 使用 Plotly 绘制条形图
fig = go.Figure(data=[
    go.Bar(x=folder_names, y=folder_sizes_gb, text=[f"{size:.2f} GB" for size in folder_sizes_gb], textposition='auto')
])

# 设置图表标题和标签
fig.update_layout(
    title="C盘占用空间大于100MB的目录",
    xaxis_title="目录",
    yaxis_title="占用空间 (GB)",
    bargap=0.2,
)

# 显示图表
fig.show()
