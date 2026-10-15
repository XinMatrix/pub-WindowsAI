import pygetwindow as gw
import pyautogui

all_windows = gw.getAllTitles()  # 获取所有打开的窗口
control_panel_window = [window for window in all_windows if "控制面板" in window]  # 查找包含“控制面板”的窗口标题
if control_panel_window:
    gw.getWindowsWithTitle(control_panel_window[0])[0].activate()  # 将控制面板窗口置于前台
    pyautogui.hotkey('alt', 'f4')  # 发送快捷键 Alt + F4 来关闭控制面板窗口
