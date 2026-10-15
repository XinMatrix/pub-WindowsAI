import psutil

# 获取所有正在运行的进程
running_processes = psutil.process_iter()

# 遍历每个进程，并打印其名称
for process in running_processes:
    print("正在运行的程序名称:", process.name())
