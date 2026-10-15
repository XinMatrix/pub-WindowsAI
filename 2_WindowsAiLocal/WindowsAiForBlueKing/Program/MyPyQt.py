import os
import sys

import keyboard
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt, QTimer, QDateTime, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, \
    QSizePolicy, QScrollArea, QDesktopWidget

from Data import temp_check, local_data
# from MyFunClass import MyFun
from CheckKey import initialize_config, get_activated_status, KeyCheckerApp
from config import log_path, get_language, my_logger
import tkinter as tk

ChatWindowsSelf = None


def resource_path(relative_path):
    """获取资源文件的绝对路径，打包后使用"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


img_bot = resource_path("e6e6e6_bot.png")
img_user = resource_path("e6e6e6_user.png")


class IsFinishedThread(QThread):
    finished = pyqtSignal(str)  # 完成信号

    def __init__(self, parent, user_message):
        super().__init__(parent)
        self.parent = parent
        self.user_message = user_message

    def run(self):
        while True:
            if temp_check['Value']:
                if self.user_message:
                    if self.user_message == '1':
                        temp = get_language('配置Hyper-V')
                    elif self.user_message == '2':
                        temp = get_language('关闭用户帐户控制')
                    elif self.user_message == '3':
                        temp = get_language('安装Chrome')
                    elif self.user_message == '4':
                        temp = get_language('安装Python 3.6.7')
                    elif self.user_message == '5':
                        temp = get_language('安装MySQL 5.7.39.0')
                    elif self.user_message == '6':
                        temp = get_language('安装Git')
                    elif self.user_message == '7':
                        temp = get_language('创建Git仓库')
                    elif self.user_message == '8':
                        temp = get_language('创建蓝鲸项目')
                    elif self.user_message == '9':
                        temp = get_language('安装配置PyCharm开发环境')
                    else:
                        temp = get_language('未知命令')
                    finish_text = get_language('执行完成')
                    if self.user_message == '1':
                        another_text = get_language('CMD窗口输入Y重启，重启后打开 Hyper-V 管理器，使用下载的ISO文件即可创建虚拟机')
                        self.finished.emit(f'{finish_text}: {self.user_message}. {temp}\n{another_text}')
                    else:
                        self.finished.emit(f'{finish_text}: {self.user_message}. {temp}')
                    temp_check['Value'] = False  # 重置条件
                    break
            QThread.sleep(1)  # 循环等待


class MainFunctionThread(QThread):
    def __init__(self, parent, user_message, result):
        super().__init__(parent)
        self.parent = parent
        self.user_message = user_message
        self.result = result

    def run(self):  # Here
        from main import main_function
        main_function(self.result, self.user_message)


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global ChatWindowsSelf
        ChatWindowsSelf = self
        self.initUI()

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
        layout.addWidget(self.chat_display_scroll)  # 将滚动区域添加到布局中

        # 聊天显示内容容器
        self.chat_display_content = QWidget()
        self.chat_display_layout = QVBoxLayout(self.chat_display_content)
        self.chat_display_layout.setAlignment(Qt.AlignTop)  # 设置内容对齐方式为顶部对齐
        self.chat_display_scroll.setWidget(self.chat_display_content)  # 设置滚动区域的内容为聊天显示容器

        # 输入布局，包含文本框和发送按钮
        input_layout = QHBoxLayout()  # 水平布局管理器

        # 输入框
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText(get_language('请输入任务编号'))  # 设置占位符文本
        self.input_box.setTextMargins(10, 3, 3, 3)  # 设置文本边距

        # 设置 Microsoft YaHei 字体
        font = QFont("Microsoft YaHei", 14)
        self.input_box.setFont(font)

        self.input_box.setMinimumHeight(50)  # 设置输入框最小高度
        self.input_box.returnPressed.connect(self.send_message)  # 绑定回车事件到发送消息方法
        input_layout.addWidget(self.input_box)  # 将输入框添加到布局中

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
        self.add_chat_message(get_language('我是WindowsAi，很高兴见到你'), is_user=False)
        self.add_chat_message(get_language('强制停止快捷键：Ctrl+Alt+k'), is_user=False)

        # 添加数字转引
        self.add_chat_message(get_language(
            '目前支持功能如下，输入对应数字即可\n'
            '1. 配置Hyper-V\n'
            '2. 关闭用户帐户控制\n'
            '3. 安装Chrome\n'
            '4. 安装Python 3.6.7\n'
            '5. 安装MySQL 5.7.39.0\n'
            '6. 安装Git\n'
            '7. 创建Git仓库\n'
            '8. 创建蓝鲸项目\n'
            '9. 安装配置PyCharm开发环境\n'),
            is_user=False)

    def handle_finished(self, message):
        self.add_chat_message(message, is_user=False)

    def center(self):
        # 将窗口居中显示
        screen = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def send_message(self):
        user_message = self.input_box.text().strip()
        if user_message:
            self.add_chat_message(user_message, is_user=True)
            self.input_box.clear()

            result = ''  # 按任务名称搜索任务

            # IDEA 使用云端数据，方便修改，最终测试时使用本地数据——真棒！
            # response = requests.get('http://192.168.0.100:5002/data')
            # local_data = response.json()

            for item in local_data:
                if user_message == item[0]:
                    result = item[1]
                    break

            if result:
                if user_message == '1':
                    temp = get_language('配置Hyper-V')
                elif user_message == '2':
                    temp = get_language('关闭用户帐户控制')
                elif user_message == '3':
                    temp = get_language('安装Chrome')
                elif user_message == '4':
                    temp = get_language('安装Python 3.6.7')
                elif user_message == '5':
                    temp = get_language('安装MySQL 5.7.39.0')
                elif user_message == '6':
                    temp = get_language('安装Git')
                elif user_message == '7':
                    temp = get_language('创建Git仓库')
                elif user_message == '8':
                    temp = get_language('创建蓝鲸项目')
                elif user_message == '9':
                    temp = get_language('安装配置PyCharm开发环境')
                else:
                    temp = get_language('未知命令')
                QTimer.singleShot(1000, lambda: self.add_chat_message(f"{get_language('即将执行')}: {user_message}. {temp}",
                                                                      is_user=False))

                # 在这里启动主程序
                self.main_function_thread = MainFunctionThread(self, user_message, result)
                self.main_function_thread.start()

                self.is_finished_thread = IsFinishedThread(self, user_message)
                self.is_finished_thread.finished.connect(lambda msg: self.add_chat_message(msg, is_user=False))
                self.is_finished_thread.start()

            else:
                QTimer.singleShot(1000, lambda: self.add_chat_message(f"{get_language('抱歉哦，我还没有学会')}: {user_message}",
                                                                      is_user=False))

    def add_chat_message(self, message, is_user=True):
        # 添加聊天消息
        timestamp = QDateTime.currentDateTime().toString("MM-dd HH:mm:ss")  # 获取当前时间 yyyy-MM-dd HH:mm:ss
        message_layout = QHBoxLayout()  # 创建水平布局管理器
        avatar_size = 35  # 头像大小

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

        text_label = QLabel(message)
        text_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))  # 设置字体
        text_label.setWordWrap(True)  # 启用自动换行

        # 确保 text_label 能扩展以填充可用空间
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 根据用户或响应调整布局属性
        if is_user:
            text_label.setAlignment(Qt.AlignRight)  # 用户消息右对齐
            message_layout.addStretch()  # 推送消息到右侧
            message_layout.addWidget(text_label)
            avatar = QLabel(self)
            avatar.setPixmap(create_rounded_avatar(img_user, avatar_size))  # 设置用户头像
            message_layout.addWidget(avatar)
        else:
            avatar = QLabel(self)
            avatar.setPixmap(create_rounded_avatar(img_bot, avatar_size))  # 设置机器人头像
            message_layout.addWidget(avatar)
            text_label.setAlignment(Qt.AlignLeft)  # 机器人消息左对齐
            message_layout.addWidget(text_label)
            message_layout.addStretch()  # 推送消息到左侧

        self.chat_display_layout.addLayout(message_layout)  # 将消息布局添加到聊天显示布局中

        timestamp_label = QLabel(timestamp)  # 创建时间戳标签
        timestamp_label.setFont(QFont("Microsoft YaHei", 8))  # 设置字体
        timestamp_label.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)  # 设置时间戳对齐方式
        self.chat_display_layout.addWidget(timestamp_label)  # 将时间戳标签添加到聊天显示布局中

        # 更新布局和滚动区域
        self.chat_display_content.updateGeometry()
        self.chat_display_scroll.updateGeometry()

        # 滚动到底部
        QTimer.singleShot(0, lambda: self.chat_display_scroll.verticalScrollBar().setValue(
            self.chat_display_scroll.verticalScrollBar().maximum()))


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
    os._exit(0)


def check_admin():
    # 检测是否为管理员权限
    # if MyFun.System.is_admin() != 1:
    from Class_1_System import is_admin
    if is_admin() != 1:
        my_logger.critical(get_language('权限不足，请使用管理员权限运行'))
        raise PermissionError(get_language('权限不足，请使用管理员权限运行'))
        # 好像不能在这里加 input()
    my_logger.info(get_language('添加强制停止快捷键') + ' Ctrl+Alt+K')
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)  # 强行停止快捷键 Ctrl+Alt+K


if __name__ == '__main__':

    # 在这里检测管理员权限
    check_admin()

    # 检查密钥是否正确——C:\Users\USER/.my_app\settings.ini
    initialize_config()  # 初始化配置文件
    check = get_activated_status()  # 如果是True说明未激活，激活返回False，不执行代码
    if check:  # 未激活
        root = tk.Tk()
        KeyCheckerApp(root)
        root.mainloop()
    else:
        try:  # 使用顶级异常捕获
            main()
        except Exception as error:
            my_logger.error(f"{get_language('错误')}: {error}", exc_info=True)
            os.startfile(log_path)
