import socket
import pyautogui
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime

# Khởi tạo Firebase
# cred = credentials.Certificate("path/to/your/firebase/credentials.json")
# firebase_admin.initialize_app(cred, {"storageBucket": "your-firebase-bucket-url"})

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "gs://pbl4-09092003.appspot.com"})

# Kết nối đến server
server_address = ('192.168.1.6', 8080)  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

while True:
    data = client_socket.recv(1024).decode('utf-8')

    if data == "takeScreen":
        # Chụp ảnh màn hình
        screenshot = pyautogui.screenshot()
        now = datetime.now()
        nameScreen = "screenshot"+ now.strftime("%H%M%S") +".png"

        # Lưu ảnh vào Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(nameScreen)
        blob.upload_from_file(nameScreen)

        # Gửi link ảnh đến server
        link = blob.public_url
        client_socket.send(link.encode('utf-8'))

client_socket.close()
