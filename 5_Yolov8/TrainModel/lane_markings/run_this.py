import sys

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from ultralytics import YOLO


def get_degree(image):  # 最小看起来更稳定些
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 0, 250, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=100)
    min_angle = np.inf  # 初始化为正无穷
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        if angle < min_angle:
            min_angle = angle
    return min_angle


# def get_degree(image):
#     image_np = np.array(image)
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 0, 250, apertureSize=3)
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=100)
#     max_angle = -np.inf  # 初始化为负无穷
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
#         if angle > max_angle:
#             max_angle = angle
#     return max_angle


# def get_degree(image):
#     image_np = np.array(image)
#     gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 0, 250, apertureSize=3)
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=10, maxLineGap=100)
#     total_angle = 0
#     num_lines = 0
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
#         total_angle += angle
#         num_lines += 1
#     return total_angle / num_lines


def crop_rectangle(frame, point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    left = int(min(x1, x2))
    top = int(min(y1, y2))
    right = int(max(x1, x2))
    bottom = int(max(y1, y2))
    # Ensure the coordinates are within the image bounds
    height, width, _ = frame.shape
    left = max(0, min(left, width))
    top = max(0, min(top, height))
    right = max(0, min(right, width))
    bottom = max(0, min(bottom, height))
    cropped_frame = frame[top:bottom, left:right]
    return Image.fromarray(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB))  # 导包错误


def execute_data(boxes, image):
    # FIXME 动态追踪问题，角度差距过大则不显示
    # TODO 画面左边的取最小，右边的取最大？
    detections = []
    theta_degrees = []
    for i in range(len(boxes.xyxy)):  # 这里是循环每个框
        detections.append((boxes.xyxy[i][0], boxes.xyxy[i][1], boxes.xyxy[i][2], boxes.xyxy[i][3]))
        img = crop_rectangle(image, (boxes.xyxy[i][0].item(), boxes.xyxy[i][1].item()),
                             (boxes.xyxy[i][2].item(), boxes.xyxy[i][3].item()), )
        try:
            theta_degrees.append(get_degree(img))
        except Exception as e:
            print(f"Error in get_degree: {e}")
            return None
    print('角度 = ', theta_degrees)
    # 短一点，多线程加载模型
    # 不要平均，要最大或最小值角度
    for detection, angle in zip(detections, theta_degrees):
        if abs(angle) < 10:  # 如果角度绝对值小于阈值则不显示，直接跳过
            continue
        x_min, y_min, x_max, y_max = detection
        center_x = int((x_min + x_max) / 2)
        center_y = int((y_min + y_max) / 2)
        length = min(x_max - x_min, y_max - y_min)  # 直线长度取框的最小边长
        angle_rad = np.deg2rad(angle)  # 将角度转换为弧度
        slope = (y_max - y_min) / (x_max - x_min)
        # length /= 0.7 * abs(slope)  # 较为稀疏
        length /= 0.6 * abs(slope)  # 几乎完美
        # length /= 0.5 * abs(slope)  # 正常连接
        # length /= 0.3 * abs(slope)  # 连接过度
        x1 = int(center_x - length * np.cos(angle_rad) / 2)
        y1 = int(center_y + length * np.sin(angle_rad) / 2)
        x2 = int(center_x + length * np.cos(angle_rad) / 2)
        y2 = int(center_y - length * np.sin(angle_rad) / 2)
        cv2.line(image, (x1, y2), (x2, y1), (0, 0, 255), 4)
    cv2.imshow('Lines', image)


class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 500, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

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
        self.model.predict('temp_frame.jpg')

    def select_image_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "All Files (*);;Image Files (*.jpg *.png)", options=options)
        if file_name:
            print('Processing...')
            processed_frame = self.model.predict(file_name)
            cv2.imshow('name', processed_frame[0].plot())
            print('Process Finished')

    def update_frame(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()
            if ret:
                results = self.model.predict(source=frame)
                result = results[0]
                execute_data(result.boxes, frame)

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
                self.load_video_yolo(video_url)

    def load_video(self, url):
        video_path = QUrl.fromLocalFile(url)
        media_content = QMediaContent(video_path)
        self.media_player.setMedia(media_content)
        self.media_player.play()
        self.media_player.pause()  # 这两行代码可以加载出来伪预览图


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
            # QMessageBox.information(None, "登录成功", "欢迎回来，{}".format(username))
            QMessageBox.information(None, "登录成功", "请稍等，程序正在初始化")
            self.video_window = VideoWindow()
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
