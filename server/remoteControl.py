import socket
serverSocket = socket.socket()
port = 12345
serverSocket.bind(('', port))
serverSocket.listen(5)

clientSocket, clientAddress = serverSocket.accept()
def shutdown_computer():
    clientSocket.send('shutdown'.encode()) 

def restart_computer():       
    clientSocket.send('restart'.encode()) 