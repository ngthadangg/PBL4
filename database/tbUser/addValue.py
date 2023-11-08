import sqlite3

# Kết nối đến cơ sở dữ liệu và tạo bảng
conn = sqlite3.connect('PBL.db')
cursor = conn.cursor()

# Chèn dữ liệu vào bảng user
insert_data_query = '''
INSERT INTO user (username, password) VALUES (?, ?);
'''

# Thực thi lệnh SQL với dữ liệu cụ thể
cursor.execute(insert_data_query, ('thanhdang', '09092003'))
cursor.execute(insert_data_query, ('admin', '123456'))

# Lưu thay đổi (commit) vào cơ sở dữ liệu
conn.commit()

# Đóng kết nối
conn.close()
