from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys

app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle("视频播放 实例")
win.resize(800, 500)

videoWidget = QVideoWidget(win)  # 视频控件
videoWidget.resize(win.width(), win.height())

player = QMediaPlayer()
player.setVideoOutput(videoWidget)

url = QFileDialog.getOpenFileUrl()[0]  # 选择本地视频
player.setMedia(QMediaContent(url))
player.play()  # 播放视频

win.show()
sys.exit(app.exec_())
