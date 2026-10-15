import time

from pynput import mouse


def on_move(x, y):
    print(f"鼠标移动到: ({x}, {y})")


# 创建监听器
listener = mouse.Listener(on_move=on_move)
listener.start()

try:
    # 保持程序运行
    while True:
        time.sleep(1)
        pass
except KeyboardInterrupt:
    listener.stop()
    print("\n程序已停止")
