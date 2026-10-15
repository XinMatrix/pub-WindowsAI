import pyautogui
import win32gui


def switch_to_window(window_name):  # 遍历窗口，找到与指定窗口名称匹配的窗口
    # 获取所有窗口的标题
    windows = pyautogui.getAllTitles()
    print(windows)
    for window in windows:
        if window_name in window:
            # 切换焦点到指定窗口
            pyautogui.getWindowsWithTitle(window)[0].activate()
            break


# 调用函数切换焦点到指定窗口
# switch_to_window('WindowsAI')
# switch_to_window('BG_WindowsAi.png')
# switch_to_window('用户帐户控制设置')

if __name__ == '__main__':
    import pygetwindow as gw

    try:
        windows = gw.getAllTitles()
        # 过滤掉空标题和特定的无效标题
        print(windows)
    except UnicodeEncodeError as e:
        print(f"UnicodeEncodeError encountered: {e}")
        # 如果遇到UnicodeEncodeError，尝试过滤掉所有包含非ASCII字符的标题


    def callback(tmp_hwnd, tmp_windows):
        if win32gui.IsWindowVisible(tmp_hwnd) and win32gui.GetWindowText(tmp_hwnd):
            tmp_windows.append((tmp_hwnd, win32gui.GetWindowText(tmp_hwnd)))
        return True


    windows_list = []
    win32gui.EnumWindows(callback, windows_list)
    print(windows_list)
