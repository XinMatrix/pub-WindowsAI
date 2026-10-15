import os

# 获取当前用户的下载文件夹路径
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# 遍历下载文件夹
for root, dirs, files in os.walk(download_folder):
    for file in files:
        # 检查文件名是否包含 "QQ" 和 ".exe"
        if "QQ" in file and file.endswith(".exe"):
            # 构建文件的完整路径
            file_path = os.path.join(root, file)
            print("Found file:", file_path)

            # 打开文件
            os.startfile(file_path)
            # 如果找到了一个符合条件的文件，这里只打开第一个找到的文件，如果您希望继续查找并打开其他文件，可以在此处添加适当的逻辑
            break
    else:
        continue
    break  # 停止遍历，因为已经找到并打开了文件
else:
    print("No file found with name containing 'QQ' and ending with '.exe' in the download folder.")
