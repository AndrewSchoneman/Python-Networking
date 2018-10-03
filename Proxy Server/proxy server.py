import socket
import time
TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
cache = {}
lifetime = {}
conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
     data = conn.recv(BUFFER_SIZE)
     if not data: break
     print ("received data:", str(data))
     response = ''   	 
     info = data.decode('iso-8859-1')   
     info = info.split()
     port = int(info[1])
     host = info[0]
     # Declare socket
     clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     clientSocket.settimeout(1.0)  

     if host not in cache:
          # Connect to the host
          try:
              clientSocket.connect((host, port))
              print ("Successfully connected to port " + str(port))
          except:
              print (host + " cannot be connected to port " + str(port))

          try:   	 
              z = clientSocket.send(str.encode("GET / HTTP/1.0\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"))
              print ("successfully sent " + str(z) + " bytes to port " + str(port))
          except:
              print ("Cannot send data to port " + str(port))

                   
          # Listen and store the response
          response = ''   	 
          while True:           	 
               received = clientSocket.recv(4096)
               response+= received.decode('iso-8859-1')
               print(received)
               if len(received) == 0:
                    break
          
          content =  response.split('\r\n\r\n')[1]
          cache[host] = content
          lifetime[host] = time.time() + 60
          conn.send(str.encode(content))
     elif host in cache and lifetime[host] > time.time():
          content = cache[host]
          conn.send(str.encode(content))
     elif host in cache and lifetime[host] < time.time():
          # Connect to the host


          try:
              clientSocket.connect((host, port))
              print ("Successfully connected to port " + str(port))
          except:
              print (host + " cannot be connected to port " + str(port))

          try:   	 
              z = clientSocket.send(str.encode("GET / HTTP/1.0\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"))
              print ("successfully sent " + str(z) + " bytes to port " + str(port))
          except:
              print ("Cannot send data to port " + str(port))

                   
          # Listen and store the response
          response = ''   	 
          while True:           	 
               received = clientSocket.recv(4096)
               response+= received.decode('iso-8859-1')
               print(received)
               if len(received) == 0:
                    break
          
          content =  response.split('\r\n\r\n')[1]
          cache[host] = content
          lifetime[host] = time.time() + 60
          conn.send(str.encode(content))
     else:
          s.close()
          print("some error occured")
     
