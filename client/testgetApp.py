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

getAppHistory()
