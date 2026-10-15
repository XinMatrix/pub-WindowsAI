import ctypes
import os
import shutil
import subprocess
import sys
import tkinter as tk
import warnings
from datetime import datetime

import keyboard
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt, QTimer, QDateTime, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, \
    QSizePolicy, QScrollArea, QDesktopWidget, QSpacerItem

from CheckKey import initialize_config, get_activated_status, KeyCheckerApp
from GPT import process_and_execute, reset_messages
from config import log_path, get_language, my_logger


# os.environ['GLib-GIO'] = 'error'
# warnings.filterwarnings("ignore")
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# warnings.filterwarnings("ignore", category=UserWarning)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


img_bot = resource_path("e6e6e6_bot.png")
img_user = resource_path("e6e6e6_user.png")

professions = [
    "今天我也是一名心理学家，可以给你一些心理学问题的答案",
    "今天我也是一名程序员，可以给你一些编程技巧",
    "今天我也是一名医生，可以给你一些治疗建议",
    "今天我也是一名律师，可以给你一些法律问题的解答",
    "今天我也是一名教师，可以给你一些教学方法",
    "今天我也是一名作家，可以给你一些写作技巧",
    "今天我也是一名记者，可以给你一些采访技巧",
    "今天我也是一名演员，可以给你一些表演技巧",
    "今天我也是一名摄影师，可以给你一些摄影技巧",
    "今天我也是一名建筑师，可以给你一些建筑设计的建议",
    "今天我也是一名美术家，可以给你一些绘画技巧",
    "今天我也是一名音乐家，可以给你一些音乐创作技巧",
    "今天我也是一名舞者，可以给你一些舞蹈技巧",
    "今天我也是一名健身教练，可以给你一些训练方法",
    "今天我也是一名足球运动员，可以给你一些运动技巧",
    "今天我也是一名篮球运动员，可以给你一些运动技巧",
    "今天我也是一名网络红人，可以给你一些网络运营技巧",
    "今天我也是一名旅游达人，可以给你一些旅游攻略",
    "今天我也是一名美食评论家，可以给你一些美食推荐",
    "今天我也是一名职场新人，可以给你一些职场建议",
    "今天我也是一名学生，可以给你一些学习方法",
    "今天我也是一名家长，可以给你一些家庭教育方法",
    "今天我也是一名父亲，可以给你一些育儿建议",
    "今天我也是一名母亲，可以给你一些育儿建议",
    "今天我也是一名儿童，可以给你一些儿童游戏的建议",
    "今天我也是一名企业家，可以给你一些商业建议",
    "今天我也是一名投资者，可以给你一些投资建议",
    "今天我也是一名创业者，可以给你一些创业建议",
    "今天我也是一名职场老手，可以给你一些职场经验分享",
    "今天我也是一名心理咨询师，可以给你一些情感问题的建议",
    "今天我也是一名数据分析师，可以给你一些数据分析的技巧",
    "今天我也是一名人力资源专员，可以给你一些招聘技巧",
    "今天我也是一名市场营销专家，可以给你一些市场推广建议",
    "今天我也是一名社会工作者，可以给你一些社会服务的建议",
    "今天我也是一名科学家，可以给你一些科学研究的方法",
    "今天我也是一名项目经理，可以给你一些项目管理的技巧",
    "今天我也是一名财务顾问，可以给你一些理财建议",
    "今天我也是一名游戏开发者，可以给你一些游戏设计的技巧",
    "今天我也是一名公共演讲者，可以给你一些演讲技巧"
]


