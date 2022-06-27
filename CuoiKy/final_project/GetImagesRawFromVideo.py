import cv2
import pickle
import os
import sys

# Đưa địa chỉ của thư mục hiện tại vào sys
cur_dir = os.getcwd()
sys.path.append(cur_dir)
# Đường dẫn của video
video_path = "video/trang.mp4"
# Lấy frame từ video
cap = cv2.VideoCapture(video_path)

dem = 1

# Hàm resize lại frame theo %
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


# Cho cam bắt liên tục và ghi hình ảnh
while True:
    ret, frame = cap.read()
    frame = rescale_frame(frame)
    cv2.imshow("frame", frame)
    cv2.imwrite("image_test/trang/trang" + str(dem) + ".jpg", frame)
    dem = dem + 1
    if dem == 21:
        break

cap.release()
cv2.destroyAllWindows()
