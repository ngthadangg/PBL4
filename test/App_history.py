import psutil
import time

# Danh sách lưu trữ các ứng dụng hiện tại
current_apps = set()

while True:
    # Lấy danh sách các ứng dụng đang chạy
    running_apps = {process.name() for process in psutil.process_iter() if process.name().endswith('.exe')}
    
    # Tìm các ứng dụng mới xuất hiện
    new_apps = running_apps - current_apps
    
    # In ra các ứng dụng mới xuất hiện
    for app in new_apps:
        print(f"New App: {app}")
    
    # Cập nhật danh sách các ứng dụng hiện tại
    current_apps = running_apps
    
    # Chờ 1 giây trước khi lặp lại để tránh tải nhiều tài nguyên hệ thống
    time.sleep(1)