class MainFunctionThread(QThread):
    message_ready = pyqtSignal(str)  # 定义一个信号

    def __init__(self, parent, user_message):
        super().__init__(parent)
        self.parent = parent
        self.user_message = user_message

    def run(self):
        output = process_and_execute(self.user_message)
        self.message_ready.emit(output)


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.message_history = []  # 用于存储消息历史
        self.history_index = -1  # 用于追踪历史消息的索引

    def initUI(self):
        self.setWindowIcon(QIcon('e6e6e6_bot.png'))
        self.resize(800, 600)  # 设置窗口大小
        self.center()  # 将窗口居中

        # 设置主窗口小部件
        self.widget = QWidget(self)
        self.widget.setObjectName("main_widget")

        layout = QVBoxLayout()  # 垂直布局管理器

        # 聊天显示区域的滚动区域
        self.chat_display_scroll = QScrollArea(self)
        self.chat_display_scroll.setWidgetResizable(True)  # 使滚动区域的内容可以自动调整大小
        self.chat_display_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 垂直滚动条始终显示
        layout.addWidget(self.chat_display_scroll)  # 将滚动区域添加到布局中

        # 聊天显示内容容器
        self.chat_display_content = QWidget()
        self.chat_display_layout = QVBoxLayout(self.chat_display_content)
        self.chat_display_layout.setAlignment(Qt.AlignTop)  # 设置内容对齐方式为顶部对齐
        self.chat_display_scroll.setWidget(self.chat_display_content)  # 设置滚动区域的内容为聊天显示容器

        input_layout = QHBoxLayout()  # 水平布局管理器
        font = QFont("Microsoft YaHei", 14)

        # 重置按钮
        self.reset_button = QPushButton(get_language('重 置'), self)
        self.reset_button.setMinimumHeight(50)  # 设置按钮最小高度
        self.reset_button.setFont(font)  # 设置按钮字体
        self.reset_button.clicked.connect(self.reset_input)  # 绑定点击事件到重置方法
        input_layout.addWidget(self.reset_button)  # 将重置按钮添加到布局中

        # 输入框
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText(get_language('请描述任务'))  # 设置占位符文本
        self.input_box.setTextMargins(10, 3, 3, 3)  # 设置文本边距
        self.input_box.setFont(font)  # 设置 Microsoft YaHei 字体
        self.input_box.setMinimumHeight(50)  # 设置输入框最小高度
        self.input_box.returnPressed.connect(self.send_message)  # 绑定回车事件到发送消息方法
        input_layout.addWidget(self.input_box)  # 将输入框添加到布局中

        # Shift + Enter

        # 发送按钮
        self.send_button = QPushButton(get_language('发 送'), self)
        self.send_button.setMinimumHeight(50)  # 设置按钮最小高度
        self.send_button.setFont(font)  # 设置按钮字体
        self.send_button.clicked.connect(self.send_message)  # 绑定点击事件到发送消息方法
        input_layout.addWidget(self.send_button)  # 将按钮添加到布局中

        # 将输入布局添加到主布局中
        layout.addLayout(input_layout)

        # 设置主小部件的布局
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)  # 设置中央小部件

        # 添加默认消息
        self.add_chat_message(get_language('我是WindowsAi Magic，很高兴见到你'), is_user=False)
        # self.add_chat_message(get_language('强制停止快捷键为：Ctrl+Alt+K'), is_user=False)
        # 添加轮播消息
        self.add_chat_message(get_language(professions[datetime.now().day % len(professions)]), is_user=False)

    def handle_finished(self, message):
        self.add_chat_message(message, is_user=False)

    def center(self):
        # 将窗口居中显示
        screen = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def reset_input(self):
        # 添加默认消息
        self.add_chat_message(
            get_language('-----------------------------------\n\t上下文已重置\n-----------------------------------'),
            is_user=False)
        reset_messages()
        # 滚动到底部
        QTimer.singleShot(10, lambda: self.chat_display_scroll.verticalScrollBar().setValue(
            self.chat_display_scroll.verticalScrollBar().maximum()))

    def send_message(self):
        user_message = self.input_box.text().strip()
        if user_message:
            my_logger.info(f"用户: {user_message}")
            self.add_chat_message(user_message, is_user=True)
            self.input_box.clear()

            # 存储消息到历史记录
            self.message_history.append(user_message)
            self.history_index = len(self.message_history)  # 重置索引

            self.main_function_thread = MainFunctionThread(self, user_message)
            self.main_function_thread.message_ready.connect(self.handle_finished)  # 连接信号
            self.main_function_thread.start()

    def add_chat_message(self, message, is_user=True):
        def create_rounded_avatar(image_path, size):
            # 创建圆形头像
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            rect = scaled_pixmap.rect()
            x_offset = (rect.width() - size) // 2
            y_offset = (rect.height() - size) // 2
            cropped_pixmap = scaled_pixmap.copy(x_offset, y_offset, size, size)
            rounded_pixmap = QPixmap(size, size)
            rounded_pixmap.fill(Qt.transparent)

            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(cropped_pixmap))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, size, size)
            painter.end()
            return rounded_pixmap

        message = message.rstrip('\n')  # 去除消息末尾的换行符

        # 添加聊天消息
        timestamp = QDateTime.currentDateTime().toString("HH:mm")  # MM-dd HH:mm:ss
        message_layout = QHBoxLayout()
        avatar_size = 35

        # 创建文本标签
        text_label = QLabel(message)
        text_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        text_label.setWordWrap(True)
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 设置聊天气泡的样式
        if is_user:
            text_label.setAlignment(Qt.AlignRight)
            text_label.setStyleSheet("background-color: #555555; border-radius: 10px; padding: 8px; color: #DDDDDD;")
            message_layout.addStretch()
            message_layout.addWidget(text_label)
            avatar = QLabel(self)
            avatar.setPixmap(create_rounded_avatar(img_user, avatar_size))
            message_layout.addWidget(avatar)
        else:
            avatar = QLabel(self)
            avatar.setPixmap(create_rounded_avatar(img_bot, avatar_size))
            message_layout.addWidget(avatar)
            text_label.setAlignment(Qt.AlignLeft)
            text_label.setStyleSheet("background-color: #555555; border-radius: 10px; padding: 8px; color: #DDDDDD;")
            message_layout.addWidget(text_label)
            message_layout.addStretch()

        # 创建复制按钮
        copy_button = QPushButton(get_language('复制'), self)
        copy_button.setFixedSize(50, 25)
        copy_button.setFont(QFont("Microsoft YaHei", 10))
        copy_button.setStyleSheet("background-color: #666666; color: #FFFFFF; border-radius: 5px;")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(message, copy_button))

        button_layout = QHBoxLayout()

        # 将按钮添加到布局中
        if is_user:
            button_layout.addItem(QSpacerItem(650, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 在左边增加空白区域
            button_layout.addWidget(copy_button)
            button_layout.addStretch()
        else:
            button_layout.addItem(QSpacerItem(45, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 在左边增加空白区域
            button_layout.addWidget(copy_button)
            button_layout.addStretch()

        # 将消息布局添加到聊天显示区域
        self.chat_display_layout.addLayout(message_layout)

        # 添加复制按钮布局
        self.chat_display_layout.addLayout(button_layout)

        # 添加时间戳
        timestamp_label = QLabel(timestamp)
        timestamp_label.setFont(QFont("Microsoft YaHei", 8))
        timestamp_label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)
        self.chat_display_layout.addWidget(timestamp_label)

        # 更新布局和滚动区域
        self.chat_display_content.updateGeometry()
        self.chat_display_scroll.updateGeometry()

        # 滚动到底部
        QTimer.singleShot(10, lambda: self.chat_display_scroll.verticalScrollBar().setValue(
            self.chat_display_scroll.verticalScrollBar().maximum()))

    def copy_to_clipboard(self, message, copy_button):
        # 将消息复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(message)
        my_logger.info(f"已复制: {message}")
        copy_button.setText(get_language('已复制'))
        copy_button.setFont(QFont("Microsoft YaHei", 8))

    def keyPressEvent(self, event):
        # 好像不行呀，输入框换行
        # if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
        # self.input_box.setText(self.input_box.text() + '\n')
        # cursor = self.input_box.textCursor()
        # cursor.insertText('\n')
        # self.input_box.setTextCursor(cursor)
        # 检测是否按下上箭头键
        if event.key() == Qt.Key_Up:
            if self.message_history and self.history_index > 0:
                self.history_index -= 1
                self.input_box.setText(self.message_history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.message_history and self.history_index < len(self.message_history) - 1:
                self.history_index += 1
                self.input_box.setText(self.message_history[self.history_index])
            else:
                self.history_index = len(self.message_history)  # 重置索引
                self.input_box.clear()
        else:
            super().keyPressEvent(event)


def init_ffmpeg_env():
    # 设置源文件夹和目标文件夹路径
    source_folder = os.path.join(os.getcwd(), 'my_ffmpeg')  # 假设my_ffmpeg文件夹在当前工作目录
    target_folder = r'C:\Program Files\my_ffmpeg'
    if not os.path.exists(target_folder):
        try:
            # 检查源文件夹是否存在
            if os.path.exists(source_folder):
                # 将文件夹移动到目标位置
                shutil.move(source_folder, target_folder)
                my_logger.info(f"文件夹已成功移动到 {target_folder}")
            else:
                my_logger.error(f"源文件夹 {source_folder} 不存在")
        except Exception as e:
            my_logger.error(f"移动文件夹时出错: {e}")

    target = r'C:\Program Files\my_ffmpeg\bin'
    powershell_command = f"""
           $existingPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
           if (-not $existingPath.Contains("{target}")) {{
               $newPath = "$existingPath;{target}"
               [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
               Write-Output "PATH 环境变量已更新"
           }} else {{
               Write-Output "路径已在 PATH 环境变量中"
           }}
           """
    try:  # 使用 PowerShell 执行命令
        result = subprocess.run(['powershell', '-Command', powershell_command],
                                capture_output=True, text=True, check=True)
        my_logger.info(f"环境变量已更新，输出日志 {result.stdout}")
    except subprocess.CalledProcessError as e:
        my_logger.error(f"更新环境变量时出现错误: {e.stderr}")
    # 移动 my_ffmpeg 文件夹到 C:\Program Files\
    # 添加Path系统环境变量 C:\Program Files\my_ffmpeg\bin


def main():
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)  # 应用暗色主题
    window = ChatWindow()  # 创建聊天窗口
    mw = qtmodern.windows.ModernWindow(window)  # 创建现代风格窗口
    mw.setWindowIcon(QIcon(img_bot))  # 确保这行在 ModernWindow 之后——这样图标才能正常显示
    mw.show()  # 显示窗口
    sys.exit(app.exec_())  # 启动应用并进入主事件循环


def on_hotkey():
    my_logger.error(get_language('用户强行停止程序'))
    # print(get_language('用户强行停止程序'))
    os._exit(0)


def is_admin():  # 判断是否为管理员，因非管理员打开会导致程序无效
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except OSError:  # 未测试 OSError
        return False


def check_admin():
    # 检测是否为管理员权限
    if is_admin() != 1:
        # print(get_language('权限不足，请使用管理员权限运行'))
        my_logger.critical(get_language('\n权限不足，请使用管理员权限运行'))
        input(get_language('按任意键退出...\n'))
        raise PermissionError(get_language('权限不足，请使用管理员权限运行'))
    my_logger.info(get_language('添加强制停止快捷键') + ' Ctrl+Alt+K')
    # print(get_language('添加强制停止快捷键') + ' Ctrl+Alt+K')
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)  # 强行停止快捷键 Ctrl+Alt+K


if __name__ == '__main__':
    # 在这里检测管理员权限
    check_admin()
    # 检查密钥是否正确——C:\Users\USER/.my_app\settings.ini
    initialize_config()  # 初始化配置文件
    if get_activated_status():  # 如果是True说明未激活，激活返回False，不执行代码
        # 激活时就配置，避免二次重启
        init_ffmpeg_env()  # 初始化环境变量——有些库需要配置，如FFMPEG与WEasyPrint
        root = tk.Tk()  # 未激活
        KeyCheckerApp(root)
        root.mainloop()
    else:
        try:  # 使用顶级异常捕获
            main()
        except Exception as error:
            # my_logger.error(f"{get_language('错误')}: {error}", exc_info=True)
            my_logger.error(f"\n{get_language('错误')}: {error}")
            # print(f"{get_language('错误')}: {error}")
            input(get_language('按任意键退出\n'))
            os.startfile(log_path)

r'''
功能示例：
1. 普通问答
  - 怎么才能每天都开开心心？
  - 1+1=？
2. 系统信息处理
  - 输出文件大小并绘制饼图，E:\jianpianDownload
  - 分析每一个内存大于100MB的程序的内存使用情况，并生成表格图
  - 连接本地mysql，账号root，密码000000，查看有哪些数据库
  - 获取系统的ip地址
3. 系统文件处理（测试中）
  - 在 C:\Users\USER\Desktop\WindowsAi Magic\ 生成一个word，内容是如何保持身心健康
  - Word导出PDF，C:\Users\USER\Desktop\WindowsAi Magic\身心健康指南.docx
  - 生成大量json模拟数据，并保存到 C:\Users\USER\Desktop\WindowsAi Magic\（出现问题，Faker未导入，已修改，等待重新编译）
  - json转excel，C:\Users\USER\Desktop\WindowsAi Magic\Sample.json
  - 压缩并删除原文件，C:\Users\USER\Desktop\WindowsAi Magic\Sample.xlsx
  - 解压这个文件并读取其中的excel文件 C:\Users\USER\Desktop\WindowsAi Magic\Sample.zip
4. 图像处理
  - 转化图片格式为webp  C:\Users\USER\Desktop\WindowsAi Magic\Sample.JPG
  - 压缩图像  C:\Users\USER\Desktop\WindowsAi Magic\Sample.JPG
5. 语音合成识别
  - 文本转语音，保存到 C:\Users\USER\Desktop\WindowsAi Magic\：你好，我是WindowsAi Magic，很高兴认识你
  - 将语音 C:\Users\USER\Desktop\output.mp3 转文本并另存（需要科学上网）
6. 其他任务
  - 帮我在桌面创建十个嵌套文件夹，分别命名1-10
  - 这个文件是什么编码格式 C:\Users\USER\Desktop\Test.py
  - 重命名文件夹下所有图片，格式为 Image_001.jpg

注意：
1. 聊天机器人暂时没有上下文功能，请提供详细描述
2. 输入向上箭头可以调出之前的输入
3. 使用 Ctrl+Alt+C 复制文件地址
4. 描述的越清楚结果会越准确
5. 如果失败请多重试几次

更多功能等待发现

使用PaddleOCR获取屏幕内容并推测我目前在做什么 —— 多重问题
抱歉，我无法直接获取屏幕内容或推测您正在做什么。请您提供具体的文本或信息，我将尽力帮助您处理相关问题。

'''
