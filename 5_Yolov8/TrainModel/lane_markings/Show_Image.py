import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


class ImageWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        self.image_path = image_path

        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # 100ms

    def initUI(self):
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.label)
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.update_image()

    def update_image(self):
        pixmap = QPixmap(self.image_path)
        self.label.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    image_path = 'show_results.jpg'  # 替换为你的图片文件路径
    window = ImageWindow(image_path)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
