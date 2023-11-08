import time
import os
from ftplib import FTP
from roboflow import Roboflow

# Initialize Roboflow
rf = Roboflow(api_key="EkhI47vMKz00RgoE3lkh")
project = rf.workspace().project("adps")
model = project.version(2, local="http://localhost:9001/").model

def capture_video(video_path):
    # Use libcamera-vid to capture a 5-second video
    os.system(f"libcamera-vid -t 5000 -o {video_path}")

# def upload_to_ftp(video_path):
#     # FTP server details
#     FTP_SERVER = "hogrider-mysql.database.azure.com"
#     FTP_USER = "csce483"
#     FTP_PASS = "hogr!ders483"
#     FTP_DEST_DIR = "your_destination_folder"

#     # Connect to the FTP server
#     with FTP(FTP_SERVER) as ftp:
#         ftp.login(user=FTP_USER, passwd=FTP_PASS)
#         ftp.cwd(FTP_DEST_DIR)
#         with open(video_path, "rb") as video_file:
#             ftp.storbinary(f"STOR {os.path.basename(video_path)}", video_file)
#         # Optionally, delete the video file after upload
#         os.remove(video_path)

def convert_to_mp4(h264_video_path, mp4_video_path):
    os.system(f"ffmpeg -framerate 24 -i {h264_video_path} -c copy {mp4_video_path}")


while True:
    # Define the classes of interest
    classes_of_interest = {'wildboar', 'hawk', 'fox', 'coyote'}

    image_path = "/tmp/temp_image.jpg"
    # Use libcamera-still to capture an image
    os.system(f"libcamera-still -o {image_path}")
    print("image taken")

    # Infer on the captured image
    prediction = (model.predict(image_path, confidence=40, overlap=30).json()) 

    print(prediction)

    # Check if any objects are detected
    if any(pred.get('class') in classes_of_interest for pred in prediction.get('predictions', [])):
        # Capture video in H.264 format
        print("video taken")
        h264_video_path = "/tmp/temp_video.h264"
        capture_video(h264_video_path)
        
        # Convert the H.264 video to MP4 format
        mp4_video_path = "/tmp/temp_video.mp4"
        convert_to_mp4(h264_video_path, mp4_video_path)
        
        # Upload the MP4 video to FTP
        # upload_to_ftp(mp4_video_path)

        # Optionally, remove the temporary H.264 video file
        os.remove(h264_video_path)

    # Wait for 1 second before capturing the next image
    time.sleep(1)
