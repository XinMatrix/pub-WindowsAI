# 获取Windows系统用户已知信息
if __name__ == '__main__':
    import os
    import getpass

    # 获取当前用户名
    username = getpass.getuser()

    # 获取用户主目录
    home_dir = os.path.expanduser("~")

    # 获取当前工作目录
    current_working_directory = os.getcwd()

    # 打印信息
    print(f"用户名: {username}")
    print(f"用户主目录: {home_dir}")
    print(f"当前工作目录: {current_working_directory}")
   