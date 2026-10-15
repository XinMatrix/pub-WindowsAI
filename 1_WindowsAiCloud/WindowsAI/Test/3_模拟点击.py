import time

import win32api
import win32con


def smooth_move_win32(x, y, duration=1, steps=100):
    start_x, start_y = win32api.GetCursorPos()
    x_distance = x - start_x
    y_distance = y - start_y
    for i in range(steps):
        progress = i / steps
        if progress < 0.5:
            easing_progress = 2 * progress * progress
        else:
            easing_progress = -1 + (4 - 2 * progress) * progress
        move_to_x = round(start_x + x_distance * easing_progress)
        move_to_y = round(start_y + y_distance * easing_progress)
        win32api.SetCursorPos((move_to_x, move_to_y))
        time.sleep(duration / steps)


def press_key(key):
    # 模拟按下按键
    win32api.keybd_event(key, 0, 0, 0)
    time.sleep(0.1)
    # 模拟释放按键
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def click_current_position():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)



if __name__ == '__main__':
    smooth_move_win32(250, 120)
    # 可以，Win32 YYDS
    # click(100, 100)
    # click()
    click_current_position()
    # press_key(65)  # 0x41对应'A'
    # press_key(0x0D)  # 0x0D对应回车键
