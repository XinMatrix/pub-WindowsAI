import cv2  # OpenCV for video processing
import yaml  # Assuming you're using this to read the YAML file
from ultralytics import YOLO


def process_video(video_path):
    temp_model = YOLO('runs/detect/train/weights/best.onnx', task='detect')

    # Open the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    total_confidence = 0
    total_boxes = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit loop if there are no more frames

        frame_count += 1
        print(f"Processing Frame {frame_count}...")

        # YOLO expects a file path, so we need to save the frame as an image first (temporary approach)
        temp_filename = 'temp_frame.jpg'
        cv2.imwrite(temp_filename, frame)

        # Run the YOLO detection on the current frame
        temp_results = temp_model(temp_filename)
        boxes = temp_results[0].boxes

        for i in range(len(boxes.xyxy)):
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            print("Box {}: ".format(i + 1))
            print("  Center Point (x, y): ", (center_x.item(), center_y.item()))
            confidence = round(boxes.conf[i].item(), 2)
            print("  Confidence: ", confidence)
            total_confidence += confidence
            total_boxes += 1

        # Optionally display the frame with detections (using OpenCV for video playback)
        # Overlay the detection results onto the frame (you can customize how results are displayed)
        frame_with_detections = temp_results[0].plot()  # this plots the boxes onto the frame

        # Show the frame in a window
        cv2.imshow('Video', frame_with_detections)

        # Wait for 1 ms before moving to the next frame (or until a key is pressed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close the OpenCV windows

    if total_boxes > 0:
        average_confidence = total_confidence / total_boxes
        print("Average Confidence: ", average_confidence)
    else:
        print("No detections made.")


# Call the process_video function with your video file path
video_path = r'C:\Users\USER\Desktop\疲劳驾驶检测\异常情况\Video_14 快速眨眼.mp4'
process_video(video_path)
