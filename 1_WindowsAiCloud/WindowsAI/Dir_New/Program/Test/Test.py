# 最好能有个窗口实时显示
import psutil
import GPUtil
import time


def get_system_usage_changes():
    # 初始化前一个状态
    prev_cpu_usage = None
    prev_memory_usage = None
    prev_bytes_sent = None
    prev_bytes_recv = None
    prev_gpu_usage = []

    while True:
        # 获取 CPU 使用率
        cpu_usage = psutil.cpu_percent(interval=1)

        # 打印变化率
        if prev_cpu_usage is not None:
            cpu_change = cpu_usage - prev_cpu_usage
            print(
                f"CPU Usage Change: {'UP' if cpu_change > 0 else 'DOWN' if cpu_change < 0 else 'No Change'} {abs(cpu_change):.2f}%")
        prev_cpu_usage = cpu_usage

        time.sleep(1)

        continue

        # 获取内存使用情况
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        # 获取网络使用情况
        network_info = psutil.net_io_counters()
        bytes_sent = network_info.bytes_sent
        bytes_recv = network_info.bytes_recv

        # 获取 GPU 使用情况（适用于 NVIDIA GPU）
        gpu_usage = []
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_usage = [gpu.load * 100 for gpu in gpus]
        except ImportError:
            gpu_usage = ["N/A"]

        # 打印变化率
        if prev_cpu_usage is not None:
            cpu_change = cpu_usage - prev_cpu_usage
            print(
                f"CPU Usage Change: {'UP' if cpu_change > 0 else 'DOWN' if cpu_change < 0 else 'No Change'} {abs(cpu_change):.2f}%")
        prev_cpu_usage = cpu_usage

        if prev_memory_usage is not None:
            memory_change = memory_usage - prev_memory_usage
            print(
                f"Memory Usage Change: {'UP' if memory_change > 0 else 'DOWN' if memory_change < 0 else 'No Change'} {abs(memory_change):.2f}%")
        prev_memory_usage = memory_usage

        if prev_bytes_sent is not None and prev_bytes_recv is not None:
            sent_change = bytes_sent - prev_bytes_sent
            recv_change = bytes_recv - prev_bytes_recv
            print(
                f"Network - Bytes Sent Change: {'UP' if sent_change > 0 else 'DOWN' if sent_change < 0 else 'No Change'} {abs(sent_change)} bytes")
            print(
                f"Network - Bytes Received Change: {'UP' if recv_change > 0 else 'DOWN' if recv_change < 0 else 'No Change'} {abs(recv_change)} bytes")
        prev_bytes_sent = bytes_sent
        prev_bytes_recv = bytes_recv

        if gpu_usage != ["N/A"]:
            gpu_changes = []
            for i, gpu in enumerate(gpu_usage):
                prev_gpu = prev_gpu_usage[i] if i < len(prev_gpu_usage) else None
                if prev_gpu is not None:
                    gpu_change = gpu - prev_gpu
                    gpu_changes.append(
                        f"GPU {i} Usage Change: {'UP' if gpu_change > 0 else 'DOWN' if gpu_change < 0 else 'No Change'} {abs(gpu_change):.2f}%")
                else:
                    gpu_changes.append(f"GPU {i} Usage: {gpu}% (No Previous Data)")
            for change in gpu_changes:
                print(change)
        prev_gpu_usage = gpu_usage

        # 等待 1 秒钟再进行下一次采样
        time.sleep(1)


# 调用函数开始监控
get_system_usage_changes()
