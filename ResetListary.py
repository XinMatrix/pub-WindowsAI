import ctypes
import os
import time
import psutil


def kill_listary():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and 'Listary.exe' in proc.info['name']:
            print(f"正在结束进程：{proc.info['name']} (PID: {proc.info['pid']})")
            try:
                proc.kill()
                print("Listary.exe 已成功结束。")
            except Exception as e:
                print(f"结束进程失败：{e}")
            return
    print("未检测到正在运行的 Listary.exe 进程。")


def start_listary():
    exe_path = r"C:\Listary.exe.lnk"
    if os.path.exists(exe_path):
        print("正在尝试以管理员权限启动 Listary...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
            print("Listary 启动命令已发送。")
        except Exception as e:
            print(f"启动失败：{e}")
    else:
        print("路径无效，请检查：", exe_path)


if __name__ == "__main__":
    kill_listary()
    time.sleep(5)  # 等待进程彻底关闭
    start_listary()

# "C:\Users\USER\AppData\Local\Programs\Python\Python39\Scripts\pyinstaller.exe" --onefile E:\WindowsAi\ResetListary.py
# 打包要加引号。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。不然就安装到其他环境里了

# C:\Users\USER\AppData\Local\Programs\Python\Python39\python.exe -m pip install psutil
# 为什么在Pycharm中启动的就可以打开，打包成程序就不行了——还真是，算了，就在这运行把
# 好像运行完自动化代码Listary就用不了了
