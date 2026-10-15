import psutil


# running_processes = psutil.process_iter()
# for item in running_processes:
#     if item.name() == 'Photos.exe':
#         item.terminate()  # 发送终止信号
#         item.wait()  # 等待进程终止

def kill_processes(processes_name):
    running_processes = psutil.process_iter()
    for item in running_processes:
        # if item.name() == 'Photos.exe':
        if item.name() == processes_name:
            item.terminate()  # 发送终止信号
            item.wait()  # 等待进程终止
