import threading
import time

from Dir_Old.Function.screen_recording import startScreenRecording, stopScreenRecording

if __name__ == '__main__':
    # tmp = threading.Thread(target=startScreenRecording, args=('test',)).start()  # 开始录屏
    threading.Thread(target=startScreenRecording, args=('test',)).start()
    time.sleep(5)
    stopScreenRecording()  # 结束录屏

