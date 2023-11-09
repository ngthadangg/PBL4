import socket
from datetime import datetime
import cv2
import numpy as np

serverSocket = socket.socket()
print("Socket successfully created")

port = 12345

def shutdown():
        serverSocket.bind(('', port))
        serverSocket.listen(5)
        # print("Socket is listening on " + str(port))

        clientSocket, clientAddress = serverSocket.accept()
        
        clientSocket.send('shutdown'.encode()) 

def restart():
        serverSocket.bind(('', port))
        serverSocket.listen(5)
        # print("Socket is listening on " + str(port))

        clientSocket, clientAddress = serverSocket.accept()
        
        clientSocket.send('restart'.encode()) 