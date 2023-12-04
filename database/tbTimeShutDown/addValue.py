import sqlite3
from time import strftime

# Kết nối đến cơ sở dữ liệu và tạo bảng
conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

# Chèn dữ liệu vào bảng user
insert_data_query = '''
INSERT INTO timeShutDown (shutdownTime) VALUES (?);
'''

# Thực thi lệnh SQL với dữ liệu cụ thể
cursor.execute(insert_data_query, (strftime('%H:%M'),))  

# Lưu thay đổi (commit) vào cơ sở dữ liệu
conn.commit()

# Đóng kết nối
conn.close()
