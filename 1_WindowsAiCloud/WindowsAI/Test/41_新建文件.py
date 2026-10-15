import os


def create_python_file(directory, filename, content):
    # 构建文件路径
    file_path = os.path.join(directory, filename)
    # 写入内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


directory = ''  # 替换为你希望的目录路径
filename = 'example.py'  # 替换为你希望的文件名
full_content = f'''# 示例Python文件

def my_function():
    print("Hello, world!")


if __name__ == "__main__":
    my_function()
'''
create_python_file(directory, filename, full_content)
