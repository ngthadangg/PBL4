import psutil
import time
import firebase_admin
from firebase_admin import credentials, db

# Khởi tạo Firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
})
ref = db.reference('app_history')

def sanitize_app_name(app_name):
    # Loại bỏ các ký tự không hợp lệ từ tên ứng dụng
    return app_name.replace('.', '_').replace('#', '_').replace('$', '_').replace('[', '_').replace(']', '_')

def update_app_history(app_name, action):
    timestamp = int(time.time())  # Lấy thời gian hiện tại
    app_ref = ref.child(sanitize_app_name(app_name)).push()
    app_ref.set({
        'action': action,
        'timestamp': timestamp
    })

def getAppHistory():
    current_apps = set()
    while True:
        # Lấy danh sách các ứng dụng đang chạy
        running_apps = {process.name() for process in psutil.process_iter() if process.name().endswith('.exe')}
        
        new_apps = running_apps - current_apps
        closed_apps = current_apps - running_apps
        
        for app in new_apps:
            app_new = "New App: {} - Time: {}".format(app, time.strftime('%Y-%m-%d %H:%M:%S'))
            print(app_new)
            update_app_history(app, 'open')  # Lưu dữ liệu khi ứng dụng mở

        for app in closed_apps:
            app_close = "Closed App: {} - Time: {}".format(app, time.strftime('%Y-%m-%d %H:%M:%S'))
            print(app_close)            
            update_app_history(app, 'close')  # Lưu dữ liệu khi ứng dụng đóng
        
        current_apps = running_apps

        # Đọc dữ liệu từ Firebase và sắp xếp theo thời gian mới nhất đầu tiên
        query = ref.order_by_child('timestamp')
        result = query.get()

        # Hiển thị dữ liệu
        if result:
            for key, value in result.items():
                print(f"{key}: Action - {value['action']}, Timestamp - {value['timestamp']}")

        # Đợi một khoảng thời gian trước khi lặp lại (ví dụ: 1 giây)
        time.sleep(1)

# Gọi hàm để bắt đầu theo dõi ứng dụng
getAppHistory()
