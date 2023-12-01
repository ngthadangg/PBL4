import sqlite3
import os
import time

def get_browsing_history():
    while True:
        
        db_path = os.path.expanduser('~') + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"
        # db_path = os.path.expanduser('~') + r'\AppD   ata\Local\Microsoft\Edge\User Data\Default'


        # Kết nối đến cơ sở dữ liệu SQLite
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Truy vấn để lấy lịch sử truy cập web
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
        results = cursor.fetchall()

        # In lịch sử truy cập web
        print("Browsing History:")
        for row in results:
            url, title, last_visit_time = row
            print(f"{last_visit_time}: {title} - {url}")

        # Đóng kết nối
        cursor.close()
        connection.close()

        # Chờ 5 giây trước khi lấy dữ liệu tiếp theo
        time.sleep(5)

# Gọi hàm để bắt đầu lấy dữ liệu liên tục
get_browsing_history()
