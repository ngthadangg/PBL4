import pyautogui
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, storage
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})

def takeScreenshot():
    now = datetime.now()
    nameScreen = "screenshot" + now.strftime("%Y%m%d-%H%M%S") + ".png"
    print("Name Screen: ", nameScreen)
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(nameScreen)
        
        # Lưu ảnh vào Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(nameScreen)
        blob.upload_from_filename(nameScreen)
        # Gửi link ảnh đến server
        link = blob.public_url
        print("Link: ",  link)
    except Exception as e:
        print("Error: " + str(e))

takeScreenshot()