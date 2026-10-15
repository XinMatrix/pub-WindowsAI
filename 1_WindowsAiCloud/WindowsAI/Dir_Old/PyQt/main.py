import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QDesktopWidget, QShortcut


# 字号加粗
# 设置字体
# Esc退出
# 快捷唤醒
# 使用Conda打包

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.url_input = None
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
        self.url_input = QLineEdit(self)
        # self.url_input.setPlaceholderText("请输入 URL")
        self.url_input.setGeometry(15, 15, window_width - 30, window_height - 30)
        self.url_input.setAlignment(Qt.AlignCenter)  # 文字居中
        self.url_input.setStyleSheet("QLineEdit { border-style: none; }"
                                     "QLineEdit::placeholder { color: #999; }")  # 移除下划线

        # 设置输入框字体大小
        font = QFont()
        font.setPointSize(24)  # 设置字号为16
        # font.setBold(True)
        font.setFamily("Microsoft YaHei")  # 设置字体为微软雅黑
        self.url_input.setFont(font)

        self.url_input.returnPressed.connect(self.send_request)

        # 快捷键还有点问题
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

    def send_request(self):
        text = self.url_input.text()
        # 加载LLAMA模型，输入指令等待输出
        print(text)
        # 假定输出内容
        # input = '卸载QQ'
        output = 'uninstall_qq>>ece_StopProgram->key_win+x->key_p->ocr_搜索应用->cp_qq->hi_uninstall->ocr_卸载->ocr_卸载->ocr_卸载->ocr_是->ocr_确定'

    def keyPressEvent(self, event):  # 捕获键盘按键事件，判断是否按下了Esc键
        if event.key() == Qt.Key_Escape:  # 按下Esc键时退出程序
            QApplication.quit()

    def open_program(self):  # 打开程序
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
