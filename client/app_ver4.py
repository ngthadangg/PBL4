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
            usage_time = close_time - current_apps[app]
            print(f"Closed App: {app}, Usage Time: {usage_time} seconds")
            
            # Cập nhật thời gian mở và thời gian sử dụng vào Firebase
            current_date = time.strftime('%Y-%m-%d')
            date_ref = ref.child(current_date)
            app_ref = date_ref.child('app_history').push()
            app_ref.update({'app_name': app, 'start-time': current_apps[app], 'usage-time': usage_time})
    
    # Cập nhật danh sách các ứng dụng hiện tại và thời điểm mở
    current_apps = running_apps
    
    # Đẩy dữ liệu vào Firebase với ngày hiện tại
    current_date = time.strftime('%Y-%m-%d')
    date_ref = ref.child(current_date)
    
    # Ghi dữ liệu vào Firebase
    for app, timestamp in new_apps.items():
        app_ref = date_ref.child('app_history').push()
        app_ref.update({'app_name': app, 'start-time': timestamp})
        print('Open app: ' , app, 'start-time: ',  timestamp)
    # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
    time.sleep(1)
