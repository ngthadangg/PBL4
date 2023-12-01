import psutil
import time
import firebase_admin
from firebase_admin import credentials, db

# Cấu hình Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
})
ref = db.reference('app_history')

# Danh sách lưu trữ các ứng dụng hiện tại
current_apps = set()

def push_to_firebase(date, new_apps, closed_apps):
    date_ref = ref.child(date)
    
    # Ghi danh sách ứng dụng mới vào Firebase
    for app in new_apps:
        date_ref.child('new_apps').push().set({'app_name': app, 'timestamp': int(time.time())})

    # Ghi danh sách ứng dụng đóng lại vào Firebase
    for app in closed_apps:
        date_ref.child('closed_apps').push().set({'app_name': app, 'timestamp': int(time.time())})

# Lặp vô hạn
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
    
    # Đẩy dữ liệu vào Firebase với ngày hiện tại
    current_date = time.strftime('%Y-%m-%d')
    push_to_firebase(current_date, new_apps, closed_apps)
    
    # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
    time.sleep(1)
