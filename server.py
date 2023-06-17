# ------- Bolierplate Code Start -----


import socket
from threading import Thread
import time
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os 

IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
buffer_size = 4096
clients = {}
is_dir_exists = os.path.isdir('shared_files')
if(not is_dir_exists):
    os.makedirs('shared_files')
def handleErrorMessage(client):
    message = ''' 
    you need to connect with one of the client first,
    before sending any message. Click on refresh to see
    all available users. '''
    client.send(message.encode())

def sendTextMessage(client_name,message):
    global clients
    other_client_name = clients[client_name]["connected_with"]
    other_client_socket = clients[other_client_name]["client"]
    finalMsg = client_name + ": " + message
    other_client_socket.send(finalMsg.encode())
def handleShowList(client):
    global clients
    counter = 0
    for c in clients:
        counter+=1
        client_address = clients[c]["address"][0]
        connected_with = clients[c]["connected_with"]
        message = ""
        if (connected_with):
            message = f"{counter},{c},{client_address},connected with {connected_with}, tiul,\n"
        else:
            message = f"{counter},{c},{client_address},available,tiul,\n"
        client.send(message.encode())
        time.sleep(1)

def removeClient(client_name):
    try:
        if(client_name in clients):
            del clients[client_name]
    except KeyError:
        pass


def disconnectClient(message,client,client_name):
    global clients
    entered_client_name = message[11:].strip()
    if entered_client_name in clients:
        clients[entered_client_name]["connected_with"] = ""
        clients[client_name]["connected_with"] = ""
        other_client_socket = clients[entered_client_name]["client"]
        greet_message = f"hello, {entered_client_name} {client_name} disconnected with you"
        other_client_socket.send(greet_message.encode())
        msg = f"you are successfully disconnected with {entered_client_name}"
        client.send(msg.encode())

def connectClient(message,client,client_name):
    global clients
    entered_client_name = message[8:].strip()
    if entered_client_name in clients:
        if not clients[client_name]["connected_with"]:
            clients[entered_client_name]["connected_with"] = client_name
            clients[client_name]["connected_with"] = entered_client_name
            other_client_socket = clients[entered_client_name]["client"]
            greet_message = f"hello, {entered_client_name} {client_name} connected with you"
            other_client_socket.send(greet_message.encode())
            msg = f"you are successfully connected with {entered_client_name}"
            client.send(msg.encode())
        else:
            other_client_name = clients[client_name]["connected_with"]
            msg = f"you are already connected with {other_client_name}"
            client.send(msg.encode())
def handleSendFile(client_name,file_name,file_size):
    global clients
    clients[client_name]["file_name"] = file_name
    clients[client_name]["file_size"] = file_size
    other_client_name = clients[client_name]["connected_with"]
    other_client_socket = clients[other_client_name]["client"]
    msg = f"\n{client_name} want to send {file_name} file with size {file_size} bytes. do you want to download?{y/n}"
    other_client_socket.send(msg.encode())
    time.sleep(1)
    msgDown = f"download: {file_name}"
    other_client_socket.send(msgDown.encode())
def grantAccess(client_name):
    global clients
    other_client_name = clients[client_name]["connected_with"]
    other_client_socket = clients[other_client_name]["client"]
    msg = "access granted"
    other_client_socket.send(msg.encode())
def declineAccess(client_name):
    global clients
    other_client_name = clients[client_name]["connected_with"]
    other_client_socket = clients[other_client_name]["client"]
    msg = "access declined"
    other_client_socket.send(msg.encode())
def handleMessages(client, message, client_name):
    if message == 'show list':
        handleShowList(client)
    elif message[:7] == 'connect':
        connectClient(message,client,client_name)
    elif message[:10] == 'disconnect':
        disconnectClient(message,client,client_name)
    elif message[:4] == "send":
        file_name = message.split(" ")[1]
        file_size = int(message.split(" ")[2])
        handleSendFile(client_name, file_name,file_size)
        print(client_name+" "+file_name+" "+ file_size)
    elif message == "y" or message == "Y":
        grantAccess(client_name)
    elif message == "n" or message == "N":
        declineAccess(client_name)
    else:
        connected = clients[client_name]["connected_with"]
        if (connected):
            sendTextMessage(client_name,message)
        else:
            handleErrorMessage(client)


        
def handleClient(client,client_name):
    global clients
    global server
    global buffer_size
    banner1 = "Welcome, You Are Now Connected To Server!\n click on refresh to see all available users\n select the user and click on connect to start chatting"
    client.send(banner1.encode())

    while True:
        try:
            buffer_size = clients[client_name]["file_size"]
            chunk = client.recv(buffer_size)
            message = chunk.decode().strip().lower()
            if (message):
                handleMessages(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass
def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client": client, 
            "address": addr,
            "connected_with": "",
            "file_name" : "",
            "file_size": 4096
        }
        print(f"{client_name}: {addr}")
        thread = Thread(target = handleClient, args=(client,client_name))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()
def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("abcde", "abcde",".",perm = "elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    ftp_server = FTPServer((IP_ADDRESS,21),handler)
    ftp_server.serve_forever()

setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()
ftp_thread = Thread(target = ftp)
ftp_thread.start()


# ------ Bolierplate Code End -----------
