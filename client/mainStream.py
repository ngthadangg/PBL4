# client.py
import cv2
import socket
import pickle
import struct

# Khởi tạo OpenCV VideoCapture
cap = cv2.VideoCapture(0)

# Khởi tạo socket để gửi dữ liệu video
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.10', 8080)

while True:
    # Đọc frame từ camera
    ret, frame = cap.read()

    # Chuyển đổi frame thành dạng bytes
    data = pickle.dumps(frame)

    # Gửi dữ liệu frame qua socket UDP
    client_socket.sendto(struct.pack("L", len(data)) + data, server_address)

# Đóng tất cả các kết nối và cửa sổ hiển thị
cap.release()