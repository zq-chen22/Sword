import socket
import threading
from settings import * 

HEADER = 64
PORT = 9090
# SERVER = "156.59.0.73"
SERVER = GLOBAL_IP
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"
ADDR = (SERVER, PORT)

if MODE == "webset":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    remsg_length = int(client.recv(HEADER).decode(FORMAT))
    remsg = client.recv(remsg_length).decode(FORMAT)
    print(remsg)


def upload(msg):
    print(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def download(msg):
    message = (msg + "&download").encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    remsg_length = int(client.recv(HEADER).decode(FORMAT))
    remsg = client.recv(remsg_length).decode(FORMAT)
    return remsg

# print(download("0"))

# if __name__ == "__main__":
#     thread0 = threading.Thread(target = upload, args = ("1&shi",))
#     thread0.start()
#     thread1 = threading.Thread(target = download, args = ("1",))
#     thread1.start()
#     thread2 = threading.Thread(target = upload, args = ("2&hello",))
#     thread2.start()
#     thread3 = threading.Thread(target = download, args = ("2",))
#     thread3.start()