import subprocess


def monitor_cpu_usage():
    command = 'typeperf "\\Processor(_Total)\\% Processor Time'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        print("Monitoring CPU usage. Press Ctrl+C to stop.")
        while True:
            # 读取标准输出
            line = process.stdout.readline()
            if line:
                # 处理输出行，去除首尾的空白字符
                line = line.strip()
                # 打印输出行
                print(line)
            else:
                # 如果没有更多的输出，跳出循环
                break
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    finally:
        # 终止子进程
        process.terminate()
        process.wait()


if __name__ == "__main__":
    monitor_cpu_usage()
