import numpy as np
import cv2
import pickle
import os
import sys

# Đưa thư mục project vào sys
cur_dir = os.getcwd()
sys.path.append(cur_dir)
# Import Cascades nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
# Đường dẫn của video
video_path = "video/trang.mp4"

cap = cv2.VideoCapture(video_path)

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
dem = 1
# Bắt hình ảnh liên tục từ video và cắt gương mặt có trong đó ra
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        # resize lại hình ảnh khuôn mặt
        resized = cv2.resize(roi_color, (250, 250))
        cv2.imshow("frame", frame)
        cv2.imwrite("image_train/trang/trang" + str(dem) + ".jpg", resized)
        # color = (255, 0, 0)  # BGR 0-255
        # stroke = 2
        # end_cord_x = x + w
        # end_cord_y = y + h
        # cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    dem = dem + 1
    # if cv2.waitKey(20) & 0xFF == ord("q"):
    #     break
    if dem == 151:
        break

cap.release()
cv2.destroyAllWindows()
