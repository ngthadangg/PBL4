import socket
from datetime import datetime
import cv2
import numpy as np

serverSocket = socket.socket()
print("Socket successfully created")

port = 12345
serverSocket.bind(('', port))
serverSocket.listen(5)

clientSocket, clientAddress = serverSocket.accept()
def shutdown_computer():
    clientSocket.send('shutdown'.encode()) 

def restart_computer():       
    clientSocket.send('restart'.encode()) 