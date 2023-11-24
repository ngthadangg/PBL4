import sqlite3
import os

def get_edge_history():
    # Đường dẫn đến cơ sở dữ liệu lịch sử của Microsoft Edge
    data_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default'
    history_db = os.path.join(data_path, 'History')

    # Kết nối đến cơ sở dữ liệu lịch sử
    try:
        connection = sqlite3.connect(history_db)
        cursor = connection.cursor()

        # Thực hiện truy vấn để lấy dữ liệu lịch sử
        cursor.execute('SELECT * FROM urls')
        history = cursor.fetchall()

        for row in history:
            web = "Open web : {}".format(row)
            print(web) 
            
        connection.close()       

    except sqlite3.OperationalError as e:
        print(e)

if __name__ == '__main__':
    get_edge_history()
