from screeninfo import get_monitors

# 获取主显示器的大小
monitor = get_monitors()[0]
width = monitor.width
height = monitor.height

print("宽度:", width)
print("高度:", height)