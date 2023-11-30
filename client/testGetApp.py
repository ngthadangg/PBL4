import psutil
import time

def is_user_application(app_info):
    try:
        user = psutil.Process(app_info['pid']).username()
        if not user.startswith("NT AUTHORITY") and not user.startswith("SYSTEM"):
            return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return False

def getAppHistory():
    current_apps = set()
    while True:
        running_apps = [process.info for process in psutil.process_iter(attrs=['pid', 'name']) if process.info['name'].endswith('.exe')]
        
        user_apps = {app['name'] for app in running_apps if is_user_application(app)}

        new_apps = user_apps - current_apps
        closed_apps = current_apps - user_apps

        for app in new_apps:
            app_new = "New App: {}".format(app)
            print(app_new)

        current_apps = user_apps

        time.sleep(1)

# Gọi hàm để kiểm tra
getAppHistory()
