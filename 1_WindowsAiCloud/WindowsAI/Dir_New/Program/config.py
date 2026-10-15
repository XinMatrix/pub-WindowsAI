import os

from DataBase import MySQLDatabase

# def get_local_ip():
#     s = ''
#     try:
#         # 建立一个到外部服务器的连接
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.settimeout(0)
#         s.connect(('8.8.8.8', 80))  # 使用 Google 公共 DNS 服务器
#         local_ip = s.getsockname()[0]
#     except socket.timeout as e:
#         e.args += ('获取本地IP地址失败',)
#         # 处理超时错误
#         local_ip = None
#     except socket.error as e:
#         e.args += ('获取本地IP地址失败',)
#         # 处理网络相关的错误
#         local_ip = None
#     finally:
#         s.close()
#     return local_ip
#
#
# temp_host = get_local_ip()
# print(temp_host)

http_host = '192.168.0.100'
temp_check = {"Value": False}  # 这样可以长久记录变量

ocr_url = f'http://{http_host}:5000/ocr'  # 注意，两个服务应该使用不同的端口
ocr_acc = f'http://{http_host}:5001/ocr_accuracy'  # 端口忘改了

last_img = os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/last_img.jpg")
db = MySQLDatabase(host=http_host, user="000000", password="000000", database="mydatabase")
