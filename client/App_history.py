import psutil
import time
import os
import psutil
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
    })

# Danh sách lưu trữ các ứng dụng hiện tại
current_apps = set()

while True:
    # Lấy danh sách các ứng dụng đang chạy
    running_apps = {process.name() for process in psutil.process_iter() if process.name().endswith('.exe')}
    
    # Tìm các ứng dụng mới xuất hiện
    new_apps = running_apps - current_apps
    
    # Tìm các ứng dụng bị đóng lại
    closed_apps = current_apps - running_apps
    
    # In ra các ứng dụng mới xuất hiện
    for app in new_apps:
        print(f"New App: {app}")
    
    # In ra các ứng dụng bị đóng lại
    for app in closed_apps:
        print(f"Closed App: {app}")
    
    # Cập nhật danh sách các ứng dụng hiện tại
    current_apps = running_apps
    
    # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
    time.sleep(1)
