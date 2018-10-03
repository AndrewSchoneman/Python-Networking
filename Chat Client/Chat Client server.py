import socket
 
UDP_IP = '127.0.0.1'
UDP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
people = {}
active = {}
inactive = set()
seqNum = 0
while 1:
     
     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     if not data: break
     print ("received data:", str(data))
     info = data.decode('iso-8859-1')
     info = info.split()
     message = info[1:]
     message = " ".join(message)
     ACK = info[1]
     
     if info[0] not in people and ACK != "ACK313258ghjk12":
          people[info[0]] = addr
          seqNum += 1
          newMessage = data.decode('iso-8859-1')
          newMessage = newMessage + " " + str(seqNum)
          print(newMessage)
          for key in people:
               print(info[0])
               if key not in inactive:
                    sock.sendto(str.encode(newMessage), people[key])
     elif info[0] in people and addr == people[info[0]] and ACK != "ACK313258ghjk12":
          seqNum += 1
          if info[0] in inactive:
               inactive.remove(info[0])
          if message == "I am leaving. Bye!":
               people.pop(info[0], None)
          for key in people:
               if key not in inactive:
                    newMessage = data.decode('iso-8859-1')
                    newMessage = newMessage + " " + str(seqNum)
               sock.sendto(str.encode(newMessage),  people[key])
     elif ACK == "ACK313258ghjk12":
          info[0] = int(info[len(info)-1])
     else:
          sock.sendto(str.encode("Sorry username is in use" + " " +str(seqNum)), addr)
     for key in active:
          if seqNum - active[key] == 3:
               inactive.add(info[0])
serv.close()
