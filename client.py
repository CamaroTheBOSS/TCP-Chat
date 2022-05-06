import socket
import threading
from bs4 import BeautifulSoup as bS

HEADER = 8        # 8 bytes for message's length
MESSAGE_TYPE = 2  # 2 bytes for message's type

PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)

name = str(input("Nickname: "))
print("Connected...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(message):
    # Sending message
    message = message.encode(FORMAT)
    header = str(len(message)).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    header = b'00' + header
    client.send(header)
    client.send(message)


def sendDoc(pathToDoc: str):
    # Reading doc file
    soup = bS(open(pathToDoc).read(), features='lxml')
    [s.extract() for s in soup(['style', 'script'])]
    tmpText = soup.get_text()
    message = ("[" + name + "]: " + "".join("".join(tmpText.split('\t')).split('\n'))).encode(FORMAT).strip()

    # Sending message
    header = str(len(message)).encode(FORMAT)
    header += b' ' * (HEADER - len(header))
    header = b'01' + header
    client.send(header)
    client.send(message)


def writing():
    while True:
        message = str(input())
        if message == "dc" or message == DISCONNECT_MESSAGE:     # Disconnecting message
            send(DISCONNECT_MESSAGE)
            break
        elif len(message) > 8:  # Send *.doc message
            if message[:8] == "sendDoc ":
                try:
                    sendDoc(message[8:])
                except FileNotFoundError:
                    print("File not found")
            else:  # Send usual message
                message = "[" + name + "]" + ": " + message
                send(message)
        else:  # Send usual message
            message = "[" + name + "]" + ": " + message
            send(message)


def reading():
    while True:
        # Confirming response from the server
        length = client.recv(HEADER).decode(FORMAT)
        if length:
            length = int(length)
            message = client.recv(length).decode(FORMAT)
            print(message)


def start():
    write = threading.Thread(target=writing)
    write.start()
    read = threading.Thread(target=reading)
    read.start()


start()
