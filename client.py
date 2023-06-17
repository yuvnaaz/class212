#-----------Bolierplate Code Start -----
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
from ftplib import FTP
import ntpath
from tkinter import filedialog
import os
from pathlib import Path
sending_file = None
downloading_file = None
fileToDownload = None

PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None
global filePathLabel
def connectToServer():
    global SERVER
    global name
    name1 = name.get()
    SERVER.send(name1.encode())
def showClientList():
    global listbox
    listbox.delete(0,"end")
    SERVER.send("show list".encode("ascii"))
def disconnectWithClient():
    global SERVER
    global listbox
    text = listbox.get(ANCHOR)
    list_item = text.split(":")
    msg = "disconnect "+ list_item[1]
    SERVER.send(msg.encode('ascii'))
def connectWithClient():
    global SERVER
    global listbox
    text = listbox.get(ANCHOR)
    list_item = text.split(":")
    msg = "connect "+ list_item[1]
    SERVER.send(msg.encode('ascii'))
def getFileSize(file_name):
    with open(file_name,"rb") as file:
        chunk = file.read()
        return len(chunk)

def browseFiles():
    global textarea
    global filePathLabel
    global sending_file
    try:
        filename = filedialog.askopenfilename()
        filePathLabel.configure(text=filename)
        HOSTNAME = "127.0.0.1"
        USERNAME = "abcde"
        PASSWORD = "abcde"
        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)
        with open(filname, 'rb') as f:
            ftp_server.storbinary(f"STOR {fname}", f)
        ftp_server.dir()
        ftp_server.quit()
        message = ("send " +fname)
        if message[:4] == "send":
            textarea.insert(END,"\n please wait \n")
            textarea.see("end")
            sending_file = message[5:]
            filesize = getFileSize("shared_files/" + sending_file)
            finalMessage = message+" "+str(filesize)
            SERVER.send(finalMessage.encode())
            textarea.insert(END,"in proccess")
    except FileNotFoundError:
        print("cancel button pressed")

def sendMessage():
    global SERVER
    global textarea
    global text_message
    global fileToDownload
    msgToSend = text_message.get()
    SERVER.send(msgToSend.encode('ascii'))
    textarea.insert(END,"\n" + "you: " + msgToSend)
    textarea.see("end")
    text_message.delete(0,'end')
    if msgToSend == "y" or msgToSend == "Y":
        textarea.insert(END, "\n please wait file is downloading")
        textarea.see("end")
        HOSTNAME = "127.0.0.1"
        USERNAME = "abcde"
        PASSWORD = "abcde"
        home = str(Path.home())
        download_path = home+"/Downloads"
        ftp_server = ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd("shared_files")
        fname = fileToDownload
        local_filename = os.path.join(str(download_path,fname))
        file = open(local_file_name, 'wb')
        ftp_server.retrbinary('RETR '+ fname, file.write)
        ftp_server.dir()
        file.close()
        ftp_server.quit()
        print("file successfully downloaded")
        textarea.insert(END,"\n" + "file successfully downloaded" + download_path)
        textarea.see("end")


def openChatWindow():

   
    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10))
    namelabel.place(x=10, y=8)

    name = Entry(window,width =30,bd = 1,font = ("Calibri",10))
    name.place(x=120,y=8)
    name.focus()

    connectserver = Button(window,text="Connect to Chat Server",bd=1, font = ("Calibri",10),command=connectToServer)
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10))
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10))
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10),command = connectWithClient)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10), command = disconnectWithClient)
    disconnectButton.place(x=350,y=160)

    refresh=Button(window,text="Refresh",bd=1, font = ("Calibri",10), command = showClientList)
    refresh.place(x=435,y=160)

    labelchat = Label(window, text= "Chat Window", font = ("Calibri",10))
    labelchat.place(x=10, y=180)

    textarea = Text(window, width=67,height=6,bd = 1,font = ("Calibri",10)) 
    textarea.place(x=10,y=200)

    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = textarea.yview)

    attach = Button(window,text = "Attach and send", bd = 1, font = ("Calibri",10), command = browseFiles)
    attach.place(x=10,y=305)

    text_message = Entry(window, width = 43,bd = 1, font = ("Calibri",12))
    text_message.place(x=98,y=305)

    

    send = Button(window,text= "Send", bd = 1, font = ("Calibri",10), command = sendMessage)
    send.place(x=450,y=305)

    filepathlabel = Label(window, text = "", fg = "blue", font = ("Calibri",10))
    filepathlabel.place(x=10,y=330)


  
  
  
  
  
    window.resizable(False,False)
    window.mainloop()



def recvMessage():
    global SERVER
    global BUFFER_SIZE

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                list1 = chunk.decode().split(",")
                listbox.insert(list1[0],list1[0] + ":" + list1[1]+":"+list1[3]+" "+list1[5])
                print(list1[0],list1[0] + ":" + list1[1]+":"+list1[3]+" "+list1[5])
            elif chunk.decode() == "access granted":
                labelchat.configure(text = "")
                textarea.insert(END, "\n" +chunk.decode('ascii'))
                textarea.see("end")
            elif chunk.decode() == "access declined":
                labelchat.configure(text = "")
                textarea.insert(END, "\n" +chunk.decode('ascii'))
                textarea.see("end")
            elif "download?" in chunk.decode():
                downloading_file = chunk.decode('ascii').split(" ")[4].strip()
                BUFFER_SIZE = int(chunk.decode('ascii').split(" ")[8])
                textarea.insert(END, "\n" +chunk.decode('ascii'))
                textarea.see("end")
            elif "download:" in chunk.decode():
                getfilename = chunk.decode().split(":")
                fileToDownload = getfilename[1]

            
            else:
                textarea.insert(END,"\n"+chunk.decode("ascii"))
                textarea.see("end")
                
        except:

            pass

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    thread1 = Thread(target = recvMessage)
    thread1.start()

   
    openChatWindow()

setup()
