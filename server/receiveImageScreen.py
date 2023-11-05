import socket			 
from datetime import datetime
import imutils
import pyautogui
import cv2
now = datetime.now()

nameScreen = "D:\\screenshot"+ now.strftime("%H%M%S") +".png"

serverSocket = socket.socket()		 
print ("Socket successfully created")

port = 12345			

serverSocket.bind(('', port))		 
# print ("socket binded to %s" %(port)) 

serverSocket.listen(5)	 
print ("socket is listening in " + str(port))		

# Chấp nhận kết nối từ client
clientSocket, clientAddress = serverSocket.accept()

# Nhận kích thước của file ảnh từ client
file_size = int(clientSocket.recv(1024).decode())
print(file_size)
# Nhận dữ liệu từ client
data = clientSocket.recv(1024)

# Mở một file ảnh mới để lưu dữ liệudd
with open(nameScreen, "wb") as image:
    received_size = 0
    while received_size < file_size:
        data = clientSocket.recv(1024)
        if not data:
            break  
        image.write(data)
        received_size += len(data)
    image.close()


# # Hiển thị ảnh
# cv2.imshow("hacker.com", imutils.resize(image))
# cv2.waitKey(0) #wait for keyboard press

# Đóng kết nối
clientSocket.close()
serverSocket.close()