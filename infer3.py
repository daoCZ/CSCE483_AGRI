import cv2
import torch
import time
import socket
from datetime import datetime
import RPi.GPIO as GPIO
import concurrent.futures
from RpiMotorLib import RpiMotorLib
import mysql.connector

#database
hostname = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname.connect(("8.8.8.8", 80))

class_names = {
    0: 'fox',
    1: 'coyote',
    2: 'hawk',
    3: 'wildboar',
}



def check_node(mydb, mycursor):
    # Grab IP address of computer (Linux)
    ip = hostname.getsockname()[0]
    print("IP address of computer: " + ip)

    # Establish node name
    node_name = 'Node 1'

    # Check if node exists in nodes table, if not, add it. If it does exist, update the ip address
    sql = "SELECT * FROM nodes WHERE name = %s"
    val = (node_name,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if len(result) == 0:
        # Add node to nodes table
        print("Node not in database, adding node to nodes table...")
        sql = "INSERT INTO nodes (name, ip_address) VALUES (%s, %s)"
        val = (node_name, ip)
    else:
        # Update ip address of node
        sql = "UPDATE nodes SET ip_address = %s WHERE name = %s"
        val = (ip, node_name)
    mycursor.execute(sql, val)
    mydb.commit()

    # Find node id of node
    sql = "SELECT node_id FROM nodes WHERE name = %s"
    val = (node_name,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    node_id = result[0][0]
    
    return node_id





def main():
    # Connect to the database
    mydb = mysql.connector.connect(
        host= "hogrider-mysql.mysql.database.azure.com",
        user="csce483",
        # password="Hogr!ders483",
        password="Hogr!ders483",
        database="csce483"
    )
    mycursor = mydb.cursor()

    node_id = check_node(mydb, mycursor)

    # Initialize video capture and VideoWriter
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_path = '/home/csce483/FTP/files'
    frame_rate = 30.0
    out = cv2.VideoWriter(video_path, fourcc, frame_rate, (640, 480))

    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/csce483/Documents/apds/model/exp4/weights/best.pt')
    model.conf = 0.6  # Set confidence threshold

    recording = False
    last_record_time = 0
    record_duration = 5

    # Camera center
    xorigin, yorigin = 320, 240

    GPIOyaw = [17, 27, 22, 5]
    GPIOpitch = [23, 24, 25, 16]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)

    motorYaw = RpiMotorLib.BYJMotor("Yaw", "28BYJ")
    motorPitch = RpiMotorLib.BYJMotor("Pitch", "28BYJ")

    while True:
        start_time=time.time()
        print("beginning loop")
        ret, frame = cap.read()
        if not ret:
            break

        #start_time = time.time()
        current_time = time.time()
        results = model(frame)
        detections = results.xyxy[0].cpu().numpy()
            
        x1 = 0.0
        x2 = 0.0
        y1 = 0.0
        y2 = 0.0
        # Process detectionshost_name = socket.getfqdn(socket.gethostname())
        # node_ip_adress = socket.gethostbyname(host_name)
        # print(node_ip_adress)
        for detection in detections:
            print('detecting something, in loop currently')
            x1, y1, x2, y2, conf, cls_id = detection
            length = x2 - x1
            width = y2 - y1

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame, f'Length: {length:.2f}, Width: {width:.2f}', (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        detection = len(detections) > 0

        #turret 
        yawNEG = True
        yawSteps = 128
        pitchPOS = True
        pitchSteps = 128

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
            print('shooting')
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
        

        if detection:
            if not recording:
                print("detected something")
                recording = True
                last_record_time = time.time()
                print("outputting video to folder")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                video_name = f'detection_{timestamp}.mp4'
                video_path = f'/home/csce483/FTP/files/{video_name}'
                print(video_path)
                out = cv2.VideoWriter(video_path, fourcc, frame_rate, (640, 480))

                animal = class_names.get(cls_id, "Unknown")

                event_time = datetime.now()

                video = video_name

                sql = "INSERT INTO events (node_id, event_time, animal, video) VALUES (%s, %s, %s, %s)"

                # Convert the data types of values to match the table columns
                values = (node_id, event_time, animal, video)

                # Execute the query with the values
                mycursor.execute(sql, values)
                mydb.commit()
        
        if recording:
            print('recording video')
            out.write(frame)   
            if(time.time() - last_record_time > record_duration):
                print('stop recording')
                recording = False
                out.release()
        # Display the resulting frame
        cv2.imshow('frame', frame)
        print('showing frame')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        end=time.time()
        print(f"Loop time: {end - start_time} seconds")

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

     # Close the database connection
    print("Closing database connection...")
    try:
        mydb.close()
    except:
        print("Database connection already closed.")
    print("Database connection closed.")

    print(hostname.getsockname()[0])

main()