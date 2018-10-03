from tkinter import *
from tkinter import messagebox
import tkinter as Tkinter
from tkinter import filedialog
import threading
import socket

root = Tkinter.Tk()
timeout = False 
users = {}
UDP_IP = '127.0.0.1'
UDP_PORT = 5005
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def showMessageDialog(header, message):
    messagebox.showinfo( header, message)
    

def startStopCallBack():

    try:
        if statusLabelText.get() == "Client is not running.":
            MESSAGE = "Hi, I am joining the room!"
            startStopButton.config(text = "Stop", fg = "red")
            statusLabelText.set("Client is running.")
        
            threading.Thread(target=listen_server).start()
            s.sendto(str.encode("<"+nickText.get() + "> " +MESSAGE ), (UDP_IP, UDP_PORT))
        else:
            showMessageDialog("Goodbye", "You've left the chat")
            s.sendto(str.encode("<"+nickText.get() + "> " +" I am leaving. Bye!" ), (UDP_IP, UDP_PORT))
            s.close()
            root.destroy()
    except:
        showMessageDialog( "Ooops", "Some error occured ...")
        return 
    
    
def messageCallBack(event):
    threading.Thread(target=listen_server).start()
    s.sendto(str.encode("<"+nickText.get() + "> " +messageEntry.get() ), (UDP_IP, UDP_PORT))
    message.set("")
    print(messageEntry.get())
   # showMessageDialog("adfsafd", messageEntry.get())

def listen_server():
    while True:
        
        try:
            data, addr = s.recvfrom(4096)
            
            message = data.decode('iso-8859-1')
            placeHolder = message.split()
            message = message.split()
            seqNum = placeHolder[len(placeHolder) -1]
            message.pop()
            message = " ".join(message)
            print(message)
          #  s.sendto(str.encode("<"+nickText.get() + "> " + "ACK313258ghjk12 "+ seqNum ), (UDP_IP, UDP_PORT))
            if message == "Sorry username is in use":
                showMessageDialog("Error", "Username in use")
                startStopButton.config(text = "Start", fg = "green")
                statusLabelText.set("Client is not running.")
            else:
                s.sendto(str.encode("<"+nickText.get() + "> " + "ACK313258ghjk12 "+ seqNum ), (UDP_IP, UDP_PORT))
                messageText.insert(END, "\n"+message)
        except:
            pass
 


frame = Frame(root)
frame.pack()

root.title("Group chat client application")
root.geometry("800x800")


L1 = Label(root, text="Type a nickname and click start:", font = ('Helvetica', 12, 'normal'))
L1.pack()
L1.place(relx = 0.02,rely = 0.02)
nickText = StringVar()
nickEntry = Entry(root, bd =5,textvariable = nickText)
nickEntry.pack()
nickEntry.place(relwidth=0.35,relx = 0.02,rely = 0.052)

startStopButton = Tkinter.Button(root, text ="Start", font = ('Helvetica', 13, 'bold'),fg = "green", background = "white", activebackground = "red",command = startStopCallBack)

startStopButton.pack()
startStopButton.place(bordermode=OUTSIDE, relheight = 0.065, relwidth=0.15, relx = 0.375, rely = 0.02)

statusLabelText = StringVar()
label = Label( root, textvariable=statusLabelText, font = ('Helvetica', 12, 'normal'),fg = "blue" )
statusLabelText.set("Client is not running.")
label.pack()
label.place(relx = 0.02,rely = 0.12)

scrollbar = Scrollbar(root)
scrollbar.pack()
scrollbar.place(relheight = 0.71,relwidth=0.96, relx = 0.02, rely = 0.15)

   
messageText = Text(root, yscrollcommand = scrollbar.set, font = ('Helvetica', 12, 'normal'))
messageText.insert(END, "Messages from server should appear here.")
messageText.pack()
messageText.place(relheight = 0.70,relwidth=0.94, relx = 0.02, rely = 0.17)
scrollbar.config( command = messageText.yview )
    

L2 = Label(root, text="Type your message and press Enter:", font = ('Helvetica', 12, 'normal'))
L2.pack()
L2.place(relx = 0.02,rely = 0.88)
message = StringVar()
messageEntry = Entry(root, bd =5,textvariable = message)
messageEntry.pack()
messageEntry.bind("<Return>", messageCallBack)
messageEntry.place(relwidth=0.94,relheight = 0.05, relx = 0.02,rely = 0.92)







root.mainloop()
