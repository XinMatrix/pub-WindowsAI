import subprocess
import sys


def upgrade_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print('pip更新成功！')
    except subprocess.CalledProcessError as e:
        print(f"pip更新失败：{e}")


def install_packages(package_list):
    mirrors = [
        "https://mirrors.aliyun.com/pypi/simple/",
        "https://pypi.tuna.tsinghua.edu.cn/simple/",
        "https://pypi.mirrors.ustc.edu.cn/simple/"
    ]
    for package in package_list:
        installed = False
        for mirror in mirrors:
            command = f"pip install {package} -i {mirror}"
            try:
                subprocess.check_call(command, shell=True)
                print(f"{package} 安装成功！（镜像：{mirror}）")
                installed = True
                break
            except subprocess.CalledProcessError as e:
                print(f"{package} 安装失败：（镜像：{mirror}），尝试下一个镜像。 错误：{e}")
        if not installed:
            print(f"{package} 在所有镜像源上都安装失败。")


def uninstall_packages(package_list):
    for package in package_list:
        command = f"pip uninstall -y {package}"
        try:
            subprocess.check_call(command, shell=True)
            print(f"{package} 卸载成功！")
        except subprocess.CalledProcessError as e:
            print(f"{package} 卸载失败：{e}")


if __name__ == '__main__':
    upgrade_pip()
    install_packages(['ultralytics'])
    # uninstall_packages(['ultralytics'])
