import socket
import threading
import time
from settings import *
# https://realpython.com/python-sockets/

# You have to bind it to your local IP (depending on which network card to use) and make use of port forwarding (NAT) in your router to forward the traffic of the public IP (for the TCP server) to your local IP. In that way your TCP server will be available remotely.

HEADER = 64
PORT = 9090
SERVER = LOCAL_IP
# SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
server.bind(ADDR)
# server.connect(ADDR)

server.listen()

data = [None, None]
recorded = [False, False]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # blocking code
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            clientID = int(msg.split("&")[0])
            if msg.split("&")[1] != "download":
                data[clientID] = msg.split("&")[1]
                recorded[clientID] = True
            else:
                while not recorded[(clientID + 1) % 2]:
                    time.sleep(0.1)
                remsg = data[(clientID + 1) % 2].encode(FORMAT)
                remsg_length = len(remsg)
                send_length = str(remsg_length).encode(FORMAT)
                send_length += b" " * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(remsg)
                recorded[(clientID + 1) % 2] = False
    
    conn.close()
        
def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()