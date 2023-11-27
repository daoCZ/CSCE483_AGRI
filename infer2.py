import cv2
import torch
import time
from datetime import datetime
import RPi.GPIO as GPIO
import concurrent.futures
from RpiMotorLib import RpiMotorLib


# Initialize video capture and VideoWriter
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_path = '/home/csce483/FTP/files'
frame_rate = 20.0
out = cv2.VideoWriter(video_path, fourcc, frame_rate, (640, 480))

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/csce483/Documents/apds/model/exp4/weights/best.pt')
model.conf = 0.6  # Set confidence threshold

recording = False
last_record_time = 0
started_recording = False

# Camera center
xorigin, yorigin = 320, 240

GPIOyaw = [17, 27, 22, 5]
GPIOpitch = [23, 24, 25, 16]

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

motorYaw = RpiMotorLib.BYJMotor("Yaw", "28BYJ")
motorPitch = RpiMotorLib.BYJMotor("Pitch", "28BYJ")



while True:
    print("beginning loop")
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()

    # Process detections
    for detection in detections:
        print('detecting something, in loop currently')
        x1, y1, x2, y2, conf, cls_id = detection
        length = x2 - x1
        width = y2 - y1

        # Draw bounding box and label on the frame
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, f'Length: {length:.2f}, Width: {width:.2f}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    detection = len(detections) > 0
    print(detection)
    print(current_time)

    print(x1, x2, y1, y2)

    yawNEG = True
    yawSteps = 256
    pitchPOS = True
    pitchSteps = 25

    isleft = xorigin < x1
    isright = xorigin > x2
    isup = yorigin < y1
    isdown = yorigin > y2

    if isleft:
        yawNEG = True
    if isright:
        yawNEG = False
    if isup:
        pitchPOS = True
    if isdown:
        pitchPOS = False
    
    isinx = (not isleft) and (not isright)
    isiny = (not isup) and (not isdown)

    if (isinx and isiny): #shoot
        GPIO.output(6, True)

    if detection:
        # CONCURRENT
        GPIO.output(6, False)
        if isinx:
            yawSteps = 0
        if isiny:
            pitchSteps = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(motorYaw.motor_run, GPIOyaw, .001 , yawSteps, yawNEG, False, "full", .05)
            f2 = executor.submit(motorPitch.motor_run, GPIOpitch, .001 , pitchSteps, pitchPOS, False, "full", .05)
    

    if detection and (current_time - last_record_time < 5):
        print("detected something")
        out.write(frame) #write frame out
        if not started_recording:
            print("outputting video to folder")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_name = f'detection_{timestamp}.mp4'
            video_path = f'/home/csce483/FTP/files/{video_name}'
            started_recording = True
            last_record_time = current_time
    else:
        if started_recording and (current_time - last_record_time > 5):
            print('stop recording')
            started_recording = False
        elif started_recording:
            out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    print('showing frame')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()