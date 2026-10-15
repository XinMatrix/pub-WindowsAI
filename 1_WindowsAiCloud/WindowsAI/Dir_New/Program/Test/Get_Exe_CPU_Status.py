import psutil


def get_application_resource_usage(application_name):
    total_cpu_percent = 0.0
    total_memory_rss = 0
    total_memory_vms = 0

    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # 如果进程名称包含应用程序名称
            if application_name.lower() in proc.info['name'].lower():
                total_cpu_percent += proc.info['cpu_percent']
                total_memory_rss += proc.info['memory_info'].rss
                total_memory_vms += proc.info['memory_info'].vms
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    total_memory_rss_mb = total_memory_rss / 1024 / 1024
    total_memory_vms_mb = total_memory_vms / 1024 / 1024

    print(f"Application: {application_name}")
    print(f"Total CPU Usage: {total_cpu_percent:.2f}%")
    print(f"Total Memory Usage (RSS): {total_memory_rss_mb:.2f} MB")
    print(f"Total Memory Usage (VMS): {total_memory_vms_mb:.2f} MB")


# 示例：获取名称中包含 'chrome' 的应用程序的整体资源利用率
get_application_resource_usage('chrome')
