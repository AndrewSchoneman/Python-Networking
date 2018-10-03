#!/usr/bin/env python

# This code is written by Stephen C Phillips.
# It is in the public domain, so you can do what you like with it
# but a link to http://scphillips.com would be nice.

import socket
import re
import select
from string import Template


# Standard socket stuff:
host = '' # do we need socket.gethostname() ?
port = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5) 
inputs = [ sock ]
outputs = []
header = "HTTP/1.1 200 OK \r\n Content-Type: text/html\r\n\r\n " # the header to send
contentType = 'application/x-www-form-urlencoded' # check to see if the POST request is correct
users = {}
# Loop forever, listening for requests:
while True:
    readable, writeable, executable = select.select(inputs, [], [])
    for s in readable: # loop through the inputs list
        if s == sock:
            csock, address = sock.accept() #accept new connection and append it to inputs
            inputs.append(csock)
            print ("Connection from: " + str(address))

        else:
            req = s.recv(1024)
            if req: # if we get a request handle it
                print(req)
                # look for GET requests
                match = re.match('GET /(\\S*) HTTP/1.1', req.decode('iso-8859-1'))
                # look for POST requests
                postMatch = re.match('POST /(\\S*) HTTP/1.1', req.decode('iso-8859-1'))

                if match:
                    # if GET match try and find the requested page
                    file= str(match).split(' ')
                    print(file)
                    if file[5] != "/":
                        
                        try:
                            with open('static' + file[5], 'r') as myfile:
                                data = myfile.read()
                            s.send(str.encode(header + data, 'iso-8859-1'))
                            s.close()
                            inputs.remove(s)
                        except (FileNotFoundError):
                            s.send(str.encode("HTTP/1.1 404 Not Found\r\n",'iso-8859-1'))
                            s.close()
                            inputs.remove(s)
                            #break
                    else:
                        s.send(str.encode("HTTP/1.1 404 Bad Request\r\n",'iso-8859-1'))
                        s.close()
                        inputs.remove(s)                      
                elif postMatch:
                    # if POST match then handle it
                    data = str(req).split("\\n\\r")
                    for word in data:
                        word.rstrip()
                    # parse the content in the POST request
                    content = data[0]
                    content = content.split(' ')
                    content = content[9].split('\\r\\n')
                    if content[0] == contentType:
                        data = str(data[len(data)-1]).split("&")
                        for i in range(len(data)):
                            data[i] = data[i].split("=")
                        with open('static/r1.html', 'r') as myfile:
                            toSend = myfile.read()
                        userInfo = [x[1] for  x in data]
                        #check to see if the user provided all of the necessary info
                        for i in range(len(userInfo)):
                            if userInfo[i] == '':
                                userInfo[i] = "UNKNOWN"
                        temp = Template(toSend)
                        # generate dynamic html and send it along
                        temp = temp.safe_substitute(fname=userInfo[0], lname = userInfo[1], gender = userInfo[2].strip('\''))
                        s.send(str.encode( header + temp, 'iso-8859-1'))
                        s.close()
                        inputs.remove(s)

                else:
                    # bad request so send error message and end connetion
                    s.send(str.encode("HTTP/1.1 404 Bad Request\r\n",'iso-8859-1'))
                    s.close()
                    inputs.remove(s)
                    #break
            else:
                # if no request end connect
                s.close()
                inputs.remove(s)
