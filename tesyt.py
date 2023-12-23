import os
import sqlite3
from datetime import datetime, timedelta

# Đường dẫn đến file lịch sử Edge
db_path = os.path.expanduser('~') + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Lấy thời gian bắt đầu và kết thúc của ngày hôm nay
today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

# Chuyển đổi thời gian sang định dạng micro giây
today_start_unix = int(today_start.timestamp()) * 1000000
today_end_unix = int(today_end.timestamp()) * 1000000

try:    
    # Thực hiện câu lệnh SELECT với điều kiện thời gian
    # cursor.execute("SELECT url, title, last_visit_time FROM urls WHERE last_visit_time BETWEEN ? AND ? ORDER BY last_visit_time DESC LIMIT 100",
    #             (today_start_unix, today_end_unix))
    cursor.execute("SELECT url, title, last_visit_time FROM urls  ORDER BY last_visit_time DESC LIMIT 100")
    results = cursor.fetchall()
except Exception as e:
    print("Lỗi: ", e)
# In kết quả
for result in results:
    print(result)

# Đóng kết nối
connection.close()
