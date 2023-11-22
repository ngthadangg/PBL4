import psutil
current_apps = set()
while True:
    # Lấy danh sách các ứng dụng đang chạy
    running_apps = {process.name() for process in psutil.process_iter() if process.name().endswith('.exe')}
    
    new_apps = running_apps - current_apps
    closed_apps = current_apps - running_apps
    
    for app in new_apps:
        # print(f"New App: {app}")
        app_new = "New App: {}".format(app)
        # clientSocket.send(app_new.encode('utf-8'))
    
    for app in closed_apps:
        # print(f"Closed App: {app}")
        app_close = "Closed App: {}".format(app)
        # clientSocket.send(app_close.encode('utf-8'))
    
    current_apps = running_apps        
