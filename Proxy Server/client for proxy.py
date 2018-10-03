import socket
from time import *
 
TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 20
MESSAGE = "google.com"
PORT = '80'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(str.encode(MESSAGE))
#data = s.recv(BUFFER_SIZE)
#print ("received data:", data)
count  =0
while count < 3:
    MESSAGE = "www.google.com"
    sleep(30)
    try:   	 
        z = s.send(str.encode(MESSAGE+" " + PORT))
        print ("successfully sent " + str(z) + " bytes to port " + str(TCP_PORT))
    except:
        print ("Cannot send data to port " + str(TCP_PORT))

    response = ''   	 
                     
    received = s.recv(16384)
    response+= received.decode('iso-8859-1')           	 
    print (response)

    MESSAGE = "www.yahoo.com"
    try:   	 
        z = s.send(str.encode(MESSAGE+" " + PORT))
        print ("successfully sent " + str(z) + " bytes to port " + str(TCP_PORT))
    except:
        print ("Cannot send data to port " + str(TCP_PORT))

    response = ''   	 
                     
    received = s.recv(16384)
    response+= received.decode('iso-8859-1')           	 
    print (response)

    MESSAGE = "www.uiowa.edu"
    try:   	 
        z = s.send(str.encode(MESSAGE+" " + PORT))
        print ("successfully sent " + str(z) + " bytes to port " + str(TCP_PORT))
    except:
        print ("Cannot send data to port " + str(TCP_PORT))
    received = s.recv(16384)
    response+= received.decode('iso-8859-1')           	 
    print (response)
    count +=1
s.close()
