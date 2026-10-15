import subprocess


def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


if __name__ == '__main__':
    # 这是退出程序，不是卸载
    # temp = run_cmd('''wmic process where "name='qq.exe'" delete''').stdout
    # temp = run_cmd('''wmic process where "name='Chrome.exe'" delete''').stdout  # 可以关闭浏览器
    temp = run_cmd('''wmic process get caption,CSName''').stdout
    print(temp)
    # print('删除实例' in temp)  # True说明关闭成功，其实直接执行就好了，没必要判断是否执行成功
    # wmic process get caption,CSName,ProcessID 查看正在运行的进程
    # wmic process where "name='qq.exe'" delete
    # 启动很可能还是需要Listary相关技术，因为未知路径，所以不能直接启动
    # 直接Windows搜索不就好了XD
    # '''wmic process where "name='qq.exe'" delete'''  # 如果显示没有可用实例说明没有在运行，如果显示实例删除成功那就是正在运行

    # from pywinauto import application
    #
    # # 启动应用程序对象
    # app = application.Application()
    # # 连接到 Chrome 进程
    # app.connect(path="chrome.exe")
    # # 找到 Chrome 的主窗口
    # chrome_window = app.top_window()
    # # 点击关闭按钮
    # chrome_window.close()
