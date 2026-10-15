import logging

import win32gui

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='SimpleTest.log',
                    filemode='a')  # w


def get_running_windows():
    def callback(tmp_hwnd, tmp_windows):
        if win32gui.IsWindowVisible(tmp_hwnd) and win32gui.GetWindowText(tmp_hwnd):
            tmp_windows.append((tmp_hwnd, win32gui.GetWindowText(tmp_hwnd)))
        return True

    windows_list = []
    win32gui.EnumWindows(callback, windows_list)
    return windows_list


if __name__ == '__main__':
    logging.info('---------------------- Start ----------------------------')
    windows = get_running_windows()
    for hwnd, title in windows:
        logging.info(title)
        print(title)
    input('Press any key to exit...')

# 使用窗口名称检测可以避免使用OCR，提高稳定性
# PyCharm Community Edition 安装 - 安装页面
# PyCharm 用户协议 - 首次启动页面
# 这里还有一个隐私协议，但是是连着的，所以不用管
# Welcome to PyCharm - 程序首页
# WAIT_WINDOWS(PyCharm Community Edition 安装)
