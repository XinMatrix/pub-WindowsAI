import pyautogui
import threading
import time


def click_position(x, y):
    pyautogui.click(x, y)
    time.sleep(0.1)  # 延迟 0.01 秒


if __name__ == '__main__':
    threads = []
    for y in range(2):
        for x in range(9):
            x_pos = 600 + x * 10
            y_pos = 500 + y * 10
            thread = threading.Thread(target=click_position, args=(x_pos, y_pos))
            threads.append(thread)
            thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()
