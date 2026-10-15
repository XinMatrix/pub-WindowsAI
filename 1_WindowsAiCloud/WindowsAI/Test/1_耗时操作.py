import threading
import time


def long_running_operation():
    # 执行耗时操作
    global_root()
    # time.sleep(5)
    # return "操作完成"


def test():
    time.sleep(5)


def next_function():
    print('延迟执行')


if __name__ == '__main__':
    # 创建一个新的线程来执行耗时操作
    thread = threading.Thread(target=long_running_operation)
    thread.start()
    thread.join()  # 等待线程结束
    print('延迟执行')
    # next_function()  # 在操作完成后调用回调函数
