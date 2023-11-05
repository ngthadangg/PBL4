import socket             
 
server = socket.socket()         
print ("Socket successfully created")
port = 12345               
 
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
server.bind(('', port))         
print ("socket binded to %s" %(port)) 
 
# put the socket into listening mode 
server.listen(5)     
print ("socket is listening")            
 
# a forever loop until we interrupt it or 
# an error occurs 
while True: 
 
# Establish connection with client. 
  client, addr = server.accept()     
  print ('Got connection from', addr )
 
  # send a thank you message to the client. encoding to send byte type. 
  client.send('Thank you for connecting'.encode()) 
 
  # Close the connection with the client 
  client.close()
   
  # Breaking once connection closed
  break