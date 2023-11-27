import cv2
import torch
import time
from datetime import datetime
import RPi.GPIO as GPIO
import concurrent.futures
from RpiMotorLib import RpiMotorLib

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/csce483/Documents/apds/model/exp4/weights/best.pt')
model.conf = 0.6  # Set confidence threshold

# Initialize video capture for the webcam
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None
recording = False
last_recorded_time = 0

# Folder to save videos
ftp_folder = '/home/csce483/FTP/files'

GPIOyaw = [17, 27, 22, 5]
GPIOpitch = [23, 24, 25, 16]

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

motorYaw = RpiMotorLib.BYJMotor("Yaw", "28BYJ")
motorPitch = RpiMotorLib.BYJMotor("Pitch", "28BYJ")

while True:
    print('beginning loop')
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    # Perform object detection only if not currently recording
    if not recording:
        results = model(frame)
        detections = results.xyxy[0].cpu().numpy()

        # Process detections and start recording if detected
        for detection in detections:
            print("detected something!")
            x1, y1, x2, y2, conf, cls_id = detection
            class_name = model.names[int(cls_id)]

            # Calculate the center of the bounding box (optional for turret aiming)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, f'{class_name} {conf:.2f}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Start recording if there is a detection and it's been more than 5 seconds since last record
            if (current_time - last_recorded_time > 5):
                print('begin recording')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                video_name = f'detection_{timestamp}.mp4'
                video_path = f'{ftp_folder}/{video_name}'
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
                recording = True
                record_start_time = current_time
                break  # Break after starting recording

    # Record video for 5 seconds
    if recording:
        out.write(frame)
        if (current_time - record_start_time) >= 5:  # Record for 5 seconds
            print('recording for 5 seconds')
            out.release()
            recording = False
            last_recorded_time = current_time

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()