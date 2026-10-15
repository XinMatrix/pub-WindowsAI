import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()
        print(f"\r当前鼠标位置：({x}, {y})", end="")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n已停止")
