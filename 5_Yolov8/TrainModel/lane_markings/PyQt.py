# 写一个登录页面
# 加载模型实时识别视频
import sys

import cv2
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from ultralytics import YOLO

from TrainModel.lane_markings.draw_line import execute_data

total_boxes = 0


class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        # self.setGeometry(100, 100, 800, 600)
        self.setGeometry(100, 100, 500, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # self.video_widget = QVideoWidget()
        # self.layout.addWidget(self.video_widget)
        #
        # self.media_player.setVideoOutput(self.video_widget)

        # Play button
        # self.play_button = QPushButton("播放")
        # self.play_button.clicked.connect(self.play_video)
        # self.layout.addWidget(self.play_button)

        self.choose_button = QPushButton("选择视频文件")
        self.choose_button.clicked.connect(self.select_file)  # 绑定选择文件按钮的点击事件
        self.layout.addWidget(self.choose_button)

        self.select_image_button = QPushButton("选择图片文件")
        self.select_image_button.clicked.connect(self.select_image_file)
        self.layout.addWidget(self.select_image_button)

        self.video_capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_playing = False

        self.model = YOLO('best_50.onnx', task='detect')  # 这个应该更好
        # self.model = YOLO('best_20_new.onnx', task='detect')  # 这个应该更好
        # self.model = YOLO('best_150_new.onnx', task='detect')

    def select_image_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "All Files (*);;Image Files (*.jpg *.png)", options=options)
        if file_name:
            processed_frame = self.model.predict(file_name)
            cv2.imshow('name', processed_frame[0].plot())
            # execute_data(processed_frame[0].boxes, 1, file_name)
            # cv2.imshow('结果', cv2.imread('show_results.jpg'))  # 推荐使用20的模型

    def update_frame(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()
            # print('CheckPoints 1 ', ret)
            if ret:
                results = self.model.predict(source=frame)
                result = results[0]
                # anno_frame = result.plot()
                # cv2.imshow("V8", anno_frame)

                # 将当前帧保存到本地文件
                # 好像不能直接识别frame
                # temp_file_path = "temp_frame.jpg"
                # cv2.imwrite(temp_file_path, frame)
                # load_model_and_execute(temp_file_path)
                # load_model_and_execute(frame)
                # processed_frame = self.model.predict(temp_file_path)
                # outcome_path = 'show_results.jpg'
                # cv2.imwrite(outcome_path, processed_frame[0])
                # cv2.imshow('123', cv2.imread(outcome_path))
                # cv2.imwrite('show_results.jpg', processed_frame[0])
                # execute_data(result.boxes, total_boxes, temp_file_path)
                # 准确率有点低而且过一会自己就关了
                print('CheckPoints 1')
                execute_data(result.boxes, total_boxes, frame)
                print('CheckPoints 2')
                total_boxes += 1
            # else:
            #     self.video_capture.release()
            #     self.timer.stop()
            #     self.is_playing = False

    def load_video_yolo(self, url):
        self.video_capture = cv2.VideoCapture(url)
        if not self.is_playing:
            self.timer.start(20)  # 根据需要调整时间间隔
            self.is_playing = True

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Video files (*.mp4 *.avi)")
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                video_url = selected_files[0]
                # self.load_video(video_url)
                self.load_video_yolo(video_url)

    def load_video(self, url):
        video_path = QUrl.fromLocalFile(url)
        media_content = QMediaContent(video_path)
        self.media_player.setMedia(media_content)
        self.media_player.play()
        self.media_player.pause()  # 这两行代码可以加载出来伪预览图

    # def play_video(self):
    #     if self.media_player.state() == QMediaPlayer.PlayingState:
    #         self.media_player.pause()
    #         self.play_button.setText("播放")
    #     else:
    #         self.media_player.play()
    #         self.play_button.setText("暂停")


class DatabaseManager:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('users.db')  # SQLite数据库文件名
        if not self.db.open():
            QMessageBox.critical(None, "错误", "无法打开数据库")
            sys.exit(1)
        self.create_table()

    @staticmethod
    def create_table():
        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")

    @staticmethod
    def add_user(username, password):
        query = QSqlQuery()
        query.prepare('INSERT INTO users (username, password) VALUES (:username, :password)')
        query.bindValue(':username', username)
        query.bindValue(':password', password)
        if not query.exec_():
            QMessageBox.warning(None, "注册失败", "注册新用户时发生错误")

    @staticmethod
    def validate_user(username, password):
        query = QSqlQuery()
        query.prepare('SELECT * FROM users WHERE username = :username AND password = :password')
        query.bindValue(':username', username)
        query.bindValue(':password', password)
        if query.exec_() and query.next():
            return True
        return False


class LoginWindow(QWidget):
    def __init__(self, temp_db_manager):
        super().__init__()

        self.video_window = None
        self.db_manager = temp_db_manager

        self.setWindowTitle('登录')
        self.setGeometry(200, 200, 300, 200)

        self.username_label = QLabel('用户名:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('密码:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton('注册')
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.db_manager.validate_user(username, password):
            QMessageBox.information(None, "登录成功", "欢迎回来，{}".format(username))
            self.video_window = VideoWindow()
            # 默认播放
            # video_url = r'C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\lane_markings\DriverCar.mp4'
            # self.video_window.load_video(video_url)  # 替换为你的视频文件路径
            self.video_window.show()
            self.close()  # 关闭登录窗口
        else:
            QMessageBox.warning(None, "登录失败", "用户名或密码错误")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(None, "注册失败", "用户名和密码不能为空")
            return

        self.db_manager.add_user(username, password)
        QMessageBox.information(None, "注册成功", "用户 {} 注册成功".format(username))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = LoginWindow(db_manager)
    window.show()
    sys.exit(app.exec_())
