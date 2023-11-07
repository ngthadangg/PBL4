import socket
from datetime import datetime
import cv2
import numpy as np

serverSocket = socket.socket()
print("Socket successfully created")

port = 12345
serverSocket.bind(('', port))
serverSocket.listen(5)
print("Socket is listening on " + str(port))

clientSocket, clientAddress = serverSocket.accept()

# Nhận kích thước của file ảnh từ client
file_size = int(clientSocket.recv(1024).decode())

# Nhận dữ liệu từ client
received_data = b""
while len(received_data) < file_size:
    data = clientSocket.recv(1024)
    received_data += data

# Chuyển dữ liệu nhận được thành mảng hình ảnh
image_array = np.frombuffer(received_data, dtype=np.uint8)

# Đọc mảng hình ảnh thành hình ảnh OpenCV
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# Hiển thị hình ảnh
cv2.imshow("hacker.com", image)
cv2.waitKey(0)  # Đợi nhấn một phím bất kỳ để đóng cửa sổ hiển thị

# Đóng kết nối
clientSocket.close()
serverSocket.close()
