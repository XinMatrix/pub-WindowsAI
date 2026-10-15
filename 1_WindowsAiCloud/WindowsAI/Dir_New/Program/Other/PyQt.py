import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QDesktopWidget, QShortcut, QMessageBox

# from MainLoop import MainLoopFunction


# 定义日志格式
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     filename='PyQtTest.log',  # 日志输出到的文件
#                     filemode='a')  # 'a' 表示追加模式，'w' 表示覆盖模式

# 我需要写一个日志，专门记录发生的错误及输出信息，给每个重要函数写INFO

class MainWindow(QMainWindow):
    @staticmethod
    def show_dialog(t):  # 创建消息框
        # logging.info('show_dialog')
        msg = QMessageBox()
        msg.setWindowTitle('提示框')
        msg.setText(f'输入内容: {t}')
        msg.exec_()

    def __init__(self):
        super().__init__()

        self.user_input = None
        self.initUI()

        # 定义鼠标按下时的初始位置
        self.drag_start_pos = None

    def initUI(self):
        self.setWindowTitle("WindowsAI客户端")

        # 获取屏幕尺寸
        screen_size = QDesktopWidget().screenGeometry()

        # 计算窗口的位置使其居中显示
        window_width = 800
        window_height = 80
        x = (screen_size.width() - window_width) // 2
        y = (screen_size.height() - window_height) // 2 - 200
        self.setGeometry(x, y, window_width, window_height)

        # 设置窗口背景颜色
        self.setStyleSheet("background-color: #f0f0f0;")

        # 移除窗口标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 创建输入框
        self.user_input = QLineEdit(self)
        # self.url_input.setPlaceholderText("请输入 URL")
        self.user_input.setGeometry(15, 15, window_width - 30, window_height - 30)
        self.user_input.setAlignment(Qt.AlignCenter)  # 文字居中
        self.user_input.setStyleSheet("QLineEdit { border-style: none; }"
                                      "QLineEdit::placeholder { color: #999; }")  # 移除下划线

        # 设置输入框字体大小
        font = QFont()
        font.setPointSize(24)  # 设置字号为16
        # font.setBold(True)
        font.setFamily("Microsoft YaHei")  # 设置字体为微软雅黑
        self.user_input.setFont(font)
        self.user_input.returnPressed.connect(self.send_request)

        # 监听快捷键 Ctrl+Alt+A
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        shortcut.activated.connect(self.open_program)

    def mousePressEvent(self, event):  # 鼠标按下时记录当前位置
        self.drag_start_pos = event.globalPos()

    def mouseMoveEvent(self, event):  # 鼠标移动时计算移动距离，并更新窗口位置
        if self.drag_start_pos:
            delta = event.globalPos() - self.drag_start_pos
            self.move(self.pos() + delta)
            self.drag_start_pos = event.globalPos()

    def mouseReleaseEvent(self, event):  # 鼠标释放时清空初始位置
        self.drag_start_pos = None

    def send_request(self):  # 回车自动发送
        text = self.user_input.text()

        # self.show_dialog(text)  # 用于监听信息

        # MainLoopFunction(text)  # 为什么没有继续执行了

        QApplication.quit()  # 关闭程序

    def keyPressEvent(self, event):  # 捕获键盘按键事件，判断是否按下了Esc键
        if event.key() == Qt.Key_Escape:  # 按下Esc键时退出程序
            QApplication.quit()

    def open_program(self):  # 打开程序
        # 快捷键还有点问题
        # 貌似是Ctrl+Q唤醒，但还有点问题
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
