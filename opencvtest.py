import cv2

cap = cv2.VideoCapture(2)  # Adjust the device number if needed

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        print("Failed to capture frame")

cap.release()
cv2.destroyAllWindows()
