# import ctypes
#
#
# def get_now_windows_name():
#     user32 = ctypes.windll.user32
#     foreground_window = user32.GetForegroundWindow()
#     window_title = ctypes.create_string_buffer(255)
#     user32.GetWindowTextA(foreground_window, window_title, 255)
#     return window_title.value.decode('gbk')
#
#
# if __name__ == '__main__':
#     print(get_now_windows_name())
# import wmi
#
# # 连接到本地计算机的WMI服务
# c = wmi.WMI()
#
# # 获取操作系统信息
# for os in c.Win32_OperatingSystem():
#     print("操作系统: ", os.Caption)
#     print("版本号: ", os.Version)
#     print("安装日期: ", os.InstallDate)
#
# # 获取处理器信息
# for processor in c.Win32_Processor():
#     print("处理器: ", processor.Name)
#     print("制造商: ", processor.Manufacturer)
#     print("核心数: ", processor.NumberOfCores)
#
# # 获取磁盘驱动器信息
# for disk in c.Win32_LogicalDisk():
#     print("驱动器: ", disk.Caption)
#     print("总大小: ", round(int(disk.Size) / (1024 ** 3), 2), "GB")
#     print("可用空间: ", round(int(disk.FreeSpace) / (1024 ** 3), 2), "GB")
#
# # 获取网络适配器信息
# for network in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
#     print("适配器: ", network.Description)
#     print("MAC地址: ", network.MACAddress)
#     print("IP地址: ", network.IPAddress)
#
# # 执行自定义查询
# query = "SELECT * FROM Win32_Process WHERE Name = 'python.exe'"
# for process in c.query(query):
#     print("进程: ", process.Name)
#     print("进程ID: ", process.ProcessId)
