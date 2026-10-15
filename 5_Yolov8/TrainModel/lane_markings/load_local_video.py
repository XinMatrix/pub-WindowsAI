import cv2
from ultralytics import YOLO

model = YOLO('best_50.onnx')
video_path = "Car.mp4"
cap = cv2.VideoCapture(video_path)

# 设置窗口的名称
window_name = "V8"

# 设置窗口的大小，比如宽度为800，高度为600
window_width = 800
window_height = 600

# 创建窗口并设置其大小
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, window_width, window_height)

while cap.isOpened():
    status, frame = cap.read()
    if not status:
        break
    results = model.predict(source=frame)
    result = results[0]
    anno_frame = result.plot()
    cv2.imshow("V8", anno_frame)
    # 设置延迟以减慢视频播放速度
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
